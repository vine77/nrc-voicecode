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
    
    *meanings=[[* [Context] *, FCT]]* -- list of possible contextual
      meanings for this command. Each element is a pair with 1st
      element being a context and the 2nd element being an action
      function to be fired if that context applies.

    CLASS ATTRIBUTES**
        
    *none* --

    .. [Context] file:///./Context.Context.html"""
        
    def __init__(self, spoken_forms=[], meanings=[], **attrs):
        Object.__init__(self)
        self.def_attrs({'spoken_forms': spoken_forms, 'meanings': meanings})
        self.init_attrs(attrs)



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
#        print '-- CSCmd.interpret: self.meanings%s' % self.meanings
        for ameaning in self.meanings:
            cont, action = ameaning[0], ameaning[1]
#            print '-- CSCmd.interpret: cont=%s' % cont
#            print '-- CSCmd.interpret: ameaning=%s, cont=%s, action=%s' % (ameaning, cont, str(action))
            if (cont == None or cont.applies(app)):
#                print '-- CSCmd.interpret: this context applies'
                action(app, cont)
                applied = 1
                break
        return applied

