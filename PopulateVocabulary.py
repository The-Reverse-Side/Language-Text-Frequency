import csv
import keyboard
import re

import spacy

'''Script aimed at quickly separating lists of words into:
    They go into 'known words' for future filtering
	They are unknown = make flashcards for them
	
	Mainly this is to quickly populate a 'known words' for more effective filtering,
	which requires less time manually in the csv deleting rows from ExtractFromFile.py

	This should be passed a one-column csv with german words. It will strip and lemmatize them
	This should only be one word, as well. Annoying the lemmas are messy to handle with things like 'der tag'
	'''

def clean_up_input(txt_file_path, input_file):
	cleaned_words = []
	with open(input_file, "r", encoding="utf-8") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			for word in row:  # Process each cell
				word = re.sub(r'[\u200b-\u200d\u2060\uFEFF]+|[ \t]+', ' ', word).strip()
				if word and not re.match(r'^\W+$', word):
					cleaned_words.append(word)

		
    # Write the words to a text file, one word per line
	with open(txt_file_path, "w", encoding="utf-8") as txtfile:
		for word in cleaned_words:
			txtfile.write(word + "\n")
    
	print(f"Words have been saved to {txt_file_path}")


# Function to process the words
def process_words(input_file, SPACY_MODEL):
	flashcard_words = []
	known_words = []
	words = []
	spacy_approved_words = "./Misc/spacy_friendly_words.txt"
	
    #! First I need to convert the csv into a Spacy-friendly format
	clean_up_input(spacy_approved_words, input_file)

    #! Then I can load friendly format into spacy
	nlp_model = spacy.load(SPACY_MODEL)
	print("Model loaded, starting processing...")
	with open(spacy_approved_words, "r", encoding="utf-8") as file:
		words = [line.strip() for line in file if line.strip()]  # Remove empty lines and whitespace

	# Lemmatize words using spaCy
	lemmatized_words = []
	print("'Flashcard Words' <-   -> 'Known Words'")
	for word in words:
		str_word = str(nlp_model(word)[0].lemma_) # Process each word with spaCy

		print(f"\nWord: {str_word}")

		while True:
			event = keyboard.read_event()  # Waits for a key event

			if event.event_type == keyboard.KEY_DOWN:
				if event.name == 'left':
					flashcard_words.append(str_word)
					print(f"Added '{word}' to Flashcard Words.")
					break
				elif event.name == 'right':
					known_words.append(str_word)
					print(f"Added '{word}' to Known Words.")
					break
				elif event.name == 'down':
					print(f"Skipped '{str_word}'.")
					break

	# Save new_filter_words to a new CSV file
	with open('Output/keeper_words.csv', 'w', newline='', encoding='utf-8') as new_file:
		writer = csv.writer(new_file)
		writer.writerows([[word] for word in flashcard_words]) # it wants a list of lists, so we have to wrap it

	# Save known_words to a new CSV file
	with open('Output/known_words.csv', 'w', newline='', encoding='utf-8') as known_file:
		writer = csv.writer(known_file)
		writer.writerows([[word] for word in known_words])

	print("Processing complete. Files saved.")


def main():
	# Language model stuff
	SPACY_MODEL = "de_dep_news_trf"
	print(f"Loading German spacy model...")
	

    # 'The rest'
	input_file_path = './Source/populate3.csv'
	process_words(input_file_path, SPACY_MODEL)


if __name__ == "__main__":
	main()
