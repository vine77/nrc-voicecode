"""Context objects which are not tied to a specific language"""

from Context import Context

class ContLanguage(Context):
    """Context that applies only if a particular programming language is the
    active one.
    
    **INSTANCE ATTRIBUTES**
    
    *ANY language=None* -- Name of the programming language for this context. If *None*, then this context always applies.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, language=None, **args_super):
        self.deep_construct(ContLanguage, \
                            {'language': language}, \
                            args_super, \
                            {})

    def applies(self, app):
        buff = app.curr_buffer
        return (self.language == None or (buff != None and  buff.language == self.language))
        

class ContC(ContLanguage):
    """This context applies if current source buffer is in C.

    It is essentially a shortcut for ContLanguage(language='C')
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ContC, {}, args_super, enforce_value={'language': 'C'})


class ContPy(ContLanguage):
    """This context applies if current source buffer is in C.

    It is essentially a shortcut for ContLanguage(language='python')
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ContPy, {}, args_super, enforce_value={'language': 'python'})



class ContAny(Context):
    """This context always applies."""

    def __init__(self, **attrs):
        self.deep_construct(ContAny, {}, attrs)
        
    def applies(self, app):
        return 1
