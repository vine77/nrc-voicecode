"""Commands for configuring VoiceCode

MODULE VARIABLES

[CmdInterp] interp -- the VoiceCode command interpreter (NOTE: because *CmdInterp.py* imports *vc_globals.py*, this variable is initialised in *CmdInterp.py* to avoid circular reference)

[CommandDictGrammar] mixed_grammar -- the SR grammar that recognises mixed continuous dictation and command utterances.

.. [CmdInterp] file:///./CmdInterp.CmdInterp
.. [CommandDictGrammar] file:///./sr_interface.CommandDictGrammar.html"""

import CmdInterp, EdSim, SourceBuff, sr_interface, SymDict, vc_globals

interp = CmdInterp.CmdInterp(app=EdSim.EdSim())
mixed_grammar = sr_interface.CommandDictGrammar(interpreter=interp)
code_select_grammar = sr_interface.CodeSelectGrammar(app=interp.app)

def add_csc(acmd):
    """Add a new Context Sensitive Command.

    [CSCmd] *acmd* is the command to add.

    .. [CSCmd] file:///./CSCmd.CSCmd.html"""

    global interp
    interp.index_csc(acmd)



def associate_language(extension, language):
    """Add an association between a file extension and a programming
    language.
        
    **INPUTS**
        
    *STR* extension -- file names that end with this extension
    will be asociated with language *languate*
        
    *STR* language -- name of the programming language        

    **OUTPUTS**
        
    *none* -- 
    """
    SourceBuff.file_language[extension] = language




def add_abbreviation(abbreviation, expansions):
    """Add an abbreviation to VoiceCode's abbreviations dictionary.
    
    **INPUTS**
    
    *STR* abbreviation -- the abbreviation 
    
    *[STR]* expansions -- list of possible expansions
    
    
    **OUTPUTS**
    
    *none* -- 
    """
    global interp
    interp.known_symbols.abbreviations[abbreviation] = expansions
    

def define_language(name, definition):
    """Defines the syntax of a programming language.
    
    **INPUTS**
    
    *STR* name -- name of the programming language
    
    [LangDef] definition -- language definition 
    
    
    **OUTPUTS**
    
    *none* -- 
    
    .. [LangDef] file:///./LangDef.LangDef.html"""
    
    SymDict.language_definitions[name] = definition
    
