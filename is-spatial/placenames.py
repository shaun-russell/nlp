""" PLACENAME related code """
import nltk
import core as core
import os.path as path
#from pathlib import Path

# MAKE THIS A BETTER FIXED LOCATION
# PLACENAME_DIRECTORY = "c:/Projects/datasets/cextract"
PLACENAME_DIRECTORY = {'pn': []}
def initialise(filepath):
  core.PATHS = core.init_paths(filepath)
  PLACENAME_DIRECTORY['pn'] = core.PATHS['PLACENAMES'][0]
  print('Initialised placenames.')


def get_country_filename(country_id):
    """Builds a file path for a specific country name."""
    return "%s/%s/%s-acs.tsv" % (PLACENAME_DIRECTORY, country_id.upper(), country_id.upper())


def get_location_names(filepath):
    """Returns a list of lines in the specific file"""
    return [line.strip() for line in open(get_country_filename(filepath)).readlines()]


@DeprecationWarning
def is_placename(name, contextlist, verbose=False):
    """Validates if a string name is a placename in the given list."""

    # progressive binary search
    midpoint = find_placenames_in_list(name.lower(), contextlist, verbose)
    if midpoint < 0:
        return False
    rrange = core.expand_places_from_index(contextlist, midpoint)
    # if len(rrange) > 1:
    #   pass
    #     # print("MULTIPLE ENTRIES FOUND (%s)" % (len(rrange)))
    # for entry in rrange:
    #   pass
        # print(entry)
    return True


def is_placename_az_search(name, verbose=False):
    """Validates a placename if it exists anywhere in the GeoNames dataset."""
    # remove strange errors caused by bad tags
    # print('NAME {}'.format(name))
    if len(name) < 2:
        # print('len exit')
        return False
    (midpoint, contextlist) = find_placename(name.lower(), verbose)
    #print(midpoint, contextlist)
    if midpoint < 0:
        # print('mid exit')
        return False
    # rrange = core.expand_places_from_index(contextlist, midpoint)
    # print('Found?')

    # if len(rrange) > 1:
    #     printer.printy("MULTIPLE ENTRIES FOUND (%s)" % (len(rrange)))
    # for entry in rrange:
    #     printer.printy("\t".join(entry[1:]))

    return True


def tag_all_placenames(working_list, quick_exit, trace=False):
    """Takes a tagged and labels all name entities if they are valid placenames."""
    quick_count = 0

    for i in range(0, len(working_list)):
        if isinstance(working_list[i], core.NameEntityTree):
            #print(working_list[i])
            tree_string = core.convert_tree_to_string(working_list[i])
            if quick_count == 2 and quick_exit:
                #print('qc break')
                break
            # print(s)
            if is_placename_az_search(tree_string, trace):
                working_list[i] = PlacenameTree(working_list[i].leaves())
                # print('placename')
                # for quick validation, exit when two placenames are found
                quick_count += 1

    return working_list



def find_placename(target_name, verbose=False):
    """Binary search for place names. Doesn't need a location as an argument."""
    # Static file paths == BAD, fix this
    filepath = "{}{}/{}.tsv".format(PLACENAME_DIRECTORY['pn'], target_name[:1], target_name[:2])
    # print('FP: {}'.format(filepath))

    # this is important because the path is constructed from the place name
    if not path.exists(filepath):
        # print('no-path')
        return (-1, [])

    datalist = [x.strip()
                for x in open(filepath, encoding='utf8').readlines()]
    length = len(datalist)
    # printer.printy("List length:", length)

    start = 0
    end = length
    mid = -1
    manuallybroken = False

    if target_name in datalist:
      return (99,[])

    # This is just a binary search looking for an initial match.
    # The initial match acts as an anchor that can be searched around.
    while start <= end:
        mid = (start + end) // 2
        # check the mid value so it doesn't break by going out of bounds
        if mid < 0 or mid >= len(datalist):
            return(-1, datalist)

        name_at_idx = datalist[mid][0].lower()
        if name_at_idx == target_name:
            manuallybroken = True
            break
        else:
            if target_name < name_at_idx:
                end = mid - 1
            else:
                start = mid + 1

    if not manuallybroken:
        return (-1, datalist)
    return (mid, datalist)


def find_placenames_in_list(placename, context_list, is_printing=False):
    """ Find placenames in a list. Alternative to alphabetic search if location is known. """

    # This code works, but it's probably far too complicated than it needs to be
    # It starts by finding the first 2 matching characters (for "performance reasons")
    # then it searches linearly up and down looking for the word to match.
    # The alleged performance improvement is likely offset by the linear search.

    # This function isn't really used because the other, non-context placename search
    # is better and doesn't need the location to be specified.

    printer = core.Printer(is_printing)
    start = 0
    end = len(context_list)
    mid = -1

    # This block searches for the first 2 matching characters.
    while start <= end:
        mid = (start + end) // 2
        # make sure we are only accessing values *inside* the list
        if mid < start or mid > end:
            # print('error in mid value? %s (%s)' % (mid, len(context_list)))
            break

        # break if partial match is found
        if context_list[mid].lower()[:2] == placename[:2]:
            break
        # otherwise keep searching
        else:
            if placename[:2] < context_list[mid].lower()[:2]:
                end = mid - 1
            else:
                start = mid + 1
    printer.printy("partial at", mid)

    # Now we have an anchor point, we
    initsplit = context_list[mid].lower().split('\t')
    iteml = placename.lower()
    # the geonames data has the
    printer.printy('do these match? ', iteml, "|", initsplit[0])
    # now investigate the partial match some more
    if iteml == initsplit[0]:
        return mid
    # just look at asciis because that's much simpler
    elif iteml < initsplit[0]:
        printer.printy("searching backwards, because",
                       iteml, "is less than", initsplit[0])
        # item is less, search linearly upwards.
        while mid > 0:
            mid -= 1
            split_item = context_list[mid].lower().split('\t')
            # printer.printysp[1])
            # check if the first 2 letters are no longer equal (no match)
            if split_item[0][:2] != iteml[:2]:
                break
            else:
                if iteml == split_item[0]:
                    return mid

    elif iteml > initsplit[0]:
        printer.printy("searching forwards, because",
                       iteml, "is greater than", initsplit[0])
        while mid < end:
            mid += 1
            # printer.printysp[1])
            split_item = context_list[mid].lower().split('\t')
            # check if the first 2 letters are no longer equal (no match)
            if split_item[0][:2] != iteml[:2]:
                break
            else:
                if iteml == split_item[0]:
                    return mid

    return -1


class PlacenameTree(nltk.Tree):
    """Tree structure to represent a place name."""

    def __init__(self, words):
        super(PlacenameTree, self).__init__("PLN", words)
        # self.__class__ = PlacenameTree

    def __str__(self):
        return super(PlacenameTree, self).__str__()
