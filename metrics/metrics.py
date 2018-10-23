import click
import tfidf
from nltk.tokenize import word_tokenize

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
def cli():
  click.echo('Metrics launched.')


@cli.command('tfidf', context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

# options/flags
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def deduplicate(in_file, out_file, no_header, dos_eol):
  ''' Removes duplicates and blanks from a line '''
  all_lines = [line.strip() for line in in_file]
  if no_header:
    del all_lines[0]
  all_documents = [(doc.strip(), word_tokenize(doc.lower())) for doc in  all_lines]

 # create a list of all the unique words in the full set of documents
  all_unique_words = []
  for _,doc_tokens in all_documents:
    for word in doc_tokens:
      if word not in all_unique_words:
        all_unique_words.append(word)

  # sort so we can manually view the results easier (looking for terms)
  all_unique_words.sort()

  # with all_unique_words as the rows and sentences as the columns
  term_doc_matrix = []

  # build the header row (word, all sentences, avg, <any extra columns>)
  header_row = []
  header_row.append('TERM')
  header_row += [sentence for sentence,_ in all_documents]
  header_row.append('AVG TF-IDF')

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_unique_words)
  word_index = 0

  # create a row for each term
  for term in all_unique_words:
    term_row = []
    term_row.append(term)

    # add the tf-idf of term in each sentence as columns
    for _,doc_tokens in all_documents:
      term_row.append(round(tfidf.tf(term, doc_tokens) * tfidf.idf(term, all_documents), 4))

    # insert average at the end (skipping the first word column)
    average_tfidf = sum(term_row[1:]) / (len(term_row[1:]))
    term_row.append(average_tfidf)
    # row finished, add it to the matrix
    term_doc_matrix.append(term_row)

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 10 == 0:
      click.echo('\rProcessed {} words of {}.'.format(word_index, total_word_count), nl=False)


  click.echo('\rProcessed {} words of {}.'.format(total_word_count, total_word_count), nl=False)
  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo(' Saving...')
  # save the words into a tf-idf matrix, tab-separated
  for row in term_doc_matrix:
    out_file.write('{}{}'.format([str(x) for x in row], eol))
  out_file.close()
  click.echo('Done!')