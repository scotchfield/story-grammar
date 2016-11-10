import parser
import re
import sys

def wordCount( st ):
    return len( re.findall( r'\b\w+\b', st ) )

try:
    input_filename = sys.argv[1]
except IndexError:
    print( 'Please pass the input filename as an argument. For example,\n> python parser.py stories/simple.txt book.txt' )
    sys.exit( 1 )

try:
    output_filename = sys.argv[2]
except IndexError:
    print( 'Please pass the output filename as an argument. For example,\n> python parser.py stories/simple.txt book.txt' )
    sys.exit( 1 )

input_file = open( input_filename, 'r' )
story = input_file.read()

output_file = open( output_filename, 'w' )
book = ''

# 52,000 words, since word counts can be inconsistent across programs.
# Let's be generous with our writing, funny program!
while wordCount( book ) < 55000:
    #parser.VERBOSE = True
    ( story_generate, story_lists, story_rules ) = parser.parse( story )
    result = parser.generate( story_generate, story_lists, story_rules, {} )

    book += '\n\n\n' + result

output_file.write( book )
output_file.close()
