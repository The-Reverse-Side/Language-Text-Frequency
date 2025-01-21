# Text Frequency Analyzer

### Objective: 
To take a foreign-language text, separate all words, lemmitizes (base form) them, create a set with individual instances of words, remove any words already known. 
Then create a csv, sorted by frequency that the word appears in the pdf, along with an example sentence of that word. + some fancy looking visualizations just for fun.

### Files:
- **known_words_utilities.py** - A collection of useful functions for cleaning/adjusting known_words files. Should theoretically make it easier to keep things clean and formatted
- **generate_word_set.py** - Cleans up raw txt to be used in *populate_unknown_words.py*
- **populate_unknown_words.py** - Used for populating a known_words_{language} list for preemptively removing known words from *word_frequency_list's* output.
- **word_frequency_list.py** - Used for creating flashcards based on word frequency from a text.

You need the following file structure:
- input dir
- known_words dir
- output dir
- processed dir
alongside the already-existing scripts dir


So output format (output_name_of_document.csv) is as follows:
This makes it easier to import as cards in the [Anki](https://apps.ankiweb.net/) flashcard app.
```
Column1		    Column2	    Column3
FrequencyInPDF	UniqueWord	ExampleSentence
6               Gilipollas  Eres gilipollas
```


## Installation and usage
To install libraries run command: `python -m pip install -r requirements.txt`

Install Spanish language model: `python -m spacy download es_dep_news_trf`
Italian language model: `python -m spacy download it_core_news_lg`
Swedish language model: `python -m spacy download sv_core_news_lg`
German language model: `python -m spacy download de_dep_news_trf`



**Weird things:**
- ExampleSentence formatting is still weird somtimes, and it still doesnt pick optimal sentences. Todo: recognize and pick another.
- Spanish - SpaCy has trouble with backticks - sesión, más, víctima, aún - when lemmatizing, despite it using spanish model
- Spanish - It separates the object pronouns, lemmitizes it (él) and adds a space. Which creates weird results such as "deshidratar él". Todo: recognize and trim.
- "es" is getting cut off words due to lemmtization being over-zealous Peeves, muggles. Lemmas are customizable if I wanna go to the trouble.

**Future features**
- It would be nice if each example sentence were unique, instead of 5 of the same sentence for each word. I could 'fix' this by randomizing card presentation order in Anki though.