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
  untrash  Fixes or purges lines with shoddy character...
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

### untrash
Removes or fixes badly encoded characters (trash) in files. Can also skip over websites because they ain't one of them real sentences.

```
Usage: nlputils untrash [OPTIONS] IN_FILE OUT_FILE

  Fixes or purges lines with shoddy character encoding.

Options:
  -x, --delete-trash  Delete lines with trash. Default process is to try
                      clean them.
  -u, --delete-urls   Delete lines that look like urls.
  -n, --no-header     Exclude the header when processing.
  -d, --dos-eol       Use \r\n dos line endings. Default is UNIX.
  --version           Show the version and exit.
  -h, --help          Show this message and exit.
```