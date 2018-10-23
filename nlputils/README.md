# NLP Utils (nlputils)
A bunch of utility scripts bundled into a nice installable package.

## Installation
Download the folder, open the terminal and install with pip using `pip install .`.

The program can then be run by calling `nlputils` in the terminal, or `nlputils --help` for more options.

## Usage
```
Usage: nlputils [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dedupe   Removes duplicates and blanks from a line
  untrash  <tba>
  transform  <tba>
```

## Commands
### dedupe
Removes blank and duplicate lines from a file. Can exclude headers. Case-sensitive by default.

```
Usage: nlputils dedupe [OPTIONS] IN_FILE OUT_FILE

  Removes duplicates and blanks from a line

Options:
  -n, --no-header  Exclude the header when processing.
  -n, --dos-eol    Use \r\n dos line endings. Default is UNIX.
  --version        Show the version and exit.
  -h, --help       Show this message and exit.
```

