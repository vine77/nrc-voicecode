from Object import Object

class Context(Object):
    """Base class for all application contexts.

    This virtual class is the base class for all context objects.
    
    **INSTANCE ATTRIBUTES**
    
    *STR doc_string=None* -- A string describing the purpose of the
     context. Used to generate "what can I say" help.
    
    *[STR] doc_topics=[]* -- List of topics where this context is
     relevant. Used to generate "what can I say" help.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, doc_string=None, doc_topics=[], **attrs):
        Object.__init__(self)
        self.def_attrs({'doc_string': doc_string, 'doc_topics': doc_topics})
        self.init_attrs(attrs)



    def applies(self, app):        
        """Returns *true* iif the context applies given current state
        of an application.

        [AppState] *app* is the application in question.
        
        .. [AppState] file:///./AppState.AppState.html"""
        
        debug.virtual('applies')




#  Todo

#  NOTE: This todo list based on old Perl code. Some of it may still
#  be relevant.

#  =head3 ContCompound

#  Create a subclass I<ContCompound> for describing compound contexts
#      e.g my $comp = new ContCompound(cond => or(new ContCFor(), ContCForGeneral()));

#  the L<applies> method would then return a list of parsed contexts
#  which applied in the course of evaluating the condition. This list
#  would be passed to the action function (Q: how does the action method
#  know which item of the list correspond to which part of the compound
#  context? maybe the returned list should be structured in such a way
#  that we know what condition was evaluated and what elements of it
#  applied).

#  Similar idea: ContSeq which describes a sequence of contexts that must
#  be satisfied, with 

#  =head3 @$appName

#  Add attribute I<@$appName> that will store the names of applications
#  to which this context applies. If undef, (or empty?) then it means it
#  applies across all apps.

#  Should add an I<$name> attribute to L<AppState/AppState> that would
#  store the name of the app it keeps status of. Then L<applies> would
#  check that I<$name> is contained in I<@$appName>.
