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
# @click.option('--evaluate', '-e', is_flag=True,
#               help='Use the second column (1/0) to evaluate accuracy.')

# options/flags
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def cli(in_file, path_file, out_file, #delimiter, evaluate,
         no_header, dos_eol):
  ''' Attempts to evaluate whether or not a line is spatial.
      If evaluating, make sure the columns are tab-separated. Excel can do this.
      NOTE: Not tagging place names because lookup dataset is too big and inefficient.
  '''
  all_lines = [line.strip() for line in in_file]
  click.echo('Found {} lines.'.format(len(all_lines)))
  exit()
  if no_header:
    del all_lines[0]

  # initialise the paths (what a mess lmao)
  core.init_paths(path_file)
  validator.initialise(path_file)

  # store this here so we don't have to re-evaluate len when printing progress
  total_word_count = len(all_lines)
  word_index = 0
  saved_lines = []
  for i,line in enumerate(all_lines):
    try:
      if validator.is_geotext(validator.process_all_text(line, True)):
        saved_lines.append('{}\t{}'.format(line.strip(), 1))
      else:
        saved_lines.append('{}\t{}'.format(line.strip(), 0))
    except:
      click.echo('\nError processing line {}'.format(i))

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 10 == 0:
      click.echo('\rProcessed {} lines out of {}.'.format(word_index, total_word_count), nl=False)

  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo('Saving...')
  # save the words into a tf-idf matrix, tab-separated
  for line in saved_lines:
    out_file.write('{}{}'.format(line, eol))
  out_file.close()
  click.echo('Done!')
