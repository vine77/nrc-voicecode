#  should the RecogStartMgr trust that the current
#  window corresponds to the editor when the editor first connects to
#  VoiceCode, or when it notifies VoiceCode of a new window.

# uncomment the following line if you want RecogStartMgr to trust 
# the current window
# trust_current_window(1)


# change these assignment if you are not using (NaturallySpeaking) US
# English edition
std_punc = std_US_punc
alt_punc = alt_US_punc
std_grouping = std_US_grouping
std_quotes = std_US_quotes
alt_grouping = alt_US_grouping
alt_quotes = alt_US_quotes

#######################################
# Include user-defined forms here
#######################################



#######################################
# add standard command and alias sets
#######################################

# generic

add_csc_set(mediator_ctrl)
add_csc_set(out_of_balance)
add_csc_set(indent_cmds)
add_csc_set(change_direction)
add_lsa_set(math_ops)
add_lsa_set(logic_ops)
add_lsa_set(comparisons)
add_lsa_set(empty_pairs)
add_csc_set(functional_pairs)
add_lsa_set(comment_aliases)
add_lsa_set(misc_aliases)
add_csc_set(new_statement)
add_csc_set(compound_statements)
add_csc_set(ctrl_structures)
add_csc_set(data_structures)
add_csc_set(function_definitions)

# Python-specific

add_lsa_set(misc_python)
add_csc_set(misc_python_cmds)
add_lsa_set(python_statements)
add_csc_set(python_compound)
add_lsa_set(python_imports)
add_lsa_set(python_comparisons)
add_lsa_set(python_operators)
add_csc_set(python_functional)

# C-specific

add_csc_set(c_preprocessor_cmds)
add_lsa_set(c_preprocessor)

#######################################
# add generated sets
#######################################

# See config_helpers.py for the definitions of these generator
# functions, and additional parameters to customize their behavior

add_escaped_characters(escaped_characters)
add_csc_set(escaped_characters)

add_repeats(repeat_last)
add_csc_set(repeat_last)

add_backspacing(backspacing)
add_csc_set(backspacing)

#######################################
# add punctuation sets
#######################################

# always create the standard (std_) sets after the corresponding alternative 
# sets (or any user-defined sets).  This allows you to override the 
# spacing behavior of standard punctuation by adding punctuation with 
# the same spoken form to the corresponding
# alt_ set.
#
# Also, use force = 1 for any sets of non-standard
# punctuation, otherwise LSAs won't be added unless the corresponding
# vocabulary entry already exists.

# If you want colon to have normal spacing instead of the default
# defined in std_US_punc in vc_config, you should add this line
# anywhere in your user configuration file before alt_punc.create

# alt_punc.add(':', ['colon'], spacing = normal_spacing)


alt_punc.create(interpreter, force = 1)
std_punc.create(interpreter)

alt_grouping.create(interpreter, force = 1)
std_grouping.create(interpreter)

alt_quotes.create(interpreter, force = 1)
std_quotes.create(interpreter)



