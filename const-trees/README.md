# Treefurcate (used as 'treefurcate')

This program can process and display tree structures in files. Plain sentences can be outputted with their corresponding constituency tree (using the Stanford CoreNLP server) and trees can be viewed using the tree visualiser.

The location (url/address) of the CoreNLP server can be specified as an argument, but the default is localhost using port 9000.

## Installation
Download the files and install locally with pip. Requires Python 3 and the `click` package (this should be installed automatically because it's a required package).

`pip install .`

Once installed, run `treefurcate -h` or `NAME --help` in the terminal for usage instructions.

## Usage
This is what the help screen shows.
```
Usage: treefurcate [OPTIONS] IN_FILE [OUT_FILE]

  A description of what this main function does.

Options:
  -c, --corenlp TEXT  The url of the CoreNLP Server. Default is
                      localhost:9000.
  -p, --process       Process the line. If no process, program looks in
                      in_file for tree to visualise.
  -v, --visualise     Draw each tree as it is processed. DON'T USE WHEN BIG
                      FILE.
  --verbose           Enables information-dense terminal output.
  --version           Show the version and exit.
  -h, --help          Show this message and exit.
```

## Examples
Using the sample files, an example is:

`treefurcate sentences.txt output.txt -p --verbose`

This example takes a list of plain-text sentences and creates the constituency tree for each line. The output is the original sentence followed by the tree as a string, separated by a TAB character.

`

## Notes
- Does x.
- Has y.
- Default w is z.

## To-do
- List stuff here.