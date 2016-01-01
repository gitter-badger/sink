# sink

[![Join the chat at https://gitter.im/Kyle-Verhoog/sink](https://badges.gitter.im/Kyle-Verhoog/sink.svg)](https://gitter.im/Kyle-Verhoog/sink?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
sink things

## Install
Clone the repository
`git clone https://github.com/kyle-verhoog/sink`

then run the setup script
`python setup.py`

## Development

### Code Formatting

#### Guidelines
See https://www.python.org/dev/peps/pep-0008

#### Code Formatter
We use Google's [YAPF](https://github.com/google/yapf)


To install, ensure `pip` is installed, then

`pip install yapf`


To apply the formatter to a file (in-place)

`yapf -i --style="pep8" <file.py>`

in order to not apply the formatter in-place and overwrite the file, do not include the `-i` option

`yapf --style="pep8" <file.py>`

### Dependencies
Requires the Dropbox API.

Installation instructions here: https://github.com/dropbox/dropbox-sdk-python

### Tokens
In order to use the Dropbox API you need an OAuth2 token to be generated. You can generate one for development by creating an app and generating an access token.

