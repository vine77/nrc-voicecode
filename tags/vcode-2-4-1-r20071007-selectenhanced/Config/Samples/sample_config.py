
#  should the RecogStartMgr trust that the current
#  window corresponds to the editor when the editor first connects to
#  VoiceCode, or when it notifies VoiceCode of a new window.

# uncomment the following line if you want RecogStartMgr to trust 
# the current window
# trust_current_window(1)

text_mode_toggling(on_spoken_as=['text mode on', 'nat text on',
                                 'natural text on', 'code mode off', 
                                 'coding mode off'],
                   off_spoken_as=['text mode off', 'nat text off',
                                  'natural text off', 'code mode on', 
                                  'coding mode on'],
                   off_sets_nat_text_to=1)

# change these assignment if you are not using (NaturallySpeaking) US
# English edition
std_punc = std_US_punc
alt_punc = alt_US_punc
std_grouping = std_US_grouping
std_quotes = std_US_quotes
alt_grouping = alt_US_grouping
alt_quotes = alt_US_quotes
std_small_numbers = std_US_small_numbers

# Capitalize command names, according to Natspeak version:

# for Natspeak 5 or earlier, use this line

#capitalize_rules(1)

# fro Natspeak 6 or later, use this line

capitalize_rules(0)

#######################################
# Include user-defined forms here
#######################################

###################################################################
# Standard symbols:
#
# Choose which files you want to scan for standard symbols (these 
# files will be re-scanned whenever the saved symbol dictionary 
# is lost, or when these files have changed since the symbol dictionary,
# or when you create a new set of speech files for VoiceCode.
#
# You can include your own files, as well as the standard ones which
# ship with VoiceCode.
###################################################################

#
# Python standard symbols
#
symbol_files = []

py_std_sym = os.path.join(vc_globals.config, 'py_std_sym.py')
symbol_files.append(py_std_sym)

C_Cpp_std_sym = os.path.join(vc_globals.config, 'C_Cpp_std_sym.cpp')
symbol_files.append(C_Cpp_std_sym)

standard_symbols_in(symbol_files)

###################################################################
# Standard abbreviations:
#
# Specify the abbreviation files which define abbreviations 
# and expansions.  
#
# These files will be re-scanned whenever the saved symbol dictionary 
# is lost, or when these files have changed since the symbol dictionary
#
# Abbreviations read from these files are appended to the list of
# abbreviations for a given word, so the first file in the list takes 
# precedence.  However, because the abbreviation dictionary is
# persistent, previously added entries will take precedence over the
# ones included in these files.  To override these abbreviations, use
# the import abbreviation function from within the mediator.
#
# You can include your own files, as well as the standard ones which
# ship with VoiceCode, but because of the persistence noted above,
# personal abbreviations are normally added by importing them, so that
# they take precedence.
#
###################################################################

abbrev_files = []

std_abbrevs = os.path.join(vc_globals.config, 'std_abbrevs.py')
py_abbrevs = os.path.join(vc_globals.config, 'py_abbrevs.py')
C_Cpp_abbrevs = os.path.join(vc_globals.config, 'C_Cpp_abbrevs.py')

abbrev_files.append(std_abbrevs)
abbrev_files.append(py_abbrevs)
abbrev_files.append(C_Cpp_abbrevs)

abbreviations_in(abbrev_files)

#######################################
# add standard command and alias sets
#######################################

# generic

add_capitalization_word_set(manual_formatting)

add_cmd_set(manual_styling)
add_cmd_set(mediator_ctrl)
add_cmd_set(out_of_balance)
add_cmd_set(indent_cmds)
add_cmd_set(change_direction)
add_cmd_set(math_ops)
add_cmd_set(logic_ops)
add_cmd_set(comparisons)
add_cmd_set(empty_pairs)
add_cmd_set(functional_pairs)
add_cmd_set(comment_aliases)
add_cmd_set(comment_commands)
add_cmd_set(misc_aliases)
add_cmd_set(new_statement)
add_cmd_set(compound_statements)
add_cmd_set(ctrl_structures)
add_cmd_set(data_structures)
add_cmd_set(function_definitions)
add_cmd_set(navigation_within_buffer)
add_cmd_set(insertion_deletions)

# new: QH
add_cmd_set(declare_variables)
add_cmd_set(operator_cmds)

#######################################
# Python-specific
#######################################

add_cmd_set(misc_python)
add_cmd_set(misc_python_cmds)
add_cmd_set(python_statements)
add_cmd_set(python_compound)
add_cmd_set(python_imports)
add_cmd_set(python_imports_cscs)
add_cmd_set(python_comparisons)
add_cmd_set(python_operators)
add_cmd_set(python_string_qualifiers)
add_cmd_set(python_functional)
py_std_func_calls.create(interpreter) 

#######################################
# C/C++-specific
#######################################

add_cmd_set(c_preprocessor_cmds)
add_cmd_set(c_navigation)
add_cmd_set(c_type_declarations)
add_cmd_set(c_type_casts)
add_cmd_set(c_statements)
add_cmd_set(c_preprocessor)
add_cmd_set(c_syntax)
add_cmd_set(c_reserved_words)

#######################################
# JavaScript-specific
#######################################
add_cmd_set(javascript_reserved_words)

#######################################
# php-specific
#######################################
add_cmd_set(php_special_lsas)

#######################################
# Emacs specific
#######################################

add_cmd_set(emacs_ctrl)

#######################################
# add generated sets
#######################################

# See config_helpers.py for the definitions of these generator
# functions, and additional parameters to customize their behavior

add_letters(military_letters, prefix = "")
add_letters(military_letters, prefix = "letter-")
add_cmd_set(military_letters)

add_escaped_characters(escaped_characters)
add_cmd_set(escaped_characters)

add_repeats(repeat_last)
add_cmd_set(repeat_last)

add_backspacing(backspacing)
add_cmd_set(backspacing)

#######################################
# add punctuation sets
#######################################

# always create the standard (std_) sets after all the alternative 
# sets (or any user-defined sets), and do not use force = 1.  
# This allows you to override the spacing behavior of standard 
# punctuation by adding punctuation with the same spoken form to 
# the corresponding alt_ set.
#
# Also, use force = 1 for any sets of non-standard
# punctuation, otherwise LSAs won't be added unless the corresponding
# vocabulary entry already exists.
# 

# If you want colon to have normal spacing instead of the default
# defined in std_US_punc in vc_config, you should add this line
# anywhere in your user configuration file before alt_punc.create

# alt_punc.add(':', ['colon'], spacing = normal_spacing)


alt_punc.create(interpreter, force = 1)
alt_grouping.create(interpreter, force = 1)
alt_quotes.create(interpreter, force = 1)

std_punc.create(interpreter)
std_grouping.create(interpreter)
std_quotes.create(interpreter)



#######################################
# add sets for dictating 2-digit numbers
#######################################
std_small_numbers.create(interpreter, numeral_prefix = "numeral ")

#####example adding you own commands 1:
##acmd = CSCmd(spoken_forms=['new method'],
##             meanings={contC: c_function_definition,
##                      contPython: py_method_declaration},
##             docstring='function definition')
##add(acmd)
#####end example

###### Example adding your own commands in a new CmdSet:
##hello_cmds = CmdSet(name = 'hello commands',
##                    description = 'just illustrating how to create a Command set')
### Create the first CSC command and add it to the set
##acmd = CSCmd(spoken_forms=['hello to planet', 'greetings to planet'], 
##             meanings={ContAny(): 
##                       ActionInsert('Hello to planet ', 
##                                     '!!!')}, 
##             docstring='prints a hello to plane.')
##hello_cmds.add(acmd)
### Create a second CSC command and add it to the set directly:
##hello_cmds.add(CSCmd(spoken_forms=['hello from planet', 'greetings from planet'], 
##                     meanings={ContAny(): 
##                        ActionInsert('Hello from planet: !!')}))  # docstring is optional
### Create afirst LSAlias command and add it to the set:
##acmd = LSAlias(['hello to you', 'greeting to you'], 
##     {all_languages: 'hello to you'}, name = 'hello_to_you')
##hello_cmds.add(acmd)
##
### Create a second LSAlias command and add it to the set directly
### for 'java' (one of the c_style_languases) the command will be in all caps:
##hello_cmds.add(LSAlias(['hello from me', 'greeting from me'], 
##     {c_style_languages: 'hello from me', 'java': 'HELLO FROM ME'}))
### Add the command set to the command interpreter (CmdInterp):
##add_cmd_set(hello_cmds)
##### end example...

#######################################
# variable formatting preferences
#######################################

####next lines set normal variables in several languages to lowerHungarian:
##set_builder_preferences(['std_lower_intercaps', 'std_underscores', 'std_run_together'],
##                        language=('python', 'javascript', 'php'))
##
###next lines set variables after a class statement to UpperHungarian:
##set_builder_preferences(['std_intercaps', 'std_underscores',
##    'std_all_caps_underscores'], language=all_languages, identifier = 'class')

