"""This script demos the capabitilies of VoiceCode.

You can do the demo in gui_sim.py by typing the following command in the
command pane:

execfile('demo.py')

and then using up/down arrows to navigate through the command history.

Make sure that:

- you are in directory 'Data/TestData'
- do File.Open and open 'Data/TestData/large_buff.py' (this makes sure you
 are in the correct directory and also makes sure that symbols for that file
 have been compiled)
- the current buffer is a python one"""


def push_cmd(command):
    """Add a command to the GUI EdSim command history, without executing it"""
    the_mediator.interp.on_app.the_editor.frame.pane.command_prompt.push(command)


#
# Make command history behave like in DOS, i.e. cursor is left at its current
# position when you push a new command onto the history stack.
#
the_mediator.interp.on_app.the_editor.frame.pane.command_prompt.cursor_always_on_top = 0

push_cmd("""# Let's look at a first example""")
push_cmd("""say(['define', 'method', 'create', 'attribute', 'add', 'argument', 'attribute', 'definition', 'method', 'body'])""")

push_cmd("""# Let's decompose that""")
push_cmd("""say(['define', 'method'])""")
push_cmd("""# Typed template code for method (no need to say 'self' or 'parens') ...""")
push_cmd("""# ... and automatically put cursor at next logical place""")
push_cmd("""say(['create', 'attribute'])""")
push_cmd("""# Didn't have to say underscore for new symbol""")
push_cmd("""say(['add', 'argument'])""")
push_cmd("""# Moved to end of argument list and added comma (wouldn't add comma if argument list empty)""")
push_cmd("""say(['attribute', 'definition'])""")
push_cmd("""# Automatically abbreviated as known symbol attr_def""")
push_cmd("""say(['method', 'body'])""")
push_cmd("""# Moved to the method body ...""")
push_cmd("""# ... and automatic indentation done by mediator (but editor level auto indent also supported)""")

push_cmd("""# Note that you can dictate non-linearly""")
push_cmd("""# For example, Here's how you dictate balanced expressions""")
push_cmd("""say(['an', 'array', 'at', 'index', 'some', 'function', 'with', 'argument', 'some', 'other', 'function', 'with', 'argument', '0'])""")
push_cmd("""# Didn't have to say the closing part of each of the balanced expressions...""")
push_cmd("""#   ... and can skip over all of them with a single utterance""")
push_cmd("""say(['out', 'of', 'brackets'])""")

push_cmd("""# To navigate, can use many strategies""")

push_cmd("""# Navigation Strategy 1: Navigation by punctuation""")
push_cmd("""say(['previous', 'paren'])""")
push_cmd("""# Didn't have to say whether it was an open or close paren...""")
push_cmd("""say(['previous', 'open', 'paren'])""")
push_cmd("""# ... but can certainly specify that""")
push_cmd("""# Note that searches are repeatable...""")
push_cmd("""say(['again'])""")
push_cmd("""# ... multiple times""")
push_cmd("""say(['3 times'])""")
push_cmd("""# ... and so is any operation of type "repeatable" such as:""")
push_cmd("""# ... page up/down, line up/down, forward/backward char etc.""")
push_cmd("""# In the future, you will be able to repeat such operations in a loop""")
push_cmd("""# For example: 'page up keep doing that' will keep paging up""")
push_cmd("""# ... until you say 'stop'""")
push_cmd("""# Note also that searches are reversible""")
push_cmd("""say(['reverse'])""")
push_cmd("""# ... and so is any "bidirectional" operation such as (again):""")
push_cmd("""# ... page up/down, line up/down, forward/backward char etc.""")

push_cmd("""# Navigation Strategy 2: Select Pseudo-Code""")


push_cmd("""# Navigation Strategy 2: Approximate positionning""")


