# Metric calculating program
A program to calculate NLP and text-specific statistical functions like TF-IDF (Term-Frequency Inverse Document-Frequency), PMI (Pointwise Mutual Information) and PPMI (Positive Pointwise Mutual Information).

## Installation
Download the folder, open the terminal and install with pip using `pip install .`.

The program can then be run by calling `metrics` in the terminal, or `metrics --help` for more options.

## Usage
```
Usage: metrics [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  tfidf  Removes duplicates and blanks from a line
```

## Commands
### tfidf
Calculates the tf-idf of every word for every sentence in a list. Outputs the result as a matrix with the last column containing the average tf-idf value for a term.

```
Usage: metrics tfidf [OPTIONS] IN_FILE OUT_FILE

  Removes duplicates and blanks from a line

Options:
  -n, --no-header  Exclude the header when processing.
  -d, --dos-eol    Use \r\n dos line endings. Default is UNIX.
  --version        Show the version and exit.
  -h, --help       Show this message and exit.
```

