"""Action functions that span different languages"""

import copy, exceptions, os, re
import Object, vc_globals

class Action(Object.Object):
    """Base class for all actions.
    
    **INSTANCE ATTRIBUTES**

    *none* --

    CLASS ATTRIBUTES**
    
    *none* -- 

    """
    
    def __init__(self, docstring=None, **args_super):
        self.deep_construct(Action, \
                            {}, \
                            args_super, \
                            {})

    def log_execute(self, app, cont):
        """Executes the action and logs it in the application's history.
        
        **INPUTS**
        
        [AppState] app -- The application to execute and log the action on.
        
        [Context] cont -- The context object that determines the parameters
        of how the action will be executed.
        

        **OUTPUTS**
        
        *none* -- 

        .. [AppState] file:///./AppState.AppState.html
        .. [Context] file:///./Context.Context.html"""

        #
        # First, make a copies of the action and context before logging them
        # to the command, in case the same prototype context and action
        # instances are being reused everytime a particular CSC is uttered.
        #
        # That way, if we later modify a command in the history (e.g.
        # "previous one" command to reexecute a directional command
        # but in the opposite direction), we won't end up affecting
        # all instances of that action.
        #
        # Note that we don't do this inside of *log* method because some
        # subclasses may override this method and forget to do the copies.
        # For example, actions that just repeat a previous action do not
        # log themselves, but instead log the actions that they repeat.
        #
        action_copy = copy.copy(self)        
        cont_copy = copy.copy(cont)
        action_copy.log(app, cont_copy)
        action_copy.execute(app, cont)


    def log(self, app, cont):
        """Log the action to an application's command history
        
        **INPUTS**
        
        [AppState] app -- Application to log the action with.

        [Context] cont -- Context in which the action was executed.
        

        **OUTPUTS**
        
        *none* -- 
        """
        app.log_cmd(cont, self)


    def execute(self):
        """Execute the action.
        
        **INPUTS**
        
        [AppState] app -- Application on which to execute the action
        
        [Context] app_cont -- Context of the application that
        determines the parameters of how the action will be executed.
                
        **OUTPUTS**
        
        *none* -- 

        .. [AppState] file:///./AppState.AppState.html"""
        
        debug.virtual('execute')

    def doc(self):
        """Returns a documentation string for the action.
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """
        
        return self.docstring

class ActionRepeatable(Action):
    """Base class for repeatable actions.

    This class doesn't actually have any additional methods. It's just
    used to flag a subclass as being an action class that can be
    repeated.
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, docstring=None, **args_super):
        self.deep_construct(Action, \
                            {}, \
                            args_super, \
                            {})

class ActionRepeatLastCmd(Action):
    """This action just repeats the last command in the command history.

    **INSTANCE ATTRIBUTES**
    
    *INT n_times=1* -- Number of times to repeate the previous command.
    
     **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, n_times=1, **args_super):
        self.deep_construct(ActionRepeatPreviousCmd, \
                            {'n_times': n_times}, \
                            args_super, \
                            {})

    def log(self, app, cont):
        """Logs the repeat actions.

        Actually, it just does nothing because instead, the repeated action
        will log itself everytime it is repeated.
        
        See [Action.execute] for description of arguments.
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        pass

    def execute(self, app, cont):
        """Repeats the last command in the command history [self.n_times].

        See [Action.execute] for description of arguments.
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute
        .. [self.n_times] file:///./actions_gen.ActionRepeatLastCmd.html"""
        
        (last_cont, last_action) = app.get_history(self, 1)
        for ii in range(self.n_times):
            last_action.log_execute(app, cont)

class ActionSelect(Action):
    """This action sets the selection in a buffer.

    **INSTANCE ATTRIBUTES**
    
    *(INT, INT) range* -- Start and end position of the range to
     be selected.

    *INT cursor_at=1* -- If positive, put cursor at end of
     selection. Otherwise, put it at beginning.

    *STR f_name=None* -- Name of file where to set selection. If
     *None*, selectin current buffer.
    
     **CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, range, cursor_at=1, f_name=None, **args_super):
        self.deep_construct(ActionSelect,
                            {'range': range, 'cursor_at': cursor_at,
                             'f_name': f_name},
                            args_super,
                            {})

    def execute(self, app, cont):
        """Selects a region in a buffer.

        See [Action.execute] for description of arguments.
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute
        .. [self.n_times] file:///./actions_gen.ActionRepeatLastCmd.html"""
        
        app.set_selection(range=self.range, cursor_at=self.cursor_at, f_name=self.f_name)
        
class ActionInsert(Action):
    """Action that inserts and indents code at cursor position
        
    **INSTANCE ATTRIBUTES**
        
    *ANY code_bef=''* -- undocumented
    *ANY code_after=''* -- undocumented
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
        
    def __init__(self, code_bef='', code_after='', **args_super):
        self.deep_construct(ActionInsert, \
                            {'code_bef': code_bef, \
                             'code_after': code_after}, \
                            args_super, \
                            {})
        
        
    def execute(self, app, cont):
        """See [Action.execute].
        
        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        
        app.insert_indent(self.code_bef, self.code_after)


    def doc(self):
        """
        
        **INPUTS**
        
        *none* -- 
        

        **OUTPUTS**
        
        *none* -- 
        """

        if self.docstring != None:
            the_doc = self.docstring
        else:
            the_doc = 'Inserts \'%s\' in current buffer' % (self.code_bef + '^' + self.code_after)
        return the_doc


class ActionSearch(Action):
    """Moves cursor to occurence of a regular expression.
        
    **INSTANCE ATTRIBUTES**
        
    *STR* regexp=None -- Regular expression to search for.

    *INT* direction=1 -- Direction of search. *Positive* means
     forward, *negative* means backward.                         
    
    *ANY* where=1 -- Place where to put cursor w.r.t. to
    *occurence. *Positive* means after occurence, *negative* means
    *before.

    *INT* num=1 -- Search for *num*th occurence.

    CLASS ATTRIBUTES**
        
    *none* -- 
    """
        
    def __init__(self, regexp=None, direction=1, num=1, where=1, **args_super):
        self.deep_construct(ActionSearch, \
                            {'regexp': regexp, \
                             'direction': direction, \
                             'num': num, \
                             'where': where}, \
                            args_super, \
                            {})



    def execute(self, app, cont):
        """See [Action.execute].

        .. [Action.execute] file:///./actions_gen.Action.html#execute"""
        
        app.search_for(regexp=self.regexp, direction=self.direction,
                       num=self.num, where=self.where)



    def doc(self):
        """See [Action.doc].

        .. [Action.doc] file:///./actions_gen.Action.html#doc
        """
        
        if self.docstring != None:
            the_doc = self.docstring
        else:
            if self.num == 1:
                if self.direction > 0:
                    str_occurence = 'to next occurence'
                else:
                    str_occurence = 'to previous occurence'
            else:
                if self.direction > 0:
                    str_dir = 'forward'
                else:
                    str_dir = 'backward'                
                str_occurence = '%s to occurence #%s' % (str_dir, self.num)
            if self.where > 0:
                str_where = ''
            else:
                str_where = ' Puts cursor after occurence.'
                
            the_doc = 'Moves %s of %s.%s' % (str_occurence, self.regexp, str_where)
        return the_doc

class ActionSearchInsert(Action):
    """Inserts some code after an occurence of a regexp
        
    **INSTANCE ATTRIBUTES**
        
    *STR regexp=None* -- The regexp to be searched for
        
    *STR to_insert=None* -- String to be inserted
        
    *INT direction=1* -- If *positive*, search forward. Otherwise,
    search backward.
        
    *INT num=1* -- Number of occurences to search for.
        
    *INT where=1* -- If *positive*, put cursor after
    occurence. Otherwise, put it before.

    *STR code_bef=''* -- Code to be inserted before cursor.

    *STR code_after=''* -- Code to be inserted after cursor.

    CLASS ATTRIBUTES**
        
    *none* -- 
    """
        
    def __init__(self, regexp=None, to_insert=None, direction=1, num=1, where=1, code_bef='', code_after='', **args_super):
        self.deep_construct(ActionSearchInsert, \
                            {'regexp': regexp, \
                             'to_insert': to_insert, \
                             'direction': direction, \
                             'num': num, \
                             'where': where, \
                             'code_bef': code_bef, \
                             'code_after': code_after}, \
                                args_super, \
                            {})



    def execute(self, app, cont):
        """See [Action.execute] for details.
        
        .. [Action.execute] file:///./Action.Action.html#execute"""
        
        app.search_for(regexp=self.regexp, direction=self.direction, num=self.num, where=self.where)
        app.insert_indent(code_bef=self.code_bef, code_after=self.code_after)


class ActionSwitchTranslation(Action):
    """Turns translation on/off
        
    **INSTANCE ATTRIBUTES**
        
    *BOOL* on -- If true, set translation to 'on'
        
    CLASS ATTRIBUTES**
        
    *none* -- 
    """
        
    def __init__(self, on=None, **args_super):
        self.deep_construct(ActionSearchInsert, \
                            {'on': on}, \
                                args_super, \
                            {})

    def execute(self, app, cont):
        """See [Action.execute] for details.
        
        .. [Action.execute] file:///./Action.Action.html#execute"""
        
        app.translation_is_off = not on


    def doc(self):
        if self.on:
            state = 'on'
        else:
            state = 'off'
        return 'turns translation \'%s\'' % state


#
# Index of the current anonymous action function.
#
anonymous_action_curr_num = 0

class AnonymousAction(exceptions.Exception):
    """Raised when the code for an anonymous action function has syntax errors"""

def indent_code(num, code):
    padding = ''
    for ii in range(num): padding = padding + ' '
    code = re.sub('(^|\n)', '\\1' + padding, code)
    return code

def anonymous_action(code, description):
    """This function creates an anonymous action function.

    The anonymous function gets an internal name of the form
    *anonymous_action_N* where *N* is some number.

    *STR code* -- Code for the anoymous action function. This code
     should assume that the application object is called *app*, and
     the context object is called *cont*.

    *STR description* -- Description of the action function
    """

    global anonymous_action_curr_num

    #
    # Create code for a new anymous action function *anonymous_action_N*
    # in a temporary file (for some reason, *exec* can't compile code
    # that declares a new function, whereas *execfile* can)
    #
    tmp_file_name = vc_globals.tmp + os.sep + 'tmp_anonymous_action.py'
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write('def anonymous_action_%s(app, cont):\n%s\n%s' % (anonymous_action_curr_num, indent_code(4, '"""' + description + '"""'), indent_code(4, code)))
    tmp_file.close()

    try:
        execfile(tmp_file_name)
        fct = eval('anonymous_action_%s' % anonymous_action_curr_num)
        anonymous_action_curr_num = anonymous_action_curr_num + 1
        return fct        
    except:
        raise AnonymousAction, 'Syntax error in code of anonymous action function.\Code was:\n%s\n' % code



###############################################################################
# Specific instances of generic actions
###############################################################################

gen_parens_pair = \
    ActionInsert(code_bef='(', code_after=')',
                 docstring="""Insert parens and puts cursor in between""")

gen_brackets_pair = \
    ActionInsert(code_bef='[', code_after=']',
                 docstring="""Insert brackets""")

gen_braces_pair = \
    ActionInsert(code_bef='{', code_after='}',
                 docstring="""Insert braces""")

gen_quotes_pair = \
    ActionInsert(code_bef='"', code_after='"',
                 docstring="""Insert quotes and moves cursor in between""")

gen_single_quotes_pair_after = \
    ActionInsert(code_bef='""', code_after='',
                 docstring="""Insert single quotes and moves cursor after""")

gen_single_quotes_pair = \
    ActionInsert(code_bef='\'', code_after='\'',
                 docstring="""Insert single quotes and moves cursor in between""")

gen_single_quotes_pair_after = \
    ActionInsert(code_bef='\'\'', code_after='',
                 docstring="""Insert single quotes and moves cursor after""")

gen_translation_off = \
    ActionSwitchTranslation(0)

gen_translation_on = \
    ActionSwitchTranslation(1)
