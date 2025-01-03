# import csv
# import keyboard

'''Unused script aimed at quickly separating lists of words into known/unknown lists to population known_words_{lang}'''

# # Function to process the words
# def process_words(input_file):
# 	new_filter_words = []
# 	known_words = []

# 	print("'Filter Words' <-   -> 'Known Words'")

# 	with open(input_file, newline='', encoding='utf-8') as csvfile:
# 		reader = csv.reader(csvfile)

# 		for row in reader:
# 			index, word, sentence = row
# 			print(f"\nWord: {word}")

# 			while True:
# 				event = keyboard.read_event()  # Waits for a key event

# 				if event.event_type == keyboard.KEY_DOWN:
# 					if event.name == 'left':
# 						new_filter_words.append(row)
# 						print(f"Added '{word}' to New Filter Words.")
# 						break
# 					elif event.name == 'right':
# 						known_words.append(row)
# 						print(f"Added '{word}' to Known Words.")
# 						break
# 					elif event.name == 'down':
# 						print(f"Skipped '{word}'.")
# 						break

# 	# Save new_filter_words to a new CSV file
# 	with open('Output/new_filter_words.csv', 'w', newline='', encoding='utf-8') as new_file:
# 		writer = csv.writer(new_file)
# 		writer.writerows(new_filter_words)

# 	# Save known_words to a new CSV file
# 	with open('Output/known_words.csv', 'w', newline='', encoding='utf-8') as known_file:
# 		writer = csv.writer(known_file)
# 		writer.writerows(known_words)

# 	print("Processing complete. Files saved.")


# if __name__ == "__main__":
# 	input_file = 'Output/OUTPUT_Spanish.csv'  # Replace with your input file path
# 	process_words(input_file)
