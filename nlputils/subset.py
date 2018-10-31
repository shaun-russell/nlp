''' Extract a subset of lines from a file. '''

import random

def extract_n(datalist, number, save_header=True):
  start = 1 if save_header else 0
  subset = []
  if save_header:
    subset.append(datalist[0])
  sample_indices = random.sample(range(start, len(datalist)), number)
  for idx in sample_indices:
    subset.append(datalist[idx])

  return subset
