import os, profile, re
import mediator, sr_interface, vc_globals


def dictate_pseudo_python():
    
    #
    # These words must be in the SR vocab, otherwise some of the say()
    # statements will faile
    #
    sr_interface.addWord(sr_interface.vocabulary_entry('aliases', 'aliases'))
    sr_interface.addWord(sr_interface.vocabulary_entry('globals', 'globals'))

    mediator.open_file('D:/blah.py')
        
    mediator.say(['import', 'modules', 'O.', 'S.', ', \\comma', 'R.', 'E.', ', \\comma', 'string', ', \\comma', 'system', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['import', 'modules', 'auto', 'test', ', \\comma', 'natural', 'link', ', \\comma', 'V.', 'C.', 'globals', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)

   
    mediator.say(['from', 'module', 'actions', 'C.', 'C.', 'P.', 'P.', ' import all\\import all', 'new', 'statement'] , user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['from', 'module', 'application', 'state', 'import', 'symbols', 'application', 'state', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['from', 'module', 'context', 'generic', 'import', 'symbols', 'context', 'C.', 'comma', 'context', 'python', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['from', 'module', 'context', 'sensitive', 'command', 'import', 'symbols', 'context', 'sensitive', 'command', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['from', 'module', 'Ed', 'simulator', 'import', 'symbol', 'Ed', 'simulator', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['from', 'module', 'object', 'import', 'symbol', 'object', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['import', 'modules', 'Ed', 'simulator', 'comma', 'symbol', 'dictionary', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['import', 'module',  'S.', 'R.', 'interface',  'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['define', 'class', 'command', 'interpreter', 'sub class\\sub class', 'of', 'object', 'class', 'body'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['define', 'method', 'initialize', 'add', 'argument', 'on', 'application', 'equals', 'none', 'comma'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['symbol', 'dictionary', 'pickle', 'file', 'equals', 'none', 'comma', 'double', 'asterisk', 'attributes', 'method', 'body'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['self', 'dot', 'declare', 'attributes', 'with', 'arguments', 'brace', 'pair'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes', 'un', 'translated', 'text', 'start', 'jump', 'out', ':\\colon', 'none', 'comma'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes', 'un', 'translated', 'text', 'end', 'jump', 'out', ':\\colon', 'none', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['self', 'dot', 'deep', 'construct', 'with', 'arguments', 'command', 'interpreter', 'comma', 'continue', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['brace', 'pair', 'single', 'quotes', 'on', 'application', 'jump', 'out', ':\\colon', 'on', 'application', 'comma',], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes', 'known', 'symbols', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'dot', 'symbol', 'dictionary', 'without', 'arguments', 'comma', 'continue', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    
    mediator.say(['single', 'quotes', 'language', 'specific', 'aliases', 'jump', 'out', ':\\colon', 'empty', 'dictionary', 'comma', 'continue', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes', 'last', 'loaded', 'language', 'jump', 'out', ':\\colon', 'none', 'comma', 'continue', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', 'comma', 'continue', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['attributes', 'new', 'statement', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    
    mediator.say(['define', 'method', 'spoken', 'form', 'regular', 'expression', 'add', 'argument', 'spoken', 'form', 'method', 'body'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['words', 'equals', 'R.', 'E.', 'dot', 'split', 'with', 'arguments'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['single', 'quotes',  'back', 'slash', 'S.', 'plus', 'sign', 'jump', 'out', 'comma', 'spoken', 'form', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['regular', 'expression', 'equals', 'empty', 'single', 'quotes', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['for', 'loop', 'a', 'word', 'in', 'list', 'words', 'loop', 'body'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['first', 'equals', 'a', 'word', 'at', 'index', '0', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['rest', 'equals', 'a', 'word', 'at', 'index', '1', ':\\colon', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['regular', 'expression', 'this', 'word', 'equals', 'single', 'quotes'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['open', 'bracket', 'jump', 'out', 'plus', 'string', 'dot', 'lower', 'with', 'arguments', 'first'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['jump', 'out', 'plus', 'string', 'dot', 'upper', 'with', 'arguments', 'first', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['if', 'statement', 'not', 'regular', 'expression', 'equal', 'to', 'empty', 'single', 'quotes', 'if', 'body'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'single', 'quotes', 'back', 'slash', 'S.', 'asterisk', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'regular', 'expression', 'this', 'word', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)
    
    mediator.say(['return', 'regular', 'expression', 'new', 'statement'], user_input='1\n1\n1\n1\n1\n1\n1\n', echo_utterance=1)

##### Moved to test_punctuation
#  #    mediator.say(['variable', ' \\blank space', ' = \\equals', ' \\space bar', 'index', '*\\asterisk', '2', '**\\double asterisk', '8', '\n\\newline'], user_input='1\n2\n1\n1\n1\n1\n1\n', echo_utterance=1)

#      mediator.say(['variable', ' = \\equals', 'variable', '/\\slash', '2', '+\\plus sign', '1', '-\\minus sign', 'index', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['variable', ' = \\equals', 'index', '%\\percent', '2', ' + \\plus', 'index', '%\\percent sign', '3', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['if', 'index', '&\\and percent', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['if', 'index', '|\\pipe', 'variable', '|\\pipe sign', 'index', '|\\vertical bar', 'value', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['index', ' = \\equals', '0', ';\\semicolon', 'variable', ' = \\equals', '0', ';\\semi', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['index', '.\\dot', 'function', '()\\without arguments', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['variable', ' = \\equals', 'new', 'list', '0', '...\\ellipsis', '10', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['#\\pound', '!\\bang', 'python', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['#\\pound sign', '!\\exclamation mark', 'python', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['if', '~\\tilde', 'index', 'and', '~\\squiggle', 'variable', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['variable', '::\\double colon', 'index', '::\\colon colon', 'field', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['if', 'index', '<\\less sign', '0', ' and \\and', 'index', '>\\greater sign', '-\\minus sign', '1', 'then'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['index', '=\\equal sign', '0', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['function', '(\\open paren', '0', ')\\close paren', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['function', 'parens', '0', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['function', '()\\empty parens', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['list', '[\\open bracket', '0', ']\\close bracket', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['list', 'brackets', '0', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['list', '[]\\empty brackets', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    


#  ## BUG: causes recognitionMimic error    
#  ##    mediator.say(['dictionary', '{\\open brace', '0', '}\\close brace', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['dictionary', 'braces', '0', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#  ## BUG: causes recognitionMimic error
#  ##    mediator.say(['dictionary', '{}\\empty braces', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['<\\open angled', 'head', '>\\close angled', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['angled brackets', 'head', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['<>\\empty angled', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
#      mediator.say(['string', ' = \\equals', '\'\\open single quote', 'message', '\'\\close single quote', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['string', ' = \\equals', 'single', 'quotes', 'message', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['\'\'\\empty single quotes', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['string', ' = \\equals', '\"\\open quote', 'message', '\"\\close quote', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['string', ' = \\equals', 'quotes', 'message', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['""\\empty quotes', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['string', ' = \\equals', '`\\open back quote', 'message', '`\\close back quote', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['string', ' = \\equals', 'back', 'quotes', 'message', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['``\\empty back quotes', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['\\a\\back slash a.', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\a\\back slash alpha', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\b\\back slash b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\b\\back slash bravo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\c\\back slash c.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\c\\back slash charlie'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\d\\back slash d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\d\\back slash delta'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\e\\back slash e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\e\\back slash echo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\f\\back slash f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\f\\back slash foxtrot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\g\\back slash g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\g\\back slash golf'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\h\\back slash h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\h\\back slash hotel'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\i\\back slash i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\i\\back slash india'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\j\\back slash j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\j\\back slash juliett'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\k\\back slash k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\k\\back slash kilo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\l\\back slash l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\l\\back slash lima'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\m\\back slash m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\m\\back slash mike'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\n\\back slash n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\n\\back slash november'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\o\\back slash o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\o\\back slash oscar'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\p\\back slash p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\p\\back slash papa'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\q\\back slash q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\q\\back slash quebec'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\r\\back slash r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\r\\back slash romeo'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\s\\back slash s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\s\\back slash sierra'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\t\\back slash t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\t\\back slash tango'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\u\\back slash u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\u\\back slash uniform'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\v\\back slash v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\v\\back slash victor'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\w\\back slash w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\w\\back slash whiskey'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\x\\back slash x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\x\\back slash xray'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\y\\back slash y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\y\\back slash yankee'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\z\\back slash z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\z\\back slash zulu'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\A\\back slash cap a.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\A\\back slash cap alpha', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\B\\back slash cap b.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\B\\back slash cap bravo', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#  #BUG:    mediator.say(['quotes', '\\C\\back slash cap c.', '\\C\\back slash cap charlie', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\D\\back slash cap d.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\D\\back slash cap delta', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\E\\back slash cap e.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\E\\back slash cap echo', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\F\\back slash cap f.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\F\\back slash cap foxtrot', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\G\\back slash cap g.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\G\\back slash cap golf', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\H\\back slash cap h.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\H\\back slash cap hotel', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\I\\back slash cap i.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\I\\back slash cap india', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\J\\back slash cap j.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\J\\back slash cap juliett', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\K\\back slash cap k.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\K\\back slash cap kilo', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\L\\back slash cap l.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\L\\back slash cap lima', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\M\\back slash cap m.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\M\\back slash cap mike', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\N\\back slash cap n.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\N\\back slash cap november', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\O\\back slash cap o.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\O\\back slash cap oscar', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\P\\back slash cap p.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\P\\back slash cap papa', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Q\\back slash cap q.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Q\\back slash cap quebec', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\R\\back slash cap r.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\R\\back slash cap romeo', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\S\\back slash cap s.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\S\\back slash cap sierra', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\T\\back slash cap t.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\T\\back slash cap tango', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\U\\back slash cap u.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\U\\back slash cap uniform', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\V\\back slash cap v.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\V\\back slash cap victor', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\W\\back slash cap w.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\W\\back slash cap whiskey', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\X\\back slash cap x.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\X\\back slash cap xray', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Y\\back slash cap y.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Y\\back slash cap yankee', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Z\\back slash cap z.'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['\\Z\\back slash cap zulu', 'new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
    
#      mediator.say(['index', 'semi', 'variable', 'semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous semi', 'previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['after', 'semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before previous semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['after semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)

#  #OK up to here            
#      mediator.say(['before semi'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', 'brackets', '0', ',\\comma', '1', ',\\comma', '3'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous comma\\previous comma', 'previous comma\\previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after comma\\after comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before previous comma\\before previous comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before next comma\\before next comma'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', '.\\dot', 'field', '.\\dot', 'value'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'dot', 'previous', 'dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'dot'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['braces', 'variable', ': \\colon', '0', 'value', ': \\colon', '0'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'colon', 'previous', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', '2', '*\\asterisk', '3', '*\\asterisk', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'asterisk', 'previous', 'star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'asterisk'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'star'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', '2', '/\\slash', '3', '/\\slash', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'slash', 'previous', 'slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'slash'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', '2', ' + \\plus', '3', ' + \\plus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'plus', 'previous', 'plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'plus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', '2', ' - \\minus', '3', ' - \\minus', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'minus', 'previous', 'minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'minus'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['variable', ' = \\equals', '2', ' % \\modulo', '3', ' % \\modulo', '4'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'percent', 'previous', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '&\\and percent', '1', '&\\and percent', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'and', 'percent', 'previous', 'and', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'and', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'and', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'and', 'percent'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '|\\pipe', '1', '|\\pipe', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'pipe', 'previous', 'pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'pipe'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '...\\ellipsis', '1', '...\\ellipsis', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'ellipsis', 'previous', 'ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'ellipsis'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '!\\bang', '1', '!\\bang', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'bang', 'previous', 'bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'bang'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '?\\question mark', '1', '?\\question mark', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'question', 'mark', 'previous', 'question', 'mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'question', 'mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'question', 'mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'question', 'mark'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '#\\pound', 'sign', '1', '#\\pound', 'sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'pound', 'sign', 'previous', 'pound', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'pound', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'pound', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'pound', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '::\\double colon', '1', '::\\double colon', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'double', 'colon', 'previous', 'double', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'double', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'double', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'double', 'colon'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '~\\tilde', '1', '~\\tilde', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'tilde', 'previous', 'tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'tilde'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '<\\less sign', '1', '<\\less sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'less', 'sign', 'previous', 'less', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'less', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'less', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'less', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '>\\greater sign', '1', '>\\greater sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'greater', 'sign', 'previous', 'greater', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'greater', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'greater', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'greater', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['0', '=\\equal sign', '1', '=\\equal sign', '2'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['previous', 'equal', 'sign', 'previous', 'equal', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['after', 'equal', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'previous', 'equal', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['before', 'next', 'equal', 'sign'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)        
    
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
    
#      mediator.say(['between parens', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'paren'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'parens'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['between brackets', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['out', 'of', 'brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'bracket'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'brackets'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['between braces', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'brace'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'braces'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)


#      mediator.say(['between angled', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'angled'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['between single quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'single', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'single', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'single', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'single', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'single', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'single', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'single', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['between quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)

#      mediator.say(['between back quotes', '1'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'back', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['after', 'back', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'back', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['previous', 'back', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['out', 'of', 'back', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['before', 'previous', 'back', 'quote'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)    
#      mediator.say(['back', 'out', 'of', 'back', 'quotes'], user_input='2\n2\n2\n2\n2\n2\n2\n', echo_utterance=1)
#      mediator.say(['new', 'statement'], user_input='2\n2\n2\n2\n', echo_utterance=1)
    
    mediator.quit(save_speech_files=0, disconnect=0)


def run():

    #
    # This file contains the native code that we will dictate
    #
    native_py_file = vc_globals.test_data + os.sep + 'native_python.py'
    native_py_file = re.sub('\\\\', '\\\\\\\\', native_py_file)

    #
    # Dictate some pseudo python where all symbols are already known
    #
    print '>>> Dictating Python when all symbols are known <<<\n'
    mediator.init_simulator()
    mediator.compile_symbols([native_py_file])
    mediator.print_symbols()
    dictate_pseudo_python()

    #
    # Dictate some pseudo python where only standard symbols are already known
    #
    print '\n>>> Dictating Python when only standard symbols are known <<<\n'    
    mediator.init_simulator()
    mediator.print_symbols()
    dictate_pseudo_python()    
