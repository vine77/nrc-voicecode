import cPickle, exceptions
import Object

class PickledObject(Object.Object):
    """
    Class for an object that can pickle/unpickle itself to a file.
    
    **INSTANCE ATTRIBUTES**
    
    *STR pickle_fname=None* -- Name of the file to/from which the file is to be
    pickled/unpickled.

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, pickle_fname=None, **args_super):

        #
        # First, create a pickle_fname attribute, so that unpickle can access it
        #
        self.decl_attrs({'pickle_fname': pickle_fname})
        
        #
        # Then override values read from pickle file, with values received
        # as arguments
        #
        self.deep_construct(PickledObject, \
                            {'pickle_fname': pickle_fname}, \
                            args_super, \
                            {})

    def pickle(self):
        """Saves the object to file.

        Name of file is *self.pickle_fname*. If *None*,don't write to file.
        
        **INPUTS**
        
        *none* -- 
        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- PickledObject.pickle:  self.pickle_fname=%s' % self.pickle_fname
        
        if self.pickle_fname != None:
            try:
                a_file = open(self.pickle_fname, 'w')
                cPickle.dump(self, a_file)
                a_file.close()
            except exceptions.Exception, mess:
                print 'Error writing %s to file \'%s\'\n%s' % (self, self.pickle_fname, mess)


    def unpickle(self):
        """Reads the object from file.

        Name of the file is *self.pickle_fname*. If *None* don't read from
        file.
        
        **INPUTS**
        
        *STR fname=None* -- Name of the from which to read the
        instance. If *None*, use 
        

        **OUTPUTS**
        
        *none* -- 
        """

#        print '-- PickledObject.unpickle: self.pickle_fname=%s' % self.pickle_fname
        
        if self.pickle_fname != None:
            try:
                orig_pickle_fname = self.pickle_fname
                a_file = open(self.pickle_fname, 'r')
                tmp = cPickle.load(a_file)
                a_file.close()
                self.__dict__ = tmp.__dict__
                
                #
                # Override value of self.pickle_fname which was read from file
                #
                self.pickle_fname = orig_pickle_fname
            except exceptions.Exception, mess:
                print 'Error reading %s from file \'%s\'\n%s' % (self, self.pickle_fname, mess)



