import click
import tfidf
import ppmi
from nltk.tokenize import word_tokenize

# There is a LOT of repeated code in here.
# The TF-IDF and PPMI commands really do the same thing, so at some point
# I will refactor this and clean it up


# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group()
def cli():
  click.echo('Metrics launched.')

@cli.command('tfidf', context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

@click.option('--words', '-w', type=click.File('r', encoding='utf8'),
                help='Only use a specific set of words (from a file).')
# options/flags
@click.option('--transpose', '-t', is_flag=True,
                help='Swap rows and columns.')
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def run_tfidf(in_file, out_file, no_header, dos_eol, words, transpose):
  ''' Evaluates a list of sentences using tf-idf. '''
  all_lines = [line.strip() for line in in_file]
  click.echo('Found {} lines.'.format(len(all_lines)))
  if no_header:
    del all_lines[0]
  all_documents = [(doc.strip(), word_tokenize(doc.lower())) for doc in  all_lines]

  click.echo('Getting unique words for tf-idf.')
  word_index = 0
  total_documents = len(all_documents)
  # create a list of all the unique words in the full set of documents
  all_unique_words = []
  if words:
    all_unique_words = [x.strip() for x in words.readlines()]
  else:
    for _,doc_tokens in all_documents:
      try:
        for word in doc_tokens:
          if word not in all_unique_words:
            all_unique_words.append(word)

        word_index += 1
        if word_index % 50 == 0:
          click.echo('\rProcessed {} documents of {}.'.format(word_index, total_documents), nl=False)
      except:
        word_index += 1
        click.echo('Error on line: {}'.format(word_index))
    click.echo('\rProcessed {} documents of {}.'.format(word_index, total_documents), nl=False)
    click.echo(' Found {} unique words.'.format(len(all_unique_words)))

    # sort so we can manually view the results easier (looking for terms)
    all_unique_words.sort()
    click.echo('Sorted.')

  # with all_unique_words as the rows and sentences as the columns
  term_doc_matrix = []

  # build the header row (word, all sentences, avg, <any extra columns>)
  header_row = []
  header_row.append('TERM,IS_SPATIAL')
  for sentence,_ in all_documents:
    sent = sentence.replace('\t',',').replace('"','').strip()
    header_row.append(sent)
  header_row.append('AVG TF-IDF')
  term_doc_matrix.append(header_row)

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_unique_words)
  all_docs_length = len(all_documents)
  word_index = 0

  # create a row for each term
  click.echo('Building matrix...')
  for term in all_unique_words:
    term_row = []
    term_row.append(term)
    num_docs_with_term = tfidf.docs_with(term, all_documents)

    # add the tf-idf of term in each sentence as columns
    for i,(_,doc_tokens) in enumerate(all_documents):
      term_row.append(round(tfidf.tf(term, doc_tokens) * tfidf.idf(term, all_documents, all_docs_length, num_docs_with_term),4))

    # insert average at the end (skipping the first word column)
    average_tfidf = sum(term_row[1:]) / (len(term_row[1:]))
    term_row.append(average_tfidf)
    # row finished, add it to the matrix
    term_doc_matrix.append(term_row)

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 5 == 0:
      click.echo('\rTF-IDF\'d {} words of {}.'.format(word_index, total_word_count), nl=False)


  click.echo('\rTF-IDF\'d {} words of {}.'.format(total_word_count, total_word_count))
  click.echo('Matrix is row:{} x col:{}'.format(len(term_doc_matrix), len(header_row)))
  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo(' Saving...')
  # save the words into a tf-idf matrix, tab-separated
  output = term_doc_matrix
  if transpose:
    click.echo('Transposing...')
    output = [*zip(*term_doc_matrix)]
    click.echo('Matrix is row:{} x col:{}'.format(len(output), len(output[0])))
  for row in output:
    out_file.write('{}{}'.format(','.join([str(x) for x in row]), eol))
  out_file.close()
  click.echo('Done!')


@cli.command('ppmi', context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

@click.option('--words', '-w', type=click.File('r', encoding='utf8'),
                help='Only use a specific set of words (from a file).')
# options/flags
@click.option('--transpose', '-t', is_flag=True,
                help='Swap rows and columns.')
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def run_ppmi(in_file, out_file, no_header, dos_eol, words, transpose):
  ''' Evaluates a list of sentences using tf-idf. '''
  all_lines = [line.strip() for line in in_file]
  click.echo('Found {} lines.'.format(len(all_lines)))
  if no_header:
    del all_lines[0]
  all_documents = [(doc.strip(), word_tokenize(doc.lower())) for doc in  all_lines]

  click.echo('Getting unique words for tf-idf.')
  word_index = 0
  total_documents = len(all_documents)
  # create a list of all the unique words in the full set of documents
  all_unique_words = []
  if words:
    all_unique_words = [x.strip() for x in words.readlines()]
  else:
    for _,doc_tokens in all_documents:
      try:
        for word in doc_tokens:
          if word not in all_unique_words:
            all_unique_words.append(word)

        word_index += 1
        if word_index % 50 == 0:
          click.echo('\rUniq\'d {} documents of {}.'.format(word_index, total_documents), nl=False)
      except:
        word_index += 1
        click.echo('Error on line: {}'.format(word_index))
    click.echo('\rUniq\'d {} documents of {}.'.format(word_index, total_documents), nl=False)
    click.echo(' Found {} unique words.'.format(len(all_unique_words)))

    # sort so we can manually view the results easier (looking for terms)
    all_unique_words.sort()
    click.echo('Sorted.')

  # with all_unique_words as the rows and sentences as the columns
  term_doc_matrix = []

  # build the header row (word, all sentences, avg, <any extra columns>)
  header_row = []
  header_row.append('TERM,IS_SPATIAL')
  for sentence,_ in all_documents:
    sent = sentence.replace('\t',',').replace('"','').strip()
    header_row.append(sent)
  header_row.append('AVG PPMI')
  term_doc_matrix.append(header_row)

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_unique_words)
  all_docs_length = len(all_documents)
  print(total_word_count)
  print(all_docs_length)
  word_index = 0

  # create a row for each term
  click.echo('Building matrix...')
  for term in all_unique_words:
    term_row = []
    term_row.append(term)
    total_occurences = ppmi.total_occurences(term, all_documents)

    # add the ppmi of term in each sentence as columns
    normsum = ppmi.get_normalisation_sum(all_documents)
    for i,(_,doc_tokens) in enumerate(all_documents):
      term_row.append(round(ppmi.positive_pmi(term, doc_tokens, all_documents, normsum, total_occurences, 4)))

    # insert average at the end (skipping the first word column)
    average_ppmi = sum(term_row[1:]) / (len(term_row[1:]))
    term_row.append(average_ppmi)
    # row finished, add it to the matrix
    term_doc_matrix.append(term_row)

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 5 == 0:
      click.echo('\rPPMI\'d {} words of {}.'.format(word_index, total_word_count), nl=False)


  click.echo('\rPPMI\'d {} words of {}.'.format(total_word_count, total_word_count))
  click.echo('Matrix is row:{} x col:{}'.format(len(term_doc_matrix), len(header_row)))
  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo(' Saving...')
  # save the words into a tf-idf matrix, tab-separated
  output = term_doc_matrix
  if transpose:
    click.echo('Transposing...')
    output = [*zip(*term_doc_matrix)]
    click.echo('Matrix is row:{} x col:{}'.format(len(output), len(output[0])))
  for row in output:
    out_file.write('{}{}'.format(','.join([str(x) for x in row]), eol))
  out_file.close()
  click.echo('Done!')