'''Takes input.txt and converts it into a cleaned, single column of words'''

import csv
import spacy


# Load spaCy's model
GERMAN_MODEL = "de_dep_news_trf" #! currently hardcoded German
nlp = spacy.load(GERMAN_MODEL)


def extract_words(file_path):
    """Reads a .txt file, extracts words, and puts them in a single column csv"""
    words = set()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Tokenize each line with spaCy
            doc = nlp(line.lower().strip())
            for token in doc:
                # Filter out punctuation, and spaces
                if token.is_alpha:
                    words.add(token.text)

    return words


INPUT_FILE = "./input/input.txt"
OUTPUT_FILE = "processed/cleaned_word_set.csv"

word_set = extract_words(INPUT_FILE)

print(f"Extracted words: {word_set}")

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as known_file:
		writer = csv.writer(known_file)
		writer.writerows([[word] for word in word_set])
