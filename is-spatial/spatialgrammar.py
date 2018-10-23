""" spatial grammar processing code """

import core as core
import nltk

SPATIAL_GRAMMAR_FILEPATH = ''
SPATIAL_GRAMMAR_CATEGORIES = []
def initialise(filepath):
  core.PATHS = core.init_paths(filepath)
  SPATIAL_GRAMMAR_FILEPATH = core.PATHS['SPATIAL_GRAMMAR'][0]
  SPATIAL_GRAMMAR_CATEGORIES = [
      'svs',
      'srv',
      'srq',
      'qtfun',
      'qtf',
      'msr',
      'ls',
      'lmv',
      'dir'
  ]


def tag_all_spatial_grammar(working_list):
    """Returns a tokenlist that with spatial grammar tagged from all categories."""

    # working_list = token_list.copy(True)
    for category in SPATIAL_GRAMMAR_CATEGORIES:
        working_list = tag_spatial_grammar(working_list, category)
    return working_list


def tag_spatial_grammar(token_list, category):
    """Returns a list that has had only a certain category of words tagged."""
    category_words = [x.strip() for x in open(
        SPATIAL_GRAMMAR_FILEPATH + category + ".txt").readlines()]
    category_words.sort(key=len, reverse=True)

    # convert the text into a string to simplify the keyword searches
    flat_word_list = []
    for token in token_list:
        if not isinstance(token, nltk.Tree):
            # append the word to the list.
            flat_word_list.append(token[0])
        else:
            # this token is a tree, put a junk value in so it won't match to anything
            # short for named entity. The shorter the string, performance will probably
            # be a little faster for each evaluation
            flat_word_list.append("N_E")

    concatenated_text = " ".join(flat_word_list)
    # get the indices of the word sequences from the list
    for spatial_word in category_words:
        # only check words that aren't already in tree structures, because those are other entities
        if spatial_word in concatenated_text:
            # now find the word, group it and tag it
            individual_words = spatial_word.split(' ')
            indices = core.get_indices_of_sublist(
                flat_word_list, individual_words)

            # using the indices, convert to tree
            # token_list = token_list.copy(True)
            idx_offset = 0
            for i in indices:
                # create the tree
                new_tree = SpatialGrammarTree(
                    token_list[i - idx_offset: (i - idx_offset) + len(individual_words)], category)

                # replace the matched words with the tree (delete extras, then replace)
                # we don't use the _ variable, but the for loop structure is easier to use
                for _ in range(0, len(individual_words) - 1):
                    # delete n - 1 words, leaving only 1 word for replacing
                    del token_list[i + idx_offset]
                token_list[i] = new_tree

                # update the offset to compensate for the removed items
                idx_offset += len(individual_words) - 1

    return token_list


class SpatialGrammarTree(nltk.Tree):
    """Class to represent a spatial grammar tree."""

    def __init__(self, words, category):
        super(SpatialGrammarTree, self).__init__(
            "SG-%s" % (category.upper()), words)
        self.__class__ = SpatialGrammarTree

    def __str__(self):
        return super(SpatialGrammarTree, self).__str__()
