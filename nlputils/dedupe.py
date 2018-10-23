''' Functions to remove duplicates and empty lines from text files. '''

def dedupe(all_lines, skip_header):
  uniques = []
  for line in all_lines:
    if line not in uniques and line != '':
      uniques.append(line)
    
  if skip_header:
    return uniques[1:]
  return uniques

