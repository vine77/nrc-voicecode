def __setattr__(self, name, value):
    if (self.__dict__.has_key(name)):
        self.__dict__[name] = value
    else:
        raise(AttributeError)
