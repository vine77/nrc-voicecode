#
# Used to generate a list of "public" (i.e. documented) symbols for the
# standard Python libraries.
#
# Feed the .tex documentation file contained in the Python distribution and
# parse all the symbol entries.
#

import glob, re, sys

def re_tex_markup(name):
    """Returns a regexp that matches a particular tex markup."""

    regexp = '\\\\begin\\{%s(ni){0,1}\\}(\\{([^\\}]*)\\})(\\{([^\\}]*)\\})*' % name        
    return regexp



def find_symbols(markup, content, symbol_list):
    
    """Finds all symbols mentioned in a particular tex markup, and
    add them to the list"""

    regexp = re_tex_markup(markup)
    match_list = re.findall(regexp, content)
    print '-- find_symbols: regexp=\'%s\'' % regexp
    print '-- find_symbols: match_list=%s' % match_list
    for a_match in match_list:
          print '-- find_symbols: a_match = %s' % repr(a_match)
          symbol_string = a_match[2] + ', ' + a_match[4]
          symbols = re.split('[^a-zA-Z_]+', symbol_string)
          print '-- find_symbols: symbol_string=\'%s\', symbols=%s' % (symbol_string, symbols)
          for a_symbol in symbols:
              symbol_list[a_symbol] = 1

symbol_list = {}
file_list = glob.glob(sys.argv[1])
for a_file_name in file_list:

    print 'processing file \'%s\'' % a_file_name
    a_file = open(a_file_name, 'r')
    content = a_file.read()
    print '-- content=%s' % content

    find_symbols('datadesc', content, symbol_list)
    find_symbols('excdesc', content, symbol_list )   
    find_symbols('funcdesc', content, symbol_list)
    find_symbols('classdesc', content, symbol_list)
    find_symbols('methoddesc', content, symbol_list)

    symbols = symbol_list.keys()
    symbols.sort()

    for a_symbol in symbols:
        print a_symbol
    
    
    
