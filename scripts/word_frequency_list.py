import collections
import csv
import re
import time

import pdfplumber
import pyinputplus as pyip
import spacy
import unicodedata

#n El pasaje: The text is composed of 84% new words: 12725 total words: 2032 known words, 10693 new words.
#n Percy Jackson 2: The text is composed of 75% new words: 6460 total words: 1590 known words, 4870 new words.
#n Harry Potter 1: The text is composed of 73% new words: 5548 total words: 1478 known words, 4070 new words.

#! Perhaps I can also add a big list of names, cities, etc to known_words
#! Write a helper script to read the known_words, make it a set, and especially for spanish, provide alternatives:
    #! Levantar el -> also add levantar, (better to do that than trim it off)
    # SpaCy can check for verbs, so I can go through the verb list and add el to all of them as well
    # at some point I actually need to go through those words too.. maybe make that rapid review script

INPUT_FILE = "./Source/source.txt" # provide either a .pdf or .txt file
filter_words_path = "./KnownWords/filter_words.csv"
# prompt = "What language is this text? (Italian, Spanish, German, or Swedish)\n"
# language = pyip.inputMenu(["Italian", "Spanish", "Swedish", "German"], prompt)

language = 'German' #! hardcoding for now

known_words_path = "./KnownWords/known_words"
match language:
        case "Spanish":
            known_words_path = known_words_path + "_es.csv"
            SPACY_MODEL = "es_dep_news_trf" # A 'trained language pipeline'
        case "Swedish":
            known_words_path = known_words_path + "_sv.csv"
            SPACY_MODEL = "sv_core_news_lg"
        case "Italian":
            known_words_path = known_words_path + "_it.csv"
            SPACY_MODEL = "it_core_news_lg"
        case "German":
            known_words_path = known_words_path + "_de.csv"
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


def main():
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
    filter_words = [word.lower().strip() for word in read_csv_list(filter_words_path)]

    wanted_words = list(
        set(unique_lemmas) - set(known_word_lemmas) - set(filter_words)) #* These are my unknown words

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
                data.append([lemma_frequencies[word], word, clean_sentence])
                break
    sorted_data = sorted(data, key=lambda x : x[0], reverse=True) # I guess 'x' iterates over every item?
    save_csv(sorted_data, "Output/OUTPUT_"+language+".csv")
        #INPUT_FILE.split(".")[0] just removes the file type text

    print(f"\nDone! Total execution time {time.time()-start_time:.0f} seconds ({(time.time()-start_time)/60:.0f} min)")


if __name__ == "__main__":
    main()