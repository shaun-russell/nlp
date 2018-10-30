# replace all this with click package stuff
import math

# tf = term frequency: how frequently a word appears in a document (sentence).
#       TF(t) is num_of_occurences_of(t) / total_terms_in_document
def tf(term, document):
  ''' Term frequency calculation for term in a document (sentence). '''
  frequency = len([w for w in document if w == term])
  terms_in_doc = len(document)
  # avoid divide-by-zero errors
  if terms_in_doc == 0:
    return 0
  return frequency / terms_in_doc

# idf = inverse document frequency: how important the term is. Frequent words
#       like 'a', 'the', 'are'..etc are given low importance values because
#       they are so common.
#       IDF(t) = log(document_count / document_count_containing(t))
def idf(term, all_documents, doc_len = -1):
  ''' Inverse document frequency calculation for term in all documents (all sentences). '''
  # cache the length of the document list
  document_count = len(all_documents) if doc_len == -1 else doc_len
  documents_with_term = len([doc for _,doc in all_documents if term in doc])
  # avoid divide-by-zero errors
  if documents_with_term == 0:
    return 0
  return math.log(document_count / documents_with_term)
