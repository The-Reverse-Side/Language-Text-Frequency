# Text Frequency Analyzer

### Objective: 
Reads in text, separate all words, lemmitizes them, remove any words already known. Then creates a csv, sorted by word-frequency, along with an example sentence where that word appears, plus some visualizations just for fun. Made for language learning.


## Installation
To install libraries run command: `python -m pip install -r requirements.txt`

Install [SpaCy language model](https://spacy.io/usage/models):

Spanish language model: `python -m spacy download es_dep_news_trf`

Italian language model: `python -m spacy download it_core_news_lg`

Swedish language model: `python -m spacy download sv_core_news_lg`

German language model: `python -m spacy download de_dep_news_trf`


### Files & order of use:
- **generate_word_set.py** - If you have just a raw .txt file, start here. Creates a single-row of cleaned words to be used in *populate_unknown_words.py*
- **populate_unknown_words.py** - Quickly populates known_words list for preemptively removing known words from *word_frequency_analysis's* output. Saves time and effort.
- **word_frequency_analysis.py** - Analyzes word frequency and outputs a csv as shown below. Also displays helpful visualizations.

    The output csv format was designed for editing then to be directed loaded into the [Anki](https://apps.ankiweb.net/) flashcard app. After importing into Anki, you can generate audio via Awesome TTS.
    ```
    Column1		    Column2	    Column3
    FrequencyInPDF	UniqueWord	ExampleSentence
    6               Gilipollas  Eres gilipollas
    ```


- **known_words_utilities.py** A collection of useful functions for cleaning/adjusting known_words files. You probably wont need to use it unless you manually dump a bunch of words in there. 

## Future features, known issues and misc
**Future features**
- It would be nice if each example sentence were unique, instead of 5 of the same sentence for each word. I could 'fix' this by randomizing card presentation order in Anki though.
- Make the word frequency square plot more friendly, instead of needing to manually enter everything.

**Known issues:**
- ExampleSentence formatting is still weird somtimes, and it still doesnt pick optimal sentences. Todo: recognize and pick another.
- Spanish - SpaCy has trouble with backticks - sesión, más, víctima, aún - when lemmatizing, despite it using spanish model
- Spanish - It separates the object pronouns, lemmitizes it (él) and adds a space. Which creates weird results such as "deshidratar él". Todo: recognize and trim.
- "es" is getting cut off words due to lemmtization being over-zealous Peeves, muggles. Lemmas are customizable if I wanna go to the trouble.

**Misc:**
- Note: I didnt include any definitions because they can be a bit weird, some sites have one word, others have long, obtuse definitions. I prefer to add them myself, especially if its small batches of words. Quality of quantity.

### License
This project is licensed under the MIT License - see the [LICENSE](./license.txt) file for details.
