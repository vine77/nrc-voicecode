"""Context objects which are not tied to a specific language"""

from Context import Context

class ContC(Context):
    """This context applies if current source buffer is in C."""
    
    def __init__(self, **attrs):
        self.deep_construct(ContC, {}, attrs)

    def applies(self, app):
        buff = app.curr_buffer
        return (buff != None and  buff.language == 'C')


class ContPy(Context):
    """This context applies if current source buffer is in Python."""
    
    def __init__(self, **attrs):
        self.deep_construct(ContPy, {}, attrs)

    def applies(self, app):
        buff = app.curr_buffer
        return (buff != None and  buff.language == 'python')


class ContAny(Context):
    """This context always applies."""

    def __init__(self, **attrs):
        self.deep_construct(ContAny, {}, attrs)
        
    def applies(self, app):
        return 1
