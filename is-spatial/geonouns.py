""" GEONOUN related code """
import nltk
import core as core

GEONOUNS_LIST = []
def initialise(filepath):
  core.PATHS = core.init_paths(filepath)
  GEONOUN_PATH = "total-geowords.txt"
  GEONOUN_DIR = core.PATHS['GEONOUNS'][0]
  # GIVE THIS A FIXED PATH
  GEONOUNS_LIST = [n.strip()
                  for n in open(GEONOUN_DIR + GEONOUN_PATH).readlines()]


def is_geonoun(string):
    """ returns True if the word is found in the geonouns list """
    return string.lower() in GEONOUNS_LIST


def get_all_geonouns(token_list):
    """ Returns all words that match geonouns in a given token list """
    gnwords = []
    for (word, i) in core.get_pos(token_list, 'NN'):
        try:
            if is_geonoun(word):
                result = greedybinary_geonoun_search(token_list, i)
                if result != None:
                    gnwords.append(result)
                else:
                    gnwords.append((word, '%s' % (i)))
            # else:
            #     result = brg_search(tokenlist, i)
            #     if result != None:
            #         gnwords.append(result)
        except:
            print('error processing:', word, i)
    return gnwords


# def tag_geonouns(token_list):
def greedybinary_geonoun_search(wordlist, anchor_idx, search_range=2):
    """Binary extended geonoun search. Checks up to three consecutive words looking for geonouns"""

    listlength = len(wordlist)
    # print(listlength, anchor_idx)

    # some quick evaluations so the algorithm doesn't %  and evaluate words that are in trees
    # e.g. if the previous word is part of a tree, don't combine it and check the geonoun list
    # because it's inefficent and pointless
    check_previous = True
    check_next = True

    if anchor_idx > 0 and wordlist[anchor_idx - 1] is nltk.Tree:
        check_previous = False
    if anchor_idx < listlength - 1 and wordlist[anchor_idx + 1] is nltk.Tree:
        check_next = False

    # extend to word before
    if anchor_idx > 0 and check_previous:
        combinedword = "%s %s" % (
            wordlist[anchor_idx - 1][0], wordlist[anchor_idx][0])
        # print('searching for', combinedword)
        if is_geonoun(combinedword):
            # print('Found.')
            # print(combinedword, 'is a geoword')
            return (combinedword, anchor_idx - 1)

    # extend to word after
    if anchor_idx < listlength - 1 and check_next:
        combinedword = "%s %s" % (
            wordlist[anchor_idx][0], wordlist[anchor_idx + 1][0])
        # print('searching for', combinedword)
        if is_geonoun(combinedword):
            # print('Found.')
            # print(combinedword, 'is a geoword')
            return (combinedword, anchor_idx)

    # extend to words before and after
    # the check next and check previous don't seem to do that muck
    if anchor_idx > 0 and anchor_idx < listlength - 1 and check_next and check_previous:
        combinedword = "%s %s %s" % (wordlist[anchor_idx - 1][0],
                                     wordlist[anchor_idx][0], wordlist[anchor_idx + 1][0])
        if is_geonoun(combinedword):
            return (combinedword, anchor_idx - 1)

    if search_range >= 2:
        # extend to two words ahead
        if anchor_idx < listlength - 2 and check_next:
            combinedword = "%s %s %s" % (
                wordlist[anchor_idx][0], wordlist[anchor_idx + 1][0], wordlist[anchor_idx + 2][0])
            if is_geonoun(combinedword):
                return (combinedword, anchor_idx)

        # extend to two words behind
        if anchor_idx >= 2 and check_previous:
            combinedword = "%s %s %s" % (
                wordlist[anchor_idx][0], wordlist[anchor_idx - 1][0], wordlist[anchor_idx - 2][0])

            if is_geonoun(combinedword):
                return (combinedword, anchor_idx)

    # No broad multi-word matches, just try the single word match now
    if is_geonoun(wordlist[anchor_idx][0]):
        return (wordlist[anchor_idx][0], anchor_idx)

    # reached the end without returning, so return None
    return None


def tag_geonouns(token_list):
    """Changes identified geonouns in the list into GNN trees, returning the modified list."""
    current_idx = 0
    # working_list = token_list.copy(True)
    working_list = []
    while current_idx < len(token_list):
        # print(current_idx, len(token_list))
        if isinstance(token_list[current_idx], nltk.Tree):
            # item is a tree, add and skip
            working_list.append(token_list[current_idx])
        # item is not a tree, therefore it's a tuple and we can look at the pos tag
        elif token_list[current_idx][1].startswith("NN"):
            # From this word index, try find a geonoun around the word
            matched_geonoun = greedybinary_geonoun_search(
                token_list, current_idx)
            if matched_geonoun is None:
                # no match at all, word is not a geonoun
                working_list.append(token_list[current_idx])
            else:
                # match is found, break it into the two parts
                (words, start_idx) = matched_geonoun
                # because the search returns only the joined word and its start_idx
                # we need to split this again to count the number of words it joined.

                # THIS SHOULD BE REFACTORED AT SOME POINT, THE ALGORITHM SHOULDN'T DO FORMATTING
                num_words_in_match = len(words.split(' '))

                # cleaner to make this its own line
                end_idx = start_idx + num_words_in_match
                # merge the lines into a
                working_list.append(GeonounTree(
                    token_list[start_idx]))
                # apply any additional offset
                current_idx += (num_words_in_match - 1)
        else:
            working_list.append(token_list[current_idx])
        current_idx += 1

    # return it as a sentence tree, seeing as a new list was made and the tgc %  is an S-tree
    return nltk.Tree("S", working_list)

# short hand


def gagn(tokenlist):
    """Shorthand for get_all_geonouns(). Meant for quick experiments in the console
    so I don't have to write these long function names with underscores"""
    return get_all_geonouns(tokenlist)


class GeonounTree(nltk.Tree):
    """A type of tree specifically for GeoNouns. Makes it easy to apply and differentiate them"""

    def __init__(self, words):
        super(GeonounTree, self).__init__("GNN", words)
        # self.__class__ = GeonounTree

    def __str__(self):
        return super(GeonounTree, self).__str__()
