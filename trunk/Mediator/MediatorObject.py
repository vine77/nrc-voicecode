import natlink
import actions_gen, AppState, CmdInterp, cont_gen, CSCmd, Object, re, sr_interface, SymDict, vc_globals

"""Defines main class for the mediator.

**MODULE VARIABLES**

[MediatorObject] *to_configure* -- When configuring a mediator object, we temporarily assign it to this global variable so that it be accessible from the various configuration function.

..[MediatorObject] file:///./MediatorObject.MediatorObject.html"""

to_configure = None

class MediatorObject(Object.Object):
    """Main object for the mediator.

    Typically, there will be one such object for every application
    that is being controlled through a VoiceCode mediator.
    
    **INSTANCE ATTRIBUTES**

    [AppState] *app = AppState.AppState()* -- Application being run
    through the mediator.
    
    [CmdInterp] *interp=CmdInterp.CmdInterp()* -- Command interpreter used to
    translate pseudo-code to native code.
    
    [CommandDictGrammar] *mixed_grammar = None* -- Speech Recognition grammar
    that recognises continuous dictation and forwards the results to the
    *interp* command interpreter.

    [CodeSelectGrammar] code_select_grammar = None -- Grammar for
    selecting a part of the visible code.

    CLASS ATTRIBUTES**
    
    *none* --

    ..[AppState] file:///./AppState.AppState.html
    ..[CmdInterp] file:///./CmdInterp.CmdInterp.html
    ..[CommandDictGrammar] file:///./sr_interface.CommandDictGrammar.html
    ..[CodeSelectGrammar] file:///./sr_interface.CodeSelectGrammar.html"""
    
    def __init__(self, interp=CmdInterp.CmdInterp(), \
                       **attrs):
        natlink.natConnect()        
        self.deep_construct(MediatorObject, \
                            {'interp': interp, \
                             'mixed_grammar': None, \
                             'code_select_grammar': None}, \
                            attrs, \
                            {})
        self.mixed_grammar = sr_interface.CommandDictGrammar(interpreter=self.interp)
        self.code_select_grammar = sr_interface.CodeSelectGrammar(interpreter=self.interp)


    def configure(self, config_file=vc_globals.default_config_file):
        """Configures a mediator object based on a configuration file.
        
        **INPUTS**
        
        *STR* config_file = vc_globals.default_config_file -- Full path of the config 
        

        **OUTPUTS**
        
        *none* -- 
        """
        global to_configure
        
        to_configure = self
        
        try:
            execfile(config_file)
        except Exception, err:
            print 'ERROR: in configuration file %s.\n' % config_file
            raise err

        #
        # Compile standard symbols for the different languages
        #
        to_configure.interp.known_symbols.parse_standard_symbols(add_sr_entries=to_configure.interp.known_symbols.sr_symbols_cleansed)
        to_configure.interp.known_symbols.sr_symbols_cleansed = 0
        
        to_configure = None

    
###############################################################################
# Configuration functions. These are not methods
###############################################################################

def add_csc(acmd, add_voc_entry=1):
    """Add a new Context Sensitive Command.

    [CSCmd] *acmd* is the command to add.

    *BOOL add_voc_entry = 1* -- if true, add a SR vocabulary entry
    for the CSC's spoken forms
    

    .. [CSCmd] file:///./CSCmd.CSCmd.html"""

    global to_configure
    to_configure.interp.index_csc(acmd, add_voc_entry)


def add_lsa(spoken_forms, meanings):
    """Add a language specific word.

    These words get added and removed dynamically from the SR
    vocabulary, depending on the language of the active buffer.

    A redundant CSC is also added to allow translation of the LSA at
    the level of the Mediator, in cases where NatSpeak prefers to
    recognise the LSA as dictated text instead of a spoken/written
    word (this often happens if the spoken form looks to much like
    dictated text, e.g. "is not equal to").
    
    **INPUTS**
    
    *STR* spoken_forms -- List of spoken form of the word.

    *{STR: STR}* meanings -- Dictionary of language specific
     meanings. Key is the language name and value is the written form
     of the LSA for that langugage. If language name is *None*, then
     it means that this LSA applies for all languages (I know, it
     doesn't make much sense syntactically).
    
    **OUTPUTS**
    
    *none* -- 
    """
    
    global to_configure

#    print '-- MediatorObject.add_lsa: spoken_forms=%s' % spoken_forms
    
    for a_meaning in meanings.items():
        language, written_as = a_meaning
        for spoken_as in spoken_forms:
            entry = sr_interface.vocabulary_entry(spoken_as, written_as)
            vc_entry = sr_interface.vocabulary_entry(spoken_as, written_as, clean_written=0)
            
            if to_configure.interp.language_specific_aliases.has_key(language):
                to_configure.interp.language_specific_aliases[language] = to_configure.interp.language_specific_aliases[language] + [vc_entry]
            else:
                to_configure.interp.language_specific_aliases[language] = [vc_entry]
            if language == None:
                #
                # This LSA is not tied to a particular langauge, so it
                # doesn't have to be dynamically added/removed
                # Add it once and for all
                #
                sr_interface.addWord(entry)
        
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
    global to_configure
    to_configure.interp.known_symbols.add_abbreviation(abbreviation, expansions, user_added=1)


def standard_symbols_in(file_list):
    """Compile symbols defined in a series of source files"""
    global to_configure

    for a_file in file_list:
        if not a_file in to_configure.interp.known_symbols.standard_symbol_sources:
            to_configure.interp.known_symbols.standard_symbol_sources = to_configure.interp.known_symbols.standard_symbol_sources + [a_file]
    

def define_language(name, definition):
    """Defines the syntax of a programming language.

    **INPUTS**

    *STR* name -- name of the programming language

    [LangDef] definition -- language definition 


    **OUTPUTS**

    *none* -- 

    .. [LangDef] file:///./LangDef.LangDef.html"""

    definition.name = name
    SymDict.language_definitions[name] = definition


def print_abbreviations():
    global to_configure
    to_configure.interp.known_symbols.print_abbreviations()
