import shlex
import sys


def getFromFile( input_filename ):
    input_file = open(input_filename, 'r')
    return input_file.read().strip().split( '\n' )

def dead( line, st ):
    print( 'ERROR Line ' + str( line ) + ': ' + st )
    sys.exit(1)

def parse( data ):
    story_variables = {}
    story_rules = {}
    story_generate = False

    data = data.split( '\n' )
    in_rule = False
    line_num = 0

    for line in data:
        line_num += 1

        line = line.strip()
        line_tokens = shlex.split( line )

        if len( line_tokens ) == 0:
            in_rule = False
        elif not in_rule:
            if line_tokens[0].lower() == 'use':
                try:
                    story_variables[line_tokens[1]] = getFromFile( line_tokens[2] )
                except IOError:
                    dead( line_num, 'Could not open ' + line_tokens[2] )
            elif line_tokens[0].lower() == 'generate':
                story_generate = line_tokens[1]
                print 'oh yeah ' + story_generate
            else:
                in_rule = line_tokens[0]
                story_rules[in_rule] = []
        else:
            story_rules[in_rule].append( line_tokens )

    return ( story_variables, story_rules, story_generate )

st = '''Use Names "text/firstnames.txt"
Use Adjectives "text/adjectives.txt"
Use Objects "text/objects.txt"

Story
  Introduction Middle End

Introduction
  AtFirst Describe

AtFirst
  "Once upon a time, there was a hero named " Names.Protagonist

Describe
  Names.Protagonist " was a " Adjectives.ProtagonistAdjective " fighter."
  Names.Protagonist "was a " Adjectives.ProtagonistAdjective " warrior."

Middle
  "Then " Names.Protagonist " went for a " Adjectives.ProtagonistAdjective " walk."

End
  "And " Names.Protagonist " died."

Generate Story'''

( story_variables, story_rules, story_generate ) = parse( st )

#print story_variables
#print story_rules
print story_generate
