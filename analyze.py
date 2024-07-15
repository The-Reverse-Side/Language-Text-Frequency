import collections
import csv
import pprint as pp
import re
import time

import pdfplumber
import spacy

INPUT_FILE = "source_sv.pdf" #source_sv.pdf source_es.pdf
SPACY_MODEL = "sv_core_news_lg" # Swedish: "sv_core_news_lg"     Spanish: "es_dep_news_trf"


def extract_text_from_pdf(pdf_path: str):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text


def save_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(data)


def read_csv(filename):
    with open(filename, 'r') as csv_file:
        text = csv_file.read()
    return text

def main():
    start_time = time.time()

    print("Loading spacy model...")
    nlp = spacy.load(SPACY_MODEL) #? What exactly is this called?
    print("Starting...")
    split_characters = r'[.!?]'
    text = extract_text_from_pdf(INPUT_FILE)
    doc = nlp(text)
    word_lemmas = [token.lemma_ for token in doc if token.is_alpha] # gathering word lemmitzations if alphabetic chars
    words = [token.text for token in doc if token.is_alpha] # gathering individual words if alphabetic chars
    
    # Split sentences, lemmitize them, and figure out frequency
    sentences = re.split(split_characters, text) # Splitting sentences individually
    sentences = [sentence.strip()+"." for sentence in sentences if sentence.strip()]
    frequencies = collections.Counter(word_lemmas)
    unique_lemmas = list(frequencies.keys())

    # Filter out unwanted words from known_words.csv
    unwanted_words = read_csv("known_words.csv")
    doc_unlovable = nlp(unwanted_words)
    unlovable_word_lemmas = [token.lemma_ for token in doc_unlovable if token.is_alpha]
    wanted_words = list(set(unique_lemmas) - set(unlovable_word_lemmas))

    data = []
    for word in wanted_words:
        index = word_lemmas.index(word)
        conjugated_word = words[index]
        for sent in sentences:
            if conjugated_word in sent:
                data.append([frequencies[word], word, sent])
                break
    sorted_data = sorted(data, key=lambda x: x[0], reverse=True)
    save_csv(sorted_data, "OUTPUT_"+INPUT_FILE.split(".")[0]+".csv")

    print(f"Done! Total execution time {time.time()-start_time:.0f} seconds ({(time.time()-start_time)/60:.0f} min)")

    


if __name__ == "__main__":
    main()