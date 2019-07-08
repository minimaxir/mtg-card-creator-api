# mtg-card-creator-api

API to create Magic card images by using Magic Set Editor and wine, enclosed in a Docker container for use in Google Cloud Run. Input is an encoded card string via mtg-gpt-2-cloud-run, outputs are Gatherer-formated text and a card image.

The API wraps code from Bill Zorn's [mtgencode](https://github.com/billzorn/mtgencode) (MIT, and Python 2 so the container includes a Python 2.7 runtime), and Magic Set Editor to render the cards into JPEGs.

This is *incredibly* jank programming, but it is not the bottleneck in the card generation (the GPT-2 text generation is) and streamlining the code workflow would not have a noticable effect on performance.

## Installation

Because the licensing for Magic Set Editor and fonts are ambigious, they are not included in this repo:

* For Magic Set Editor, download Basic [Magic Set Editor 2.0.1](http://magicseteditor.boards.net/page/downloads) (*not* 2.0!) and move the resulting `MSE` folder to the repo folder.
* For the fonts, download the "Fonts for Magic Templates" [here](http://msetemps.sourceforge.net/phpBB3/viewtopic.php?t=144#p601). Copy the fonts from the `Magic - All` and `Magic - After M15` folders into a `fonts` folder in the repo folder.

## Helpful Notes

* The image is returned as a base64-encoded string. It's the user's responsibility to add an approrpiate MIME-type if necessary.
* The card formatting issues are due to the underlying mtgencode/MSE implementations and are not easy to fix. (most notable with Planeswalker cards)

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

*Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use.*

## License

MIT

## Disclaimer

This repo has no affiliation or relationship with OpenAI or Wizards of the Coast.