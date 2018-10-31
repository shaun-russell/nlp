''' PPMI functions. '''

import math

# ppmi = Positive Point-wise Mutual Information.
#         This is the same as PMI, but with negative values replaced with zero.

# I was just looking at the paper that explains PPMI and I see if we follow what it says then we would get something different from what I was suggesting. But it depends how “context” is interpreted. If we treat each sentence as a context then:
# t_ij | occurences_in_sentence = number of times word i occurs in sentence j / normalisation sum
# p_i | total_occurences = the sum of occurrences of word i in all sentences / normalisation sum
# p_j | total_sentence_length = sum of occurrences of all words in sentence / normalisation sum
# normalisation sum = sum of occurrences of all words in all sentences
# pmi_ij = log(t_ij / (p_i . p_j))
# ppmi_ij = pmi_ij if pmi_ij is > 0
# otherwise 0


def total_occurences(word, all_sentences):
  total_occurences = 0
  for _,sent in all_sentences:
    total_occurences += len([w for w in sent if w == word])
  return total_occurences


def get_normalisation_sum(all_sentences):
  total_words = 0
  for sent in all_sentences:
    total_words += len([w for w in sent])
  return total_words

def pmi(word, sentence, all_sentences, norm_sum, total_occurences):
  # don't process anything if the end result will be 0
  if total_occurences == 0:
    return 0

  # number of times the word appears in the sentence
  occurences_in_sentence = len([w for w in sentence if w == word]) / norm_sum
  # all occurences of the word in all sentences
  total_occurences = total_occurences / norm_sum
  # number of words in the sentence
  total_sentence_length = len(sentence) / norm_sum

  value = occurences_in_sentence / (total_occurences * total_sentence_length)
  # must do this to avoid math domain error
  if value <= 0:
    return 0
  pmi_value = math.log(value)
  return pmi_value

def positive_pmi(word, sentence, all_sentences, norm_sum, total_occurences):
  pmi_value = pmi(word, sentence, all_sentences, norm_sum, total_occurences)
  if pmi_value > 0:
    return pmi_value
  else:
    return 0

