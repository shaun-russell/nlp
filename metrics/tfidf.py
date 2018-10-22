


# replace all this with click package stuff
import sys
import math

input_filename = sys.argv[1]
case_sensitive = bool(sys.argv[2])
output_filename = sys.argv[3] if len(sys.argv) > 3 else input_filename[:-4]+'output.txt'

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

def ppmi():
  pas


def main():
  all_documents = [word_tokenize(doc) for doc in open(input_filename).readlines()]
