import sys

from Object import Object


class CSCmd(Object):
    """Class for Context Sensitive Commands (CSCs).

    A CSC is a phrase which, when uttered into an application, may
    fire a particular action.
    
    A CSC may fire different actions depending on the context of the
    application where it was typed.
        
    **INSTANCE ATTRIBUTES**
        
    *STR spoken_forms=[]* -- list of alternatives ways that this
     command can be spoken out. They can be regular expressions.
    
    *meanings=*{* [Context] *: * [Action] *}* -- Dictionary of
    possible contextual meanings for this command. Key is a context
    and value is an action object to be fired if that context applies.

    CLASS ATTRIBUTES**
        
    *none* --

    .. [Context] file:///./Context.Context.html
    .. [Action] file:///./Action.Action.html"""
        
    def __init__(self, spoken_forms=[], meanings={}, docstring=None, **attrs):
        self.deep_construct(CSCmd,
                            {'spoken_forms': spoken_forms,\
                             'meanings': meanings},
                            attrs)


    def interpret(self, app):
        """Executes the command if any of its contexts applies.

        [AppState] app is the application into which the command was spoken.

        Returns *true* iif on of the valid contexts applied.
        
        .. [AppState] file://./AppState.AppState.html"""

        applied = 0
        
        #
        # Try each of the contextual meanings in turn until find one that
        # applies
        #
#        print '-- CSCmd.interpret: self.meanings=%s' % self.meanings
        for ameaning in self.meanings.items():
            cont, action = ameaning
#            print '-- CSCmd.interpret: cont=%s' % cont
#            print '-- CSCmd.interpret: ameaning=%s, cont=%s, action=%s, action.doc()=%s' % (ameaning, cont, str(action), action.doc())
            if (cont == None or cont.applies(app)):
#                print '-- CSCmd.interpret: this context applies'
                action.execute(app, cont)
#                print '-- CSCmd.interpret: current buffer is now:'
#                app.print_buff_content()
                applied = 1
                break            

        return applied

    def doc(self):
        """Returns the documentation for that CSC.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return self.docstring
