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


push_cmd("""# - template code""")
push_cmd("""# - symbol dictation""")
push_cmd("""# - navigation""")
push_cmd("""# - indentation""")
push_cmd("""say(['for', 'an', 'attribute', 'definition', 'in', 'attributes', 'this', 'class', 'dot', 'items', 'without', 'arguments', 'do'])""")
push_cmd("""say(['for'])""")
push_cmd("""say(['do'])""")


push_cmd("""# - non-linear dictation of balanced expressions""")


push_cmd("""# - navigation by punctuation""")
push_cmd("""# - repeatble commands""")

push_cmd("""# -Select pseudo-code""")
