# mtg-card-creator-api

Docker container to create Magic card images by using Magic Set Editor and wine. Input is an encoded card string, outputs are Gatherer-formated text and a card image.

## Installation

Because the licensing for Magic Set Editor and fonts are ambigious, they are not included in this repo:

* For Magic Set Editor, download Basic [Magic Set Editor 2.0.1](http://magicseteditor.boards.net/page/downloads) (*not* 2.0!) and move the resulting `MSE` to the repo folder.
* For the fonts, download the "Fonts for Magic Templates [here](http://msetemps.sourceforge.net/phpBB3/viewtopic.php?t=144#p601). Copy the fonts from the `Magic - All` and `Magic - After M15` folders into a `fonts` folder in the repo folder.

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

*Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use.*

## License

MIT

## Disclaimer

This repo has no affiliation or relationship with OpenAI or Wizards of the Coast.