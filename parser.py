import random
import shlex
import sys


VERBOSE = False

def getFromFile( input_filename ):
    input_file = open(input_filename, 'r')
    return input_file.read().strip().split( '\n' )

def dead( st, line=False ):
    line_st = ''

    if line is not False:
        line_st = ' Line ' + str( line )

    print( 'SORRY' + line_st + ': ' + st )

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
                    dead( 'Could not open ' + line_tokens[2], line_num )
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
    var_id = False
    if len( token_obj ) > 1:
        var_id = token_obj[1]

    if var_list not in lists:
        dead( 'Attempted to use a list that does not exist (' + var_list + ')' )

    if var_id is False:
        return random.choice( lists[var_list] )

    if var_list not in variables:
        variables[var_list] = {}

    if var_id not in variables[var_list]:
        variables[var_list][var_id] = random.choice( lists[var_list] )
        if VERBOSE:
            print 'Setting ' + var_id + ' (' + var_list + ') to value ' + variables[var_list][var_id]

    return variables[var_list][var_id]

def generate( source, lists, rules, variables ):
    if VERBOSE:
        print( 'Starting rule: ' + str( source ) )

    while unusedCount( source ) > 0:
        result = []

        for token in source:
            if not unusedToken( token ):
                result.append( token )
            elif isVariable( token ):
                result.append( '"' + getVariable( token, variables, lists ) + '"' )
            else:
                try:
                    result.extend( random.choice( rules[token] ) )
                except KeyError:
                    dead( 'Could not find rule ' + token + ' when generating. Please make sure this rule is defined.' )
                except IndexError:
                    dead( 'Could not choose a replacement rule, is ' + token + ' empty?' )

        source = result

    source = [ s.replace( '"', '' ) for s in source ]
    source = filter( None, source )

    return ''.join( source )


if __name__ == "__main__":
    try:
        input_filename = sys.argv[1]
    except IndexError:
        dead( 'Please pass the filename as an argument. For example,\n> python parser.py stories/simple.txt' )
    input_file = open( input_filename, 'r' )
    story = input_file.read()

    ( story_generate, story_lists, story_rules ) = parse( story )
    result = generate( story_generate, story_lists, story_rules, {} )

    print( result )
