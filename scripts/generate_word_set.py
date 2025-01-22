'''Takes input.txt and converts it into a cleaned, single column of words'''

import csv
import spacy


# Load spaCy's model
LANGUAGE_MODEL = "en_core_web_trf" #! currently hardcoded German de_dep_news_trf
# English: en_core_web_trf
nlp = spacy.load(LANGUAGE_MODEL)


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


INPUT_FILE = "./input/jim.txt"
OUTPUT_FILE = "processed/cleaned_word_set.csv"

word_set = extract_words(INPUT_FILE)

print(f"A total of {len(word_set)} have been extracted")

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as known_file:
		writer = csv.writer(known_file)
		writer.writerows([[word] for word in word_set])
