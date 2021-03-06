""" High level functions for web interface type stuff """

# import placenames as pn
# import geonouns as gn
# import spatialgrammar as sg
# import core as core

import placenames as pn
import geonouns as gn
import spatialgrammar as sg
import core as core

def initialise(filepath, placenames = False):
  if placenames:
    filepath.seek(0)
    pn.initialise(filepath)
  filepath.seek(0)
  gn.initialise(filepath)
  filepath.seek(0)
  sg.initialise(filepath)
  filepath.seek(0)

def process_all_text(text_string, quick=False, use_placenames=False):
    """Takes a string, tags all named entities, geofeatures, place names and spatial grammar"""
    # print("Preliminary tagging...")
    token_list = core.tgc(text_string)
    # print("Name Entity chunking...")
    token_list = core.ne_group_extended(token_list)
    # for x in token_list:
    #     print(type(x), x)
    if use_placenames:
      # print("Tagging Place Names...")
      token_list = pn.tag_all_placenames(token_list, quick)
    # print("Tagging Geo Features...")
    token_list = gn.tag_geonouns(token_list)
    # print("Tagging Spatial Grammar...")
    token_list = sg.tag_all_spatial_grammar(token_list)
    # print("Done")
    # print(token_list)
    return token_list


def is_geotext(token_list, gnn_requirement, use_placenames):
    """Determines if a sentence contains the components to be identified as geographic text"""
    num_of_placenames = len(
        [x for x in token_list if isinstance(x, pn.PlacenameTree)])
    num_of_geonouns = len(
        [x for x in token_list if isinstance(x, gn.GeonounTree)])
    num_of_spatial_grammar = len(
        [x for x in token_list if isinstance(x, sg.SpatialGrammarTree)])

    # Needs at least one placename (relatum) and at least two locations in total
    # Also needs at least 1 spatial grammar word.
    if num_of_spatial_grammar >= 1:
      if use_placenames:
        # require at least 2 geonouns or placenames
        if num_of_geonouns + num_of_placenames >= 2:
          return True
      else:
        if num_of_geonouns >= gnn_requirement:
          return True

    return False
