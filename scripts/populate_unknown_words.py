'''
	Script aimed to quickly populate a 'known words' list for more effective filtering.
	
	This requires less time than manually deleting rows from word_frequency_list.py
	This should be passed a one-column csv of words.
'''

import csv
import re

import keyboard
import spacy


def clean_up_input(CLEANED_WORDS_PATH, INPUT_FILE):
	'''Extracts words from the CSV, removes unnecessary characters, strips, etc. 
	Creates a nice txt file for SpaCy to use at txt_file_path'''

	cleaned_words = set()
	with open(INPUT_FILE, "r", encoding="utf-8") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			for word in row:
				# removing those annoying mystery spaces, tabs, weirdshit
				word = re.sub(r'[\u200b-\u200d\u2060\uFEFF]+|[ \t]+',' ',word).strip().lower()
				if word and not re.match(r'^\W+$', word):
					cleaned_words.add(word)

	print("cleaned_words length ", len(cleaned_words))

    # Write the words to a text file, one word per line
	with open(CLEANED_WORDS_PATH, "w", encoding="utf-8") as txtfile:
		for word in cleaned_words:
			txtfile.write(word + "\n")
    
	print(f"Words cleaned! Saved to path: {CLEANED_WORDS_PATH}")


def process_words(INPUT_FILE, SPACY_MODEL):
	'''Takes txt file and lemmatizes each phrase, then prompts user to sort'''
	new_known_words = []
	words = []
	CLEANED_INPUT = "./processed/spacy_friendly_words.txt"
	KNOWN_WORDS_PATH = f'./known_words/known_words_de.csv' # hardcoded german for now
	
    # First I need to convert the csv into a Spacy-friendly format
	clean_up_input(CLEANED_INPUT, INPUT_FILE)

    # Now I can load the cleaned file into spacy
	nlp_model = spacy.load(SPACY_MODEL)
	print("Model loaded, starting processing...")
	with open(CLEANED_INPUT, "r", encoding="utf-8") as file:
		# Remove empty lines and whitespace.. just in case
		words = [line.strip() for line in file if line.strip()]

	# Remove any words already in known_words from words
	csv_words = set()
	with open(KNOWN_WORDS_PATH, "r", encoding="utf-8") as file:
		reader = csv.reader(file)
		for row in reader:
			if row:  # Avoid empty lines
				csv_words.add(row[0])  # Add the word to the set, stripping whitespace

	filtered_list = [word for word in words if word not in csv_words]
	print("filtered_list length ", len(filtered_list))

	# Lemmatize words using spaCy
	lemmatized_words = []
	print("'Unknown (skip) Words' <--   --> 'Known Words'")
	for word in filtered_list:
		processed_word = nlp_model(word)
		lemmatized_phrase = " ".join([token.lemma_ for token in processed_word])

		print(f"\nWord: {lemmatized_phrase}")


		while True:
			event = keyboard.read_event()  # Waits for a key event

			# if word not already in new_known_words, then process
			if word in new_known_words:
				print("ALREADY IN THE LIST") # added cuz I was getting dupes, but now there are none.. 
				break

			if event.event_type == keyboard.KEY_DOWN:
				if event.name == 'left':
					print(f"Ignoring '{lemmatized_phrase}'.")
					break
				if event.name == 'right':
					new_known_words.append(lemmatized_phrase)
					print(f"Added '{lemmatized_phrase}' to Known Words.")
					break

	# Append new known words to existing known_words csv for that language
	with open(KNOWN_WORDS_PATH, 'a', newline='', encoding='utf-8') as known_file:
		writer = csv.writer(known_file)
		writer.writerows([[word] for word in new_known_words])


	print("Processing complete. known_words updated.")


def main():
	# todo-eventually.. select language here later on
	SPACY_MODEL = "de_dep_news_trf"	
	INPUT_FILE = './processed/generated_words.csv'

	process_words(INPUT_FILE, SPACY_MODEL)


if __name__ == "__main__":
	main()
