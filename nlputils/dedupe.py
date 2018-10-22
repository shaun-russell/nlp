''' Functions to remove duplicates and empty lines from text files. '''

def dedupe(all_lines, skip_header):
  deduped_lines = []
  # list(set(x)) gets all unique lines
  if skip_header:
    deduped_lines = list(set(all_lines[1:]))
  else:
    deduped_lines = list(set(all_lines))
  # remove any blank lines (other junk line features can be added)
  try:
    del deduped_lines[deduped_lines.index('')]
  except:
    # i guess no junk lines in that set
    pass

  # return the list instead of parsing the file
  return deduped_lines

