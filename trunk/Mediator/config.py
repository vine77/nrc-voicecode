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
    



def add_lsa(language_list, spoken_as_list, written_as):
    """Add a language specific word.

    These words get added and removed dynamically from the SR
    vocabulary, depending on the language of the active buffer.
    
    **INPUTS**
    
    *[STR]* language_list -- Names of the languages for which this
    new word applies. If None, then add this for all languages.
        
    *STR* spoken_as_list -- List of spoken form of the word.

    *STR* written_as -- Written form of the word.
    
    **OUTPUTS**
    
    *none* -- 
    """
    
    global interp

#    print '-- config.add_lsa: language_list=%s, spoken_as_list=%s, written_as=\'%s\'' % (repr(language_list), repr(spoken_as_list), written_as)
    if language_list == None:
        #
        # For None language, add it to the SR vocabulary
        #            
        sr_interface.addWord(entry)
    else:
        for language in language_list:
            for spoken_as in spoken_as_list:
#                print '-- config.add_lsa: processing language=%s, spoken_as=%s, written_as=%s' % (language, spoken_as, written_as)
                entry = sr_interface.vocabulary_entry(spoken_as, written_as)
                if interp.language_specific_aliases.has_key(language):
                    interp.language_specific_aliases[language] = interp.language_specific_aliases[language] + [entry]
                else:
                    interp.language_specific_aliases[language] = [entry]
                

def define_language(name, definition):
    """Defines the syntax of a programming language.
    
    **INPUTS**
    
    *STR* name -- name of the programming language
    
    [LangDef] definition -- language definition 
    
    
    **OUTPUTS**
    
    *none* -- 
    
    .. [LangDef] file:///./LangDef.LangDef.html"""
    
    SymDict.language_definitions[name] = definition
    
