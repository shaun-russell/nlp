import nltk

punctuation = [',','.',':',';','*', ')','(','|','{','}','0','1',"'",'-','[',']']
def get_most_frequent_n(wordlist, number):
  text = ' '.join(wordlist)
  all_words = nltk.tokenize.word_tokenize(text)
  distribution = nltk.FreqDist(w.lower() for w in all_words if w not in punctuation)
  print(distribution.most_common(1))
  return distribution.most_common(number)