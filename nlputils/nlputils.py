import click
import dedupe

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
@click.option('--dos-eol', '-n', is_flag=True,
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
@click.argument('flights-file', type=click.File('r'), required=True)
@click.argument('airports-file', type=click.File('r', encoding='utf8'), required=True)
# options
@click.option('--delete-trash', '-d', is_flag=True,
              help='Delete lines with trash. Default process is to try clean them.')
@click.option('--no-header', '-n', is_flag=True,
                help='Exclude the header when processing.')
@click.version_option(version='1.0.0')

def untrash():
  click.echo('untrashed nothing!')
  pass

