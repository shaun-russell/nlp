# Read Me
This algorithm is very old and was my first attempt at a Natural Language Processing program that identifies spatial things in sentences. It basically just looks in lists.

Better programs have since been developed. _No judgements on the code quality please_.

## Installation
Download the source, navigate to the folder with all the Python files and run `pip install .` to install.

Then `isspatial --help` to see the usage instructions (and verify installation). Might need additional installation for `nltk` if you get Python errors.

Because of poor architecture and the need of lookup files, the program needs to know where these files are. This is what the `path-file` input is for. In the source code, there is a file called `paths.txt`. This needs to be copied to the directory you are going to run the program in and passed as an argument to the program.

Remember to update the paths inside the file to wherever you've downloaded the source code to.

## Usage
```
Usage: isspatial [OPTIONS] IN_FILE PATH_FILE OUT_FILE

  Attempts to evaluate whether or not a line is spatial. If evaluating,
  make sure the columns are tab-separated. Excel can do this. NOTE: Not
  tagging place names because lookup dataset is too big and inefficient.

Options:
  -n, --no-header       Exclude the header when processing.
  -d, --dos-eol         Use \r\n dos line endings. Default is UNIX.
  --version             Show the version and exit.
  -h, --help            Show this message and exit.
  ```

## Examples
Basic example is `isspatial test-sentences.txt paths.txt output.txt`

## Notes
There are some limitations with this program:
- Placename identification is disabled. This program runs on lookups and the size of the placenames dataset is too big to upload and use effectively. Additionally, the accuracy was poor because almost everything was confirmed as a placename due to the variety of names in the dataset.