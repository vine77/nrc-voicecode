"""Safe __setattr__ function which checks for existance of attribute before setting it."""

def __setattr__(self, name, value):
    
    """Safe __setattr__ function which checks for existance of
    attribute before setting it."""
    
    if (self.__dict__.has_key(name)):
        self.__dict__[name] = value
    else:
        exc = AttributeError()
        exc.args=(name)
        raise(exc)
