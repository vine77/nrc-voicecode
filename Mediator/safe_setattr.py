
def __setattr__(self, name, value):
#    sys.stdout.write('calling safe __setattr__\n')
    if (self.__dict__.has_key(name)):
#        sys.stdout.write("attribute '%s' exists\n" % (name))
        self.__dict__[name] = value
    else:
#        sys.stderr.write("ERROR: Could not SET attribute '" + name + "'\n")
        throw('attr_set')
