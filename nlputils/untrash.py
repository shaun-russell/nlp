''' Functions to find and clean trash lines. '''

# character encoding fixing library
import ftfy

# characters after this are unlikely to be in normal English sentences
# Sentences in languages like French or Spanish will be marked as trash
# however, because these contain, though intentionally, special chars
# that are also seen when character encodings aren't read properly.
UPPER_LIMIT_CHAR = '¥'

def is_sentence_trash(sentence):
  ''' Returns True if the sentence contains non-ASCII looking characters. '''
  for character in sentence:
    if character > UPPER_LIMIT_CHAR:
      return True
  return False

def try_fix_encoding(sentence):
  ''' Attempt to fix the encoding and return nice text. '''
  return ftfy.fix_text(sentence)

def unmicrosoft_encoding(sentence):
  # microsoft have their own 1-byte encoding
  try:
    cleano = sentence.encode('cp1252').decode('utf8')
    return cleano
  except:
    return sentence

def has_url(sentence):
  ''' Returns True if sentence looks suspiciously like a url. '''
  if 'www' in sentence:
    return True
  elif 'http' in sentence:
    return True
  # passed the basic checks, probably not a url
  return False
