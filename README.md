# Foreign Language Text Frequency Analyzer

**Objective**: To take a foreign-language PDF (source_language.pdf) and isolate all words, lemmitize them, create a set with individual instances of words, remove any words already known (known_words.csv). Then create a list, sorted by frequency that the word appears in the pdf, accompanied with an example sentence of that word.

**Files**:
- source_language.pdf - Foreign-language PDF (example "source_es.pdf")
- known_words.csv - Words that I already know, duh. From Anki and Top1000 word lists. Not from Google Sheets pending words
- output_name_of_document.csv - the final resulting document


So output format (output_name_of_document.csv) should be:
```
Column1		Column2		Column3
FrequencyInPDF	UniqueWord	ExampleSentence
```
This makes it easier to import as cards in the [Anki](https://apps.ankiweb.net/) flashcard app.



## Installation and usage
To install libraries run command `python3 -m pip install -r requirements.txt`
Install Spanish language model `python3 -m spacy download es_dep_news_trf`
Install Swedish language model `python3 -m spacy download sv_core_news_lg`

To run the program just run command `python3 analyze.py`


**Known_Words:**
Note: Analyze.py lemmitizes known_words before filtering out.. so known_words.csv can be very ugly

Spanish: I am starting from scratch, so dont need to worry about what was previously in Anki
- El Problema de los Tres Cuerpos
- 1000 most frequent words

Swedish: A bit of a mess...
- Harry Potter och De Vises Sten
- 1000 most frequent words


**Weird things:**
- ExampleSentence formatting is still weird somtimes.
- In Spanish, it separates the object pronouns, lemmitizes it (él) and adds a space. Which creates weird results such as "deshidratar él"


**Future features**
- It would be nice if each example sentence were unique, instead of 5 of the same sentence for each word. I could fix this by randomizing card presentation order in Anki though.