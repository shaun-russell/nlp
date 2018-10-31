import click
import dedupe
import untrash
import subset

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group()
def cli():
  click.echo('Utils launched.')

# START CLI COMMANDS

@cli.command('dedupe', context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=True)

# options/flags
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
# other required arguments
@click.version_option(version='1.0.0')

def deduplicate(in_file, out_file, no_header, dos_eol):
  ''' Removes duplicates and blanks from a line '''
  all_lines = [line.strip() for line in in_file]
  deduped_lines = dedupe.dedupe(all_lines, no_header)

  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  for line in deduped_lines:
    out_file.write('{}{}'.format(line, eol))
  out_file.close()
  click.echo('Reduced {} lines to {} lines.'.format(len(all_lines), len(deduped_lines)))
  exit()


@cli.command('untrash', context_settings=CONTEXT_SETTINGS)
@click.argument('in_file', type=str, required=True)
@click.argument('out_file', type=click.File('w+', encoding='utf8'), required=True)

@click.option('--encoding', '-e', type=str, default='utf8',
              help='Character encoding. If errors, try a different encoding.')

# options
@click.option('--delete-trash', '-x', is_flag=True,
              help='Delete lines with trash. Default process is to try clean them (but will delete if uncleanable).')
@click.option('--delete-urls', '-u', is_flag=True,
              help='Delete lines that look like urls.')
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
@click.version_option(version='1.0.0')

def run_untrash(in_file, out_file, encoding,
                delete_trash, delete_urls, no_header, dos_eol):
  ''' Fixes or purges lines with shoddy character encoding. ''' 

  # use this rather than list comprehension to avoid repeating the
  # web url check in the processing (since it would do the exact same
  # thing in both loops)
  all_lines = []
  deleted_web_lines = 0
  inputfile = open(in_file, 'r', encoding=encoding)
  if no_header:
    # sneakily read the first line (header) without doing anything
    inputfile.readline()

  for line in inputfile:
    if delete_urls and untrash.has_url(line):
      deleted_web_lines += 1
    else:
      all_lines.append(line.strip())
  
  # notify the user that (cob)web links are gone
  if delete_urls:
    click.echo('Found and deleted {} web-looking lines.'.format(deleted_web_lines))

  # cache these for performance
  total_word_count = len(all_lines)
  word_index = 0
  uncleanable_lines = 0

  cleaned_lines = []
  # skip all lines that fail the trash check
  for line in all_lines:
    if not untrash.is_sentence_trash(line):
      # if not trash, keep
      cleaned_lines.append(line.strip())
    elif not delete_trash:
      # line is trash, but attempt to clean with cleany library
      cleaned = untrash.try_fix_encoding(line)
      if not untrash.is_sentence_trash(cleaned):
        # cleaned!
        cleaned_lines.append(cleaned.strip())
      else:
        # try solve strange microsoft encoding problems
        cleaned = untrash.fix_microsoft_encoding(line)
        if not untrash.is_sentence_trash(cleaned.strip()):
          # cleaned!
          cleaned_lines.append(cleaned.strip())
        else:
          uncleanable_lines += 1

    # else skip it because it's trash

    # print progress so the user knows how long the program will take,
    # but do it periodically because print statements are slow.
    word_index += 1
    if word_index % 10 == 0:
      click.echo('\rProcessed {} lines of {}.'.format(word_index, total_word_count), nl=False)

  # show that we've processed all lines now
  click.echo('\rProcessed {} lines of {}.'.format(total_word_count, total_word_count))

  if delete_trash:
    click.echo('Reduced {} lines to {} lines.'.format(len(all_lines), len(cleaned_lines)))
  else:
    click.echo('Found {} uncleanable lines.'.format(uncleanable_lines))
    click.echo('Reduced {} lines to {} lines.'.format(len(all_lines), len(cleaned_lines)))
  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo('Saving...')
  for line in cleaned_lines:
    out_file.write('{}{}'.format(line.strip(), eol))
  out_file.close()
  click.echo('Done!')
  exit()


@cli.command('subset', context_settings=CONTEXT_SETTINGS)
@click.argument('in_file', type=click.File('r', encoding='utf8'), required=True)
@click.argument('line-count', type=int, required=True)
@click.argument('out_file', type=click.File('w+', encoding='utf8'), required=True)


# options
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.option('--dos-eol', '-d', is_flag=True,
                help='Use \\r\\n dos line endings. Default is UNIX.')
@click.version_option(version='1.0.0')

def run_subset(in_file, line_count, out_file, no_header, dos_eol):
  ''' Creates a subset of lines from a file. ''' 
  in_lines = [x.replace('\r','').replace('\n','') for x in in_file.readlines()]
  click.echo('Extracting...')
  # probably change this to not be a double negative
  sample = subset.extract_n(in_lines, line_count, not no_header)

  # use the correct eol for the system
  eol = '\r\n' if dos_eol else '\n'

  click.echo('Saving...')
  for line in sample:
    out_file.write('{}{}'.format(line.strip(), eol))
  out_file.close()
  click.echo('Done!')
  exit()

