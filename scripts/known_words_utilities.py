'''
    A collection of useful functions for cleaning/adjusting known_words files
    This should theoretically make it easier to keep things clean and formatted
'''

import csv
import glob

def clean_csv_inplace(file_path):
    '''Removes duplicates, whitespace, and lower()s all words'''
    cleaned_words = set()

    # Step 1: Read and clean the words
    with open(file_path, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            for word in row:
                # Convert to lowercase, strip whitespace
                clean_word = word.strip().lower()
                if clean_word: # Skip empty lines
                    cleaned_words.add(clean_word)

    # Step 2: Write the cleaned words back to the same file
    with open(file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for word in sorted(cleaned_words):
            writer.writerow([word])

    print(f"Cleaned words saved back to '{file_path}'. Total unique words: {len(cleaned_words)}")


# Go through and clean all known_words files, despite language
# INPUT_FILE_PATH = "./known_words/known_words_de.csv"  # Replace with your input CSV file path
directory_path = "./known_words"

for csv_file in glob.glob(os.path.join(directory_path, "*.csv")):
    print(f"Processing file: {csv_file}")
    clean_csv_inplace(csv_file)