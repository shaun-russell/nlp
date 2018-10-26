import click
import validator
import core
import sys

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r', encoding='utf8'), required=True)
@click.argument('path-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

# @click.option('--delimiter', '-m', type=str, default='\t',
#               help='The delimiter to split evaluation columns on. Default is TAB. Only needed when evaluating.')
@click.option('--geonouns', '-g', type=int, default=2,
              help='Specify how many geonouns are needed to find a match. Default is 2.')
@click.option('--placenames', '-p', is_flag=True,
              help='Use placenames in spatial classification process.')
@click.option('--save-errors', '-s', is_flag=True,
              help='Save errors in a file called errors.txt.')

# options/flags
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def cli(in_file, path_file, out_file, geonouns, placenames,
         no_header, dos_eol, save_errors):
  ''' Attempts to evaluate whether or not a line is spatial.
      If evaluating, make sure the columns are tab-separated. Excel can do this.
      NOTE: Not tagging place names because lookup dataset is too big and inefficient.
  '''
  all_lines = [line.strip() for line in in_file]
  click.echo('Found {} lines.'.format(len(all_lines)))
  if no_header:
    del all_lines[0]

  # initialise the paths (what a mess lmao)
  core.init_paths(path_file)
  validator.initialise(path_file, placenames)

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_lines)
  word_index = 0
  saved_lines = []
  saved_lines.append('sentence\tactual\talgorithm')

  error_lines = []
  for i,line in enumerate(all_lines):
    try:
      if validator.is_geotext(validator.process_all_text(line, True, placenames), geonouns, placenames):
        saved_lines.append('{}\t{}'.format(line.strip(), 1))
      else:
        saved_lines.append('{}\t{}'.format(line.strip(), 0))
    except:
      error_lines.append(line)

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 50 == 0:
      click.echo('\rProcessed {} lines out of {}.'.format(word_index, total_word_count), nl=False)

  click.echo('\nProcessing failed in {} lines.'.format(len(error_lines)))
  if save_errors:
    try:
      click.echo('Saving errors...')
      open('errors.txt', 'w+', encoding='utf8').writelines([l.strip() for l in error_lines])
      click.echo('Saved errors')

    except:
      click.echo('Error saving errors.txt')

  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo('Saving...')
  # save the words into a tf-idf matrix, tab-separated
  for line in saved_lines:
    out_file.write('{}{}'.format(line, eol))
  out_file.close()
  click.echo('Done!')
