# replace all this with click package stuff
import sys
import math

input_filename = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) > 2 else input_filename[:-4]+'output.txt'

from nltk.tokenize import word_tokenize

# tf = term frequency: how frequently a word appears in a document (sentence).
#       TF(t) is num_of_occurences_of(t) / total_terms_in_document
def tf(term, document):
  ''' Term frequency calculation for term in a document (sentence). '''
  frequency = len([w for w in document if w == term])
  terms_in_doc = len(document)
  return frequency / terms_in_doc

# idf = inverse document frequency: how important the term is. Frequent words
#       like 'a', 'the', 'are'..etc are given low importance values because
#       they are so common.
#       IDF(t) = log(document_count / document_count_containing(t))
def idf(term, all_documents):
  ''' Inverse document frequency calculation for term in all documents (all sentences). '''
  document_count = len(all_documents)
  documents_with_term = len([doc for doc in all_documents if term in doc])
  return math.log(document_count / documents_with_term)

# ppmi = Positive Point-wise Mutual Information.
#         This is the same as PMI, but with negative values replaced with zero.
#         PMI measures the likelihood of a word being associated with another
#         word (collocations?)
#         This isn't an alternative to tf-idf, but instead of values the
#         'relatedness' of two words.

def ppmi():
  pass


# replace this with a command-line command
def main():
  # lowercasing all words because otherwise there will be too many and it 
  # will be too messy
  all_lines = [line.strip() for line in open(input_filename, encoding='utf8').readlines()]
  all_documents = [(doc.strip(),word_tokenize(doc.lower())) for doc in  all_lines]

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
  header_row += [sentence for _,sentence in all_documents]
  header_row.append('AVG TF-IDF')

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_unique_words)
  word_index = 0

  # create a row for each term
  for term in all_unique_words:
    term_row = []
    term_row.append(term)

    # add the tf-idf of term in each sentence as columns
    for doc,doc_tokens in all_documents:
      term_row.append(tf(term, doc_tokens) * idf(term, all_documents))

    # insert average at the end (skipping the first word column)
    average_tfidf = sum(term_row[1:]) / (len(term_row[1:]))
    term_row.append(average_tfidf)
    # row finished, add it to the matrix
    term_doc_matrix.append(term_row)

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index >= 50:
      print('\rProcessed {} words of {}.'.format(word_index, total_word_count))

  line_endings = '\r\n' if input('DOS line endings (\\r\\n)? y/n: ').lower() == 'y' else '\n'
  # save the words into a tf-idf matrix, tab-separated
  out_file = open(output_filename, 'w+', encoding='utf8')
  for row in term_doc_matrix:
    out_file.write('{}{}'.format([str(x) for x in row], line_endings))
  out_file.close()
  print('Done!')

if __name__ == '__main__': main()
