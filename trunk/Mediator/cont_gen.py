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


class ContPerl(ContLanguage):
    """This context applies if current source buffer is in Perl.

    It is essentially a shortcut for ContLanguage(language='perl')
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ContPerl, {}, args_super, enforce_value={'language': 'perl'})

class ContPy(ContLanguage):
    """This context applies if current source buffer is in Python.

    It is essentially a shortcut for ContLanguage(language='python')
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ContPy, {}, args_super, enforce_value={'language': 'python'})


class ContAny(Context):
    """This context always applies, UNLESS translation is off."""

    def __init__(self, **attrs):
        self.deep_construct(ContAny, {}, attrs)
        
    def applies(self, app):
        return not app.translation_is_off

class ContLastActionWas(Context):
    """This context applies if the last action application's command history
    was of a certain type"""

    def __init__(self, type, **attrs):
        """**INPUTS**

        *CLASS* type -- A class object (not instance). The context applies if
        the last action is an instance of a class that is a descendant (not
        necessarily direct) of class *type*.
        """
        
        self.deep_construct(ContAny, {'type': type}, attrs)
        
    def applies(self, app):
        (last_cont, last_action) = app.get_history(1)
        return isinstance(last_action, self.type)


class ContAnyEvenOff(Context):
    """This context always applies, EVEN IF translation is off."""

    def __init__(self, **attrs):
        self.deep_construct(ContAnyEvenOff, {}, attrs)
        
    def applies(self, app):
        return 1


class ContTranslationOff(Context):
    """This context only applies when translation of commands is 'off'
    
    **INSTANCE ATTRIBUTES**
    
    *none*-- 
    
    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, **args_super):
        self.deep_construct(ContTranslationOff, \
                            {}, \
                            args_super, \
                            {})
    def applies(self, app):
        return app.translation_is_off

