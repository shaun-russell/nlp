''' Tool for getting constituency trees from sentences processed with CoreNLP. '''

# Better description of thing.
import click
from pycorenlp import StanfordCoreNLP
from nltk.tree import Tree,ParentedTree
import re

# used to tell Click that -h is shorthand for help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ANNOTATORS = "tokenize,ssplit,pos,lemma,ner,truecase,parse,depparse,relation"
CNLP_PROPS = {'annotators':ANNOTATORS, 'pipelineLanguage': 'en', 'outputFormat': 'json'}

tree_extract_regex = re.compile('(\([A-Z ]*\(.*\)\))')

# individual functions go here
def functo(parpar):
  ''' this function does XYZ. '''
  pass

# classes
class LineData():
  def __init__(self, sentence, annotated_data):
    self.original_text = sentence.strip()

    self.const_tree_str = ''
    if isinstance(annotated_data, str):
      self.const_tree_str = annotated_data
    else:
      self.const_tree_str = annotated_data['sentences'][0]['parse']
    self.const_tree_str_flat = self.const_tree_str.replace('\r\n','').replace('\n','').replace('  ', ' ')

  @staticmethod
  def header(delim='\t'):
    ''' Return the header as a delimited string. '''
    columns = ['sentence', 'constituency tree']
    return delim.join(columns)

  def export(self, delim='\t'):
    ''' Return the data as a delimited string. '''
    return delim.join([self.original_text, self.const_tree_str_flat])


# START CLI COMMANDS
@click.command(context_settings=CONTEXT_SETTINGS)
# required arguments
@click.argument('in-file', type=click.File('r', encoding='utf8'), required=True)
@click.argument('out-file', type=click.File('w+', encoding='utf8'), required=False)

# optional arguments
@click.option('--corenlp', '-c', default='http://localhost:9000',
              help='The url of the CoreNLP Server. Default is localhost:9000.')

# flags
@click.option('--process', '-p', is_flag=True,
              help='Process the line. If no process, program looks in in_file for tree to visualise.')
@click.option('--visualise', '-v', is_flag=True,
              help="Draw each tree as it is processed. DON'T USE WHEN BIG FILE.")
@click.option('--verbose', is_flag=True,
              help='Enables information-dense terminal output.')

# other required arguments
@click.version_option(version='1.0.0')


# main entry point function
def cli(in_file, out_file, corenlp,
        visualise, verbose, process):
  '''
    A description of what this main function does.
  '''
  if process and out_file == None:
    click.echo('Processing requires an output file to save data.')
  nlp = StanfordCoreNLP(corenlp) if process else None
  
  # parse the header for column indexes
  header_line = in_file.readline()
  header = header_line.strip()
  
    
  # use the same line endings as the input
  eol = '\r\n' if '\r' in header_line else '\n'

  # store lines in here
  saved_lines = []
  # append a header
  saved_lines.append(LineData.header())
  
  word_index = 0
  # main operation in here
  for line in in_file:
    tree = ''
    # if processing, get the tree from the corenlp results
    linedata = None
    if nlp != None:
      annotated = nlp.annotate(line.strip(), properties=CNLP_PROPS)
      linedata = LineData(line, annotated)
      tree = linedata.const_tree_str
    else:
      # if not processing, look for tree structure
      try:
        tree = str(tree_extract_regex.search(line).groups()[0])
        linedata = LineData('', tree)
      except:
        click.echo('Tree not found in : {}'.format(line))
    
    if visualise:
      try:
        print(linedata.const_tree_str)
        Tree.fromstring(linedata.const_tree_str_flat).draw()
      except:
        click.echo('Tree could not be parsed or visualised.')

    if process:
      saved_lines.append(linedata.export('\t'))
    # periodic progress updates
    word_index += 1
    if verbose and word_index % 10 == 0:
      click.echo('\rProcessed {}.'.format(word_index), nl=False)
   
  if verbose: click.echo('Saving...')

  # write the matched lines to the output file if processed
  # if not processed, nothing to save
  if process and out_file != None:
    for content in saved_lines:
      # replace content with useful stuff
      out_file.write('{}{}'.format(content, eol))
    out_file.close()

  # finished
  if verbose: click.echo('Saved')