import random
import shlex
import sys


def getFromFile( input_filename ):
    input_file = open(input_filename, 'r')
    return input_file.read().strip().split( '\n' )

def dead( line, st ):
    print( 'ERROR Line ' + str( line ) + ': ' + st )
    sys.exit(1)

def parse( data ):
    story_lists = {}
    story_rules = {}
    story_generate = []

    data = data.split( '\n' )
    in_rule = False
    line_num = 0

    for line in data:
        line_num += 1

        line = line.strip()
        line_tokens = shlex.split( line, posix=False )

        if len( line_tokens ) == 0:
            in_rule = False
        elif not in_rule:
            if line_tokens[0].lower() == 'use':
                try:
                    story_lists[line_tokens[1]] = getFromFile( line_tokens[2] )
                except IOError:
                    dead( line_num, 'Could not open ' + line_tokens[2] )
            elif line_tokens[0].lower() == 'generate':
                story_generate = line_tokens[1:]
            else:
                in_rule = line_tokens[0]
                story_rules[in_rule] = []
        else:
            story_rules[in_rule].append( line_tokens )

    return ( story_generate, story_lists, story_rules )

def unusedToken( token ):
    if len( token ) > 0 and token[0] != '"':
        return True

    return False

def unusedCount( rule ):
    count = 0

    for token in rule:
        if unusedToken( token ):
            count += 1

    return count

def isVariable( token ):
    return token.find( '.' ) > -1

def getVariable( token, variables, lists ):
    token_obj = token.split( '.' )

    var_list = token_obj[0]
    var_id = token_obj[1]

    if var_id not in variables:
        variables[var_id] = random.choice( lists[var_list] )

    return variables[var_id]

def generate( source, lists, rules, variables ):
    print( 'Starting rule: ' + str( source ) )

    while unusedCount( source ) > 0:
        result = []

        for token in source:
            if not unusedToken( token ):
                result.append( token )
            elif isVariable( token ):
                result.append( '"' + getVariable( token, variables, lists ) + '"' )
            else:
                result.extend( random.choice( rules[token] ) )

        source = result

    source = [ s.replace( '"', '' ) for s in source ]
    source = filter( None, source )

    return ''.join( source )


st = '''
Use Names text/firstnames.txt
Use Adjectives text/adjectives.txt
Use Objects text/objects.txt

Story
  Introduction Middle End

Introduction
  AtFirst Describe

AtFirst
  "Once upon a time, there was a hero named " Names.Protagonist ". "

Describe
  Names.Protagonist " was a " Adjectives.ProtagonistAdjective " fighter. "
  Names.Protagonist " was a " Adjectives.ProtagonistAdjective " warrior. "

Middle
  "Then " Names.Protagonist " went for a " Adjectives.ProtagonistAdjective " walk. "

End
  "And " Names.Protagonist " died. "

Generate Story'''


( story_generate, story_lists, story_rules ) = parse( st )
result = generate( story_generate, story_lists, story_rules, {} )

print( result )
