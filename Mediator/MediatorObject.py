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


def add_lsa(language_list, spoken_as_list, written_as):
    """Add a language specific word.

    These words get added and removed dynamically from the SR
    vocabulary, depending on the language of the active buffer.

    A redundant CSC is also added to allow translation of the LSA at
    the level of the Mediator, in cases where NatSpeak prefers to
    recognise the LSA as dictated text instead of a spoken/written
    word (this often happens if the spoken form looks to much like
    dictated text, e.g. "is not equal to").
    
    **INPUTS**
    
    *[STR]* language_list -- Names of the languages for which this
    new word applies. If None, then add this for all languages.
        
    *STR* spoken_as_list -- List of spoken form of the word.

    *STR* written_as -- Written form of the word.
    
    **OUTPUTS**
    
    *none* -- 
    """
    
    global to_configure

#    print '-- MediatorObject.add_lsa: language_list=%s, spoken_as_list=%s, written_as=\'%s\'' % (repr(language_list), repr(spoken_as_list), written_as)

    
    if language_list == None:
        #
        # For None language, add entries to the SR vocabulary
        #            
        for spoken_as in spoken_as_list:
            entry = sr_interface.vocabulary_entry(spoken_as, written_as)
            sr_interface.addWord(entry)
    else:
        for language in language_list:
            for spoken_as in spoken_as_list:
                entry = sr_interface.vocabulary_entry(spoken_as, written_as)
#                print '-- MediatorObject.add_lsa: processing language=%s, spoken_as=%s, written_as=%s' % (language, spoken_as, written_as)
                if to_configure.interp.language_specific_aliases.has_key(language):
                    to_configure.interp.language_specific_aliases[language] = to_configure.interp.language_specific_aliases[language] + [entry]
                else:
                    to_configure.interp.language_specific_aliases[language] = [entry]

    #
    # Generate an anonymous action function that types the appropriate text
    #
    the_action = actions_gen.anonymous_action('app.insert(\'%s\')' % written_as, 'Inserts \'%s\'' % written_as)                    

    #
    # Add a CSC for translating the LSA at the mediator level.
    # This redundant translation is necessary because if the spoken form of
    # the LSA looks too much like dictated text (e.g. "is equal to"), NatSpeak
    # will tend to always recognise it as dictated text instead of a
    # spoken form/written form word. So Mediator must be able to translate
    # it also in case NatSpeak screws up
    #
    if language_list == None:
        #
        # If no language was specified, the CSC applies in all contexts
        #
        the_meanings = [cont_gen.ContAny(), the_action]
    else:
        #
        # Applicable contexts are the language contexts for each of the
        # applicable languages
        #
        the_meanings = []
        for a_language in language_list:
            the_meanings = the_meanings + [[cont_gen.ContLanguage(language=a_language), the_action]]

    aCSC = CSCmd.CSCmd(spoken_forms=spoken_as_list, meanings=the_meanings)
    #
    # Note: we add this CSC with add_voc_entry=0 because we don't want to
    #       reenforce NatSpeak's tendancy to recognise the LSA as a dictated
    #       sentence
    #
    add_csc(aCSC, add_voc_entry=0)
        
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
    to_configure.interp.known_symbols.abbreviations[abbreviation] = expansions


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


