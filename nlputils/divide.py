''' Extract all subsets of lines of N size from a file. '''


def segment(datalist, number, save_header=True):
  all_subsets = [[]]
  if save_header:
    all_subsets[0].append(list[0])

  subset_idx = 0
  start = 1 if save_header else 0
  for i in range(start, len(datalist)):
    all_subsets[subset_idx].append(datalist[i])
  
    # COMPLETE THIS (found out there was a unix command called 'split' so I use that instead)

  return all_subsets
