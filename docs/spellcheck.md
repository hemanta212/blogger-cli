# Spellchecking (Experimental)
Spellchecking is available in blogger for 'Html', 'ipynb' and 'markdown' files. It is best supported in markdown files. However, technically you can run the 'spellcheck' command on any type of file.

## Usage
The command only takes a single parameter that is a file path.

    $ blogger spellcheck  ~/test.md

It outputs incorrect words, its line no and suggestion(if available)
Due to 'pyspellcheck' being slow in large files it's suggestions is not displayed. You can use -f to force suggestions.

## Performance
Spellchecking is not an easy job. An offline blogger engine can only do so much.
There are some issues with spellchecking.
- Text extraction
- Speed of suggestion

### Speed of suggestion
The following library is used by blogger to provide this functionality:
- misspellings
- pyspellcheck

Both are available offline. Misspellings have a collection of misspelling->correct word map.
It is much faster but its scope is low and only catch common English errors.
You can get incorrect words and suggestions if 'misspellings' catches it.

Similarly, 'pyspellcheck' almost catches all incorrect spellings. But running its suggestion engine in blog posts files is very expensive so suggestions are not available.

'Pyspellcheck', obviously is not complete as it sometimes can label correct words as incorrect especially if there are slang words, brand names and such.

### Text extraction
Extracting sentence structure is difficult without Natural language processing. Blogger instead splits each word and passes into spell-check. This leads to some problems where the words at last of a sentence get extracted along with grammatical symbols and are marked as incorrect words like 'good?', 'go.', etc.
Ignoring words with these symbols was not an option as it may suppress real incorrect words.

However, Html tags and other redundancies are eliminated.

To sum up, 'spellcheck' command leaves you to filter through incorrect and analyze mistakes for the most part.
