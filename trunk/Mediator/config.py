"""Commands for configuring VoiceCode"""

import vc_globals

def add_csc(acmd):
    """Add a new Context Sensitive Command.

    [CSCmd] *acmd* is the command to add.

    .. [CSCmd] file:///./CSCmd.CSCmd.html"""

    vc_globals.interp.index_csc(acmd)

    
