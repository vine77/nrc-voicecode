"""Action functions that span different languages"""

import exceptions, os, re
import Object, vc_globals

class Action(Object.Object):
    """Base class for all actions.
    
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

    def execute(self, app, app_cont):
        """Execute the action.
        
        **INPUTS**
        
        [AppState] app -- Application on which to execute the action
        
        [Context] app_cont -- Context of the application that is
        relevant for the execution of this action.
        
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

