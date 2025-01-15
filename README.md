# Text Frequency Analyzer

### Objective: 
To take a foreign-language text, separate all words, lemmitizes (base form) them, create a set with individual instances of words, remove any words already known. 
Then create a csv, sorted by frequency that the word appears in the pdf, along with an example sentence of that word. + some fancy looking visualizations just for fun.

### Files:
- **KnownWords/known_words_{language}.csv** - Words that I already know and can be skipped in the frequency list
  - Includes cards that are already added as Anki cards
  - Currently no other source - Im working on other script to quickly populate this list
- **source.pdf/source.txt** - Foreign-language text
- **output_name_of_document.csv** - the final resulting document
- **ExtractFromFile.py** - 
- **FilterOutput.py** -
- **app.py** -


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


**Known_Words:**
Note: Analyze.py lemmitizes known_words before filtering out.. so known_words.csv can be very ugly
- filter_words.csv - is a general list of words with countries and characters in my series that I dont need to learn
- filter_words_{langauge}.csv - is a language-specific list of words I know, populated from Anki
- Note to self: My known words are stored in Google sheets - Vocab Lexicon pages




**Weird things:**
- ExampleSentence formatting is still weird somtimes.
- Spanish - SpaCy has trouble with backticks - sesión, más, víctima, aún - when lemmatizing, despite it using es model
- Spanish - It separates the object pronouns, lemmitizes it (él) and adds a space. Which creates weird results such as "deshidratar él"
- "es" is getting cut off words due to lemmtization being over-zealous Peeves, muggles. Lemmas are customizable if I wanna go to the trouble.

**Future features**
- It would be nice if each example sentence were unique, instead of 5 of the same sentence for each word. I could 'fix' this by randomizing card presentation order in Anki though.