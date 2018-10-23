"""UTILITIES and ALIASES  functions for commonly used nltk functions."""
import nltk
import os

# SHORTHAND FUNCTIONS (ALIASES FOR NLTK)

# initialise paths
PATHS = {}
GEOCODES = []
def init_paths(path_file):
  PATHFILE = [x.strip() for x in path_file]
  PATHS = dict(
      GEONOUNS=[x.split(':')[1] for x in PATHFILE if x.startswith('GEONOUN')],
      SPATIAL_GRAMMAR=[x.split(':')[1]
                      for x in PATHFILE if x.startswith('SPATIAL')],
      PLACENAMES=[x.split(':')[1] for x in PATHFILE if x.startswith('PLACE')],
      CODEREF=[x.split(':')[1] for x in PATHFILE if x.startswith('CODE')]
  )

  GEONAMES_CODE_REFERENCE_PATH = PATHS['CODEREF'][0] + "coderef.txt"
  GEOCODES = [getcode(x) for x in open(
      GEONAMES_CODE_REFERENCE_PATH, 'r').readlines()]
  return PATHS



def getsent(text):
    """tokenize text into sentences."""
    return nltk.tokenize.sent_tokenize(text)


def tokenize(text):
    """tokenize a sentence into individual words."""
    return nltk.word_tokenize(text)


def tag(token_list):
    """using a list of word tokens, tag these as parts of speech."""
    return nltk.pos_tag(token_list)


def chunk(word_list, is_binary):
    """apply the standford NE chunking to a pos-tagged list of words."""
    return nltk.ne_chunk(word_list, binary=is_binary)


def ttg(text):
    """tokenize and tag a string."""
    return tag(tokenize(text))


def tgc(text):
    """tokenize, tag, and stanford ne-chunk a string."""
    return chunk(tag(tokenize(text)), True)


# UTILITIES
def get_pos(tokenlist, pos):
    """ filter a list to return the words that match the provided part of speech"""
    matching_pos_words = []
    i = 0
    for (word, pos_tag) in tokenlist:
        try:
            if pos_tag.startswith(pos):
                matching_pos_words.append((word, i))
        except:
            print('error', word, pos_tag)
        i += 1
    return matching_pos_words


def getcode(line):
    """ Extract out the Geonames reference code for searching. """
    split_line = line.split('\t')
    head = split_line[0][2:]
    desc = split_line[1]
    return (head, desc)



def define(searchcode):
    """ Print the definition of a specific Geonames reference code."""
    print([head + ": " + desc for (head, desc) in GEOCODES if head == searchcode])


def create_tree(tuples, verbose=False):
    """ Converts a list of tuples into a tree."""
    printer = Printer(verbose)
    printer.printy(tuples)

    tree = nltk.Tree('NE', tuples)

    printer.printy(tree)
    return tree


def is_tree(obj):
    """If the item is a tree (base class nltk.tree), return true."""
    return isinstance(obj, nltk.Tree)
    # except:
    #     print('error evaluating if object %s is nltk.Tree' % (obj))
    #     return False


def get_indices_of_sublist(main_list, sublist):
    """Like .index() on a string, but as a list. e.g. returns the index of [3,4] in [1,2,3,4,5].
       Finds all indices in a list in case there are duplicates."""
    indices = []
    for i in range(0, len(main_list)):
        item = main_list[i]
        # if the first word of the sublist matches the current word, and the search will not
        # exceed the bounds of the list, then evaluate the sequence of words in the sublist
        if item == sublist[0] and i + len(sublist) < len(main_list):
            matches_all = True
            # e.g. [0]==[5], [1]==[6], [2]==[7]
            # If a match is incorrect at any stage, stop evaluating
            for j in range(0, len(sublist)):
                if sublist[0 + j] != main_list[i + j]:
                    matches_all = False
                    break
            if matches_all:
                # perfect match, save the index
                indices.append(i)
                # skip the current index ahead
                i += len(sublist) - 1

    return indices


def convert_tree(tree, new_type, extra_tag=None):
    """ Replace a tree with a tree of another type (a derived tree). """
    leaves = tree.leaves()
    if extra_tag is None:
        return new_type(leaves)
    return new_type(leaves, extra_tag)


def convert_tree_to_string(ne_tree):
    """Converts a tree into a string"""
    return " ".join([w[0] for w in ne_tree])


class Printer():
    """ Wrapper class for printing. Removes if statements and blocking functions from main code."""

    def __init__(self, is_printing=True):
        """init"""
        self.is_printing = is_printing

    def enable(self):
        """ Enables printing."""
        self.is_printing = True

    def disable(self):
        """ Disables printing. """
        self.is_printing = False

    def set_printing(self, is_printing):
        """ Set printing using a boolean."""
        self.is_printing = is_printing

    def printy(self, *args):
        """ If printing is enabled, this will print. """
        if self.is_printing:
            print(args)

# _______________________
# Data Structures

# SHOULD THESE TREE STRUCTURES GO INTO THEIR OWN FILE?


class NameEntityTree(nltk.Tree):
    """Generic name entity tree used to differentiate from the base tree."""

    def __init__(self, leaves):
        super(NameEntityTree, self).__init__("_NE", leaves)
        # self.__class__ = NameEntityTree

    def __str__(self):
        return super(NameEntityTree, self).__str__()


# ______________________________________
# Algorithms

# CURRENTLY UNUSED normalisation functions
def fuzzy_normalize(tagged):
    """ Capitalise words if they are nouns. """
    return tgc(" ".join([w.capitalize() if t in ["NN", "NNS"]
                         else w for (w, t) in tagged]))


def fuzzy_normalize_greedy(tagged):
    """ Capitalise words in a very greedy fashion. """
    normalized_list = []

    for (word, pos_tag) in tagged:
        if pos_tag == "NN" or pos_tag == "NNS" or pos_tag == "NNP":
            # capitalise to proper noun
            capword = word.capitalize()
            normalized_list.append(capword)

            # is the new NNP preceded by an adjective?
            i = normalized_list.index(capword)
            if i > 0:
                # check previous word tag
                if tagged[i - 1][1] == "JJ":
                    print('JJ found at:', i)
                    jjword = normalized_list[i - 1]
                    normalized_list[i - 1] = jjword.capitalize()
        else:
            normalized_list.append(word)  # add without modification

    return tgc(" ".join(normalized_list))


def expand_places_from_index(placename_list, idx):
    """Searches up and down from the index, collecting places with the same name."""
    if idx == -1:
        return []

    # Find and save the initial value
    word = placename_list[idx][0]
    matched_places = []
    matched_places.append(placename_list[idx])

    # Search forward in the list (downwards)
    i = idx - 1
    while placename_list[i][0] == word and i > 0:
        matched_places.append(placename_list[i])
        i -= 1

    # Search backward in the list (upwards)
    i = idx + 1
    length = len(placename_list)
    while placename_list[i][0] == word and i < length:
        matched_places.append(placename_list[i])
        i += 1

    return matched_places


def ne_group_extended(tagged_text, verbose=False):
    """ Pretty sure this is the current name entity chunking algorithm."""
    printer = Printer(verbose)
    try:
        all_ne_groups = []
        current_ne_group = []
        group_idx = -1

        for i, word in enumerate(tagged_text):
            if not is_tree(word):
                # word is a regular tuple, not an NE tree
                name, pos_tag = word
                if pos_tag == 'NNP' or pos_tag == 'NNPS':
                    # it's a proper noun, append it to the current chunk.
                    if group_idx == -1:
                        group_idx = i
                    current_ne_group.append((group_idx, word))

                # match regular nouns if they are capitalised
                elif (pos_tag == "NNS" or pos_tag == 'NN') and name[0] < 'a':
                    if group_idx == -1:
                        group_idx = i
                    current_ne_group.append((group_idx, word))

                # match verbs if they are capitalised
                elif pos_tag == 'VBG' and name[0] < 'a':
                    if group_idx == -1:
                        group_idx = i
                    current_ne_group.append((group_idx, word))

                else:
                    # this is its own variable because pylint says len shouldn't be in a conditional
                    current_group_len = len(current_ne_group)

                    # add definite articles ('the') if there are already words in a group
                    # would match Bob the Bear as a named entity, but not the Bear
                    # maybe add some check to see if it's capitalised and not the first word,
                    # because there would be a lot of place names called 'The XYZ'
                    if pos_tag == 'DT' and current_group_len > 0:
                        current_ne_group.append((group_idx, word))
                    # also insert 'of's into the group for matches like 'Cape of Death'
                    elif name.lower() == 'of' and current_group_len > 0:
                        current_ne_group.append((group_idx, word))
                    else:
                        # not a match, stop grouping and save the current group
                        if current_group_len > 0:
                            all_ne_groups.append(current_ne_group.copy())
                        current_ne_group = []
                        group_idx = -1
            else:
                # word is an NE tree
                current_group_len = len(current_ne_group)
                if current_group_len > 0:
                    # merge named entities if already building one
                    current_ne_group += [(group_idx, (a, b))
                                         for (a, b) in word.leaves()]  # join lists
                continue
        # complete the final chunk, if one exists
        current_group_len = len(current_ne_group)
        if current_group_len > 0:
            all_ne_groups.append(current_ne_group.copy())
            current_ne_group = []

        idx_offset = 0
        for group in all_ne_groups:
            printer.printy(group)
        # Don't think this copy() is necessary, because the value is already copied when
        # passed as an argument to this function
        # However, it's not harming anything so it can stay for now
        newsentence = tagged_text.copy(True)

        for group in all_ne_groups:
            startpos = group[0][0]
            wordnum = len(group)

            # Clear out the words that are grouped in a tree.
            # num - 1 because one of the words is replaced with the new tree, rather than inserted
            for i in range(wordnum):
                del newsentence[startpos - idx_offset]

            tree = create_tree([t[1] for t in group])
            newsentence.insert(startpos - idx_offset, tree)
            idx_offset += (wordnum - 1)

        # We want to convert the generic, base-class NE trees to NameEntityTree types
        # This is so we can differentiate class instances in other parts of the program
        for i in range(0, len(newsentence)):
            if is_tree(newsentence[i]):
                newsentence[i] = NameEntityTree(newsentence[i].leaves())

        return newsentence

    # this shouldn't really be a catch-all; I should know what error would actually be thrown
    # should write tests
    except Exception as exception:
      pass
        # print('Name Entity Grouping Failed:', exception)
