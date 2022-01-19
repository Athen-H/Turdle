# Turdle
A questionable Wordle clone made with Python.

I have no idea what I'm doing here so this all kind of a huge mess, but I think it works.

shitlesscorn.txt contains 4,177 'reasonable' 5-letter words that the game can choose from as the 'goal' word.
Obtained from http://www.mieliestronk.com/corncob_lowercase.txt but stripped of slurs and most exclusively proper nouns.
As the source states, this list prefers British over American spellings.

words_alpha.txt contains 15,918 5-letter words, many very unreasonable, to use as a check when trying to submit a word.
It would be annoying to try to submit a real word but be denied because your word is unreasonable.
Obtained from https://github.com/dwyl/english-words, not yet stripped so it contains lots of superfluous non-5-letter words.

Thanks to Sid for much help with all this.
