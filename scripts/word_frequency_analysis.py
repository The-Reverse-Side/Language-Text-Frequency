import collections
import csv
import re
import time
import unicodedata

import matplotlib.pyplot as plt
import pandas as pd
import pdfplumber
import pyinputplus as pyip
import spacy
from matplotlib.patches import Patch
from pywaffle import Waffle
import plotly.graph_objects as go

#n El pasaje: The text is composed of 84% new words: 12725 total words: 2032 known words, 10693 new words.
#n Percy Jackson 2: The text is composed of 75% new words: 6460 total words: 1590 known words, 4870 new words.
#n Harry Potter 1: The text is composed of 73% new words: 5548 total words: 1478 known words, 4070 new words.

#! Perhaps I can also add a big list of names, cities, etc to known_words
#! Write a helper script to read the known_words, make it a set, and especially for spanish, provide alternatives:
    #! Levantar el -> also add levantar, (better to do that than trim it off)
    # SpaCy can check for verbs, so I can go through the verb list and add el to all of them as well
    # at some point I actually need to go through those words too.. maybe make that rapid review script

INPUT_FILE = "./input/input.txt" # provide either a .pdf or .txt file
# prompt = "What language is this text? (Italian, Spanish, German, or Swedish)\n"
# language = pyip.inputMenu(["Italian", "Spanish", "Swedish", "German"], prompt)

language = 'German' #! hardcoding for now

known_words_path = "./known_words/known_words.csv"
match language:
        case "Spanish":
            SPACY_MODEL = "es_dep_news_trf" # A 'trained language pipeline'
        case "Swedish":
            SPACY_MODEL = "sv_core_news_lg"
        case "Italian":
            SPACY_MODEL = "it_core_news_lg"
        case "German":
            SPACY_MODEL = "de_dep_news_trf"


def extract_text_from_pdf(pdf_path: str) -> str:
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                all_text += extracted_text.encode('utf-8').decode('utf-8')  # Re-encode to ensure UTF-8
    return all_text


def extract_text_from_txt(txt_path: str) -> str:
    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        #q I manually encoded it in Notepad++ too, still works without manual conversion?
        return txt_file.read()


def save_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)


def read_csv_text(filename):
    with open(filename, 'r', encoding='utf-8') as csv_file:
        text = csv_file.read()
    return normalize_text(text)


def read_csv_list(filename):
    with open(filename, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        # Flattening rows into a single list
        words = [word.lower() for row in reader for word in row]
    return words


def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFC', text)


def analyze_text_frequency():
    start_time = time.time()

    print(f"Got it, loading {language} spacy model...")

    nlp_model = spacy.load(SPACY_MODEL) # Returns a Language object convention is to call it nlp
    nlp_model.max_length = 2000000 # Explicitly increasing max length to handle large books
    print("Model loaded, starting processing...")

    # Checking the file type and calling the appropriate method
    if INPUT_FILE[-3:] == "pdf":
        source_text = extract_text_from_pdf(INPUT_FILE)
    elif INPUT_FILE[-3:] == "txt":
        source_text = extract_text_from_txt(INPUT_FILE)
    else: # Wrong file type!
        raise Exception("Wrong file type!")

    # Process text, get word content
    # try:
    processed_text = nlp_model(source_text) # Processed text (tokenized), but still contains white spaces for example
    # Tokenization is when text is split into words, punctuation marks, etc
    words = [token.text for token in processed_text if token.is_alpha] # Getting content for each token if alphabetic char
    # except ValueError:
    #     print("The file is too big!") #maybe it makes sense to check the file size first instead??


    # Get word lemmas and their frequency
    word_lemmas = [token.lemma_.lower().strip() for token in processed_text if token.is_alpha] # Getting lemma for each token if alphabetic char
    lemma_frequencies = collections.Counter(word_lemmas) # Returns a dict sorted with frequency of word occurrences
    unique_lemmas = list(lemma_frequencies.keys()) # The keys of course are the words

    # Separate sentences and format them nicely
    split_characters = r'[.!?]'
    sentences = re.split(split_characters, source_text) # Separating out the sentences from the original text
    sentences = [sentence.strip()+"." for sentence in sentences if sentence.strip()] # Strips all non-empty sentences

    # Filter out unwanted words from known_words_{lang}
    known_words = read_csv_text(known_words_path)
    processed_known_words = nlp_model(known_words)
    known_word_lemmas = [token.lemma_.lower().strip() for token in processed_known_words if token.is_alpha]

    wanted_words = list(
        set(unique_lemmas) - set(known_word_lemmas)) #* These are my unknown words

    unwanted_word_count = len(set(unique_lemmas)) - len(set(wanted_words)) #* Known words

    total_word_count = len(unique_lemmas)
    new_word_percentage = int((total_word_count - unwanted_word_count) / total_word_count * 100) # unique lemmas / unwanted words
    print(f"\nThe text is composed of {new_word_percentage}% new words: "
          f"{total_word_count} total words: {unwanted_word_count} known words, " # catching everything in the list?
          f"{total_word_count - unwanted_word_count} new words.")

    data = []
    for word in wanted_words:
        # print(word)
        index = word_lemmas.index(word) # grabs the location of that lemma
        conjugated_word = words[index] # Then uses that to find the conjugated version of the word
        for sentence in sentences: # There should be a more efficient way of doing this..?
            if conjugated_word in sentence:
                sentence = sentence[:250] # Trying to stop these overly long example sentences (normally bugs)
                clean_sentence = sentence.replace('\n', ' ')  # Replace new lines with a space
                data.append([lemma_frequencies[word], word, "", clean_sentence]) # includes empty column for definitions
                break

    # header = ["Frequency", "Word", "Definition", "Example Sentence"]

    sorted_data = sorted(data, key=lambda x : x[0], reverse=True) # I guess 'x' iterates over every item?
    save_csv(sorted_data, "output/word_frequency_"+language+".csv")
        #INPUT_FILE.split(".")[0] just removes the file type text

    print(f"\nDone! Total execution time {time.time()-start_time:.0f} seconds ({(time.time()-start_time)/60:.0f} min)")




def word_freq_square_plot():
    '''Creates a square plot that compares new/known word ratio for (manually inserted) book data'''
    pasaje_data = {'New Words': 10693, 'Known Words': 2032}
    percy_jackon_data = {'New Words': 4870, 'Known Words': 1590}
    harry_potter_data = {'New Words': 3443, 'Known Words': 1712}
    colors=['#217A79',  '#97E196',]

    # Calculate percentage of new words
    # pasaje_new_words_pct = pasaje_data['New Words'] / sum(pasaje_data.values()) * 100
    # percy_new_words_pct = percy_jackon_data['New Words'] / sum(percy_jackon_data.values()) * 100
    # harry_new_words_pct = harry_potter_data['New Words'] / sum(harry_potter_data.values()) * 100


    plot1 = {'values': [count/100 for count in pasaje_data.values()], # [expression for item in iterable]
             'title': {'label': f'El Pasaje: Probably CEFR C1+ level', 'loc': 'left', 'fontsize': 12}
            }
    plot2 = {'values': [count/100 for count in percy_jackon_data.values()],
            'title': {'label': f'Percy Jackson 2: 9-12 year olds', 'loc': 'left', 'fontsize': 12}
    }
    plot3 = {'values': [count/100 for count in harry_potter_data.values()],
            'title': {'label': f'Harry Potter 1: 9-12 year olds', 'loc': 'left', 'fontsize': 12}
    }


    fig = plt.figure(
        1,
        FigureClass=Waffle,
        plots={
            311: plot1,
            312: plot2,
            313: plot3,
        },
        rows=5,
        colors=colors, # Our focus is on New Words, so we make that the bolder color
        rounding_rule='ceil',  # Change rounding rule, so value less than 1000 will still have at least 1 block
        figsize=(8, 6)
    )

    # fig.text(0.85, 0.75, f'{pasaje_new_words_pct:.1f}% new words', fontsize=16, color=colors[0], fontweight='bold')  # For El Pasaje
    # fig.text(0.85, 0.45, f'{percy_new_words_pct:.1f}% new words', fontsize=16, color=colors[0], fontweight='bold')   # For Percy Jackson
    # fig.text(0.85, 0.15, f'{harry_new_words_pct:.1f}% new words', fontsize=16, color=colors[0], fontweight='bold')   # For Harry Potter


    legend_elements = [Patch(facecolor=colors[0], label='New Words'),
                       Patch(facecolor=colors[1], label='Known Words')]

    fig.legend(
        handles=legend_elements,
        labels=['New Words', 'Known Words'],
        loc='lower right',
        fontsize=10,
        # frameon=False,
        bbox_to_anchor=(0.95, 0.05),
        title="Legend"
    )

    # Add a title and a small detail at the bottom
    fig.suptitle('Word Analysis of several Spanish language books', fontsize=14, fontweight='bold')
    fig.supxlabel(f"Each block represents 100 unqiue words",
                  fontsize=8,
                  x=0.5, # position at the 14% axis
                 )
    fig.set_facecolor('#F1F1F1') # This is the background

    plt.show()

    # So here we can tell The Passage (El Pasaje) has much more of an advanced vocabulary,
    # and generally a much more diverse vocabulary
    # With this, I can select a book based on the challenge I want,
    # then go to the vocab frequency to see what kind of words I can expect to learn



def word_frequency_chart(min_word_freq):
    '''Frequency chart. max_word_freq determines the lowest word freq to include in chart'''
    #! hardcoded German for now
    df = pd.read_csv('./output/word_frequency_German.csv', header=None, names=['Frequency', 'Word', 'Definition', 'Example']) 

    # Filter words with frequency >= min_word_freq
    df = df[df['Frequency'] >= min_word_freq]

    # Sort the dataframe by frequency in descending order
    df = df.sort_values('Frequency', ascending=False)

    # Create a color scale based on the frequency
    color_palette = ['#D3F2A3', '#97E196', '#6CC08B', '#5BAE94', '#217A79', '#105965', '#074050']

    min_freq = df['Frequency'].min()
    max_freq = df['Frequency'].max()
    norm = (df['Frequency'] - min_freq) / (max_freq - min_freq)
    colors = [color_palette[int(n * (len(color_palette) - 1))] for n in norm]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df['Word'],
            y=df['Frequency'],
            hovertext = df['Word'] + " : " + df['Frequency'].astype(str) + "<br><br>" + df['Example'],
            hoverinfo='text',
            marker_color=colors,
            marker_line=dict(width=1, color=colors),
            opacity=1,
            name='Word Frequency'
        )
    )

    fig.update_layout(
        plot_bgcolor='#F5F5F5'
    )

    fig.update_xaxes(
        title_text='Word',
        title_font={"weight": "bold"}, #"size": 18, "family": "Arial, sans-serif", "color": "black",
        tickfont={"weight": "bold"},
        tickangle=45,
    )

    fig.update_yaxes(
        title_text='Frequency',
        title_font={"weight": "bold"},
        tickfont={"weight": "bold"},
    )

    fig.show()



def main():
    analyze_text_frequency() # Needed for plotting

    # word_freq_square_plot() # Displays a square plot of various (manually inserted) book's new/known word ratios
    word_frequency_chart(5) # Creates a chart with desc word frequency


if __name__ == "__main__":
    main()