# Text Frequency Analyzer

**Objective**: To take a foreign-language text, separate all words, lemmitizes (base word form) them, create a set with individual instances of words, remove any words already known. 
Then create a list, sorted by frequency that the word appears in the pdf, accompanied by an example sentence of that word. + some fancy looking visualizations just for fun.

**Files**:
- KnownWords/known_words_{language}.csv - Words that I already know and can be skipped in the frequency list
  - Includes cards that are already added as Anki cards
- source.pdf/.txt - Foreign-language text
- output_name_of_document.csv - the final resulting document


So output format (output_name_of_document.csv) should be:
```
Column1		Column2		Column3
FrequencyInPDF	UniqueWord	ExampleSentence
```
This makes it easier to import as cards in the [Anki](https://apps.ankiweb.net/) flashcard app.



## Installation and usage
To install libraries run command `python3 -m pip install -r requirements.txt`
Install Spanish language model `python3 -m spacy download es_core_news_lg`
Install Italian language model `python3 -m spacy download it_core_news_lg`
Install Swedish language model `python3 -m spacy download sv_core_news_lg`

To run the program just run command `python3 ExtractFromFile.py`


**Known_Words:**
Note: Analyze.py lemmitizes known_words before filtering out.. so known_words.csv can be very ugly




**Weird things:**
- ExampleSentence formatting is still weird somtimes.
- Spanish - SpaCy has trouble with backticks - sesión, más, víctima, aún - when lemmatizing, despite it using es model
- Spanish - It separates the object pronouns, lemmitizes it (él) and adds a space. Which creates weird results such as "deshidratar él"
- "es" is getting cut off words due to lemmtization being over-zealous Peeves, muggles. Lemmas are customizable if I wanna go to the trouble.

**Future features**
- It would be nice if each example sentence were unique, instead of 5 of the same sentence for each word. I could 'fix' this by randomizing card presentation order in Anki though.