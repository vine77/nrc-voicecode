import auto_test, exceptions, os, posixpath, profile, sys

class Object:
    """A base class for objects with safe attribute access methods

    This class defines a safe *__setattr__* method, which raise an
    exception when trying to set the value of an inexistant attribute.

    For performance reasons, these safe attribute setting methods are
    only invoked if environment variable *$PY_DEBUG_OBJECT=1*.

    Note that this class does not define a safe *__getattr__*
    method because Python already raises an exception when trying to
    get the value of an inexistant attribute.

    Profile tests on NT indicate that:

    - the speed of constructors for Object and non-Object instances are the same
    - the speed of attribute *gets* is the same for Object and non-Object instances
    - when *$PY_DEBUG_OBJECT=0*, the performance of attribute *sets* is the same for Object and non-Object instances
    - when *$PY_DEBUG_OBJECT=1*, attribute *sets* are slower by a factor of about 15 for Object instances than for non-Object instances

    **TEMPLATE CONSTRUCTOR**

    Constructors for each of the subclasses of *Object* are
    responsible for adding an entry in *self.__dict__* corresponding
    to the attributes defined by that class (otherwise those
    attributes will be considered as undefined by the safe
    *__setattr__* method)

    You can do this using the [def_attrs] method.

    Note however that Python does not automatically invoke the
    constructor of every superclass of a class, so your constructor
    should do this explicitly. Below is a template constructor.

    Example:

       class AClass(Super1, ..., SuperN):
          def __init__(self, attr1=val1, ..., attrN=valN, **attrs):
             Super1.__init__(self)
             ...
             SuperN.__init__(self)
             self.def_attrs({'attr1': attr1, ..., 'attrN': attrN}
             self.init_attrs(attrs)

    Where *attr1, ..., attrN* are the new attributes defined by
    *AClass*, and *val1, ..., valN* are their default values. 
                         
    This guarantees that in the end, you have an instance of *AClass*
    with *all* attributes (i.e. attributes for this class and all superclasses)
    defined and set to their default values.

    Note the use of dictionary *attrs*. This dictionary collects
    additional attribute names and values which are then passed to
    method [init_attrs] to initialise attributes defined by
    superclasses of *AClass*. Thus if *AClass* is a subclass of
    *Super1* and if *Super1* defines attribute *blah*, then you can
    construct an instance of *AClass* with *blah=1* using the statement:

    *x = AClass(blah=1)*

    without the constructor of *AClass* having to know explicitly
    about attribute *blah*.
                       
    Note that the file *Admin/python.el* contains an Emacs macro
    *py-obclass* which automatically types this kind of template code
    for a class and its constructor

    **INSTANCE ATTRIBUTE**

    *none* --

    **CLASS ATTRIBUTE**

    *none* --

    .. [def_attrs] file:///./Object.Object.html#Object.Object.def_attrs
   .. [init_attrs] file:///Object.Object.html#Object.Object.init_attrs"""


    #
    # Safe __setattr__ method is defined in file 'safe_setattr.py'.
    # Load it only if environment variable PY_DEBUG_OBJECT=1
    #
    if (os.environ.has_key('PY_DEBUG_OBJECT') and (os.environ['PY_DEBUG_OBJECT'] != '0')):
        code_file = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Mediator' + os.sep + 'safe_setattr.py')
        execfile(code_file)


    def __init__(self):
        pass
    
    def def_attrs(self, attrs):
        """Define new attributes for *self*

        Attributes are set even if they do not exist in
        *self.__dict__*.

        **INPUTS**

        *{STR: ANY}* attrs -- dictionary with attribute name as the keys and
         default values as the values.

        **OUTPUTS**

        *none* -- 
        """
        for an_attr_def in attrs.items():
            self.__dict__[an_attr_def[0]] = an_attr_def[1]        

    def init_attrs(self, attrs):
        """Initialises existing attributes

        Attributes are only set if they already exist in
         *self.__dict__*. Otherwise, an *AttributeError* exception is
         raised.
        
        **INPUTS**

        *{STR: ANY}* attrs -- dictionary with attribute name as the keys and
         default values as the values.

        **OUTPUTS**

        *none* -- 
        """
        for an_attr_init in attrs.items():
            setattr(self, an_attr_init[0], an_attr_init[1])


    
class SmallObject(Object):
    """A test object with few attributes

    This class is used to profile the performance of access methods
    when accessing attribute from a small Object subclass.

    **INSTANCE ATTRIBUTE**

    *STR* name --
    *INT* age --

    **CLASS ATTRIBUTE**
    
    *none* -- 
    """
    def __init__(self, name="Alain", age=36):
        """Constructor

        **INPUTS**

        *STR* name="Alain" -- undocumented 

        *INT* age=36 -- undocumented 


        **OUTPUTS**

        *none* -- 
        """
        self.__dict__['name'] = name
        self.__dict__['age'] = age

class LargeObject(Object):
    """A test object with many attributes

    This class is used to profile the performance of access methods
    when accessing attributes of a large Object subclass.

    **INSTANCE ATTRIBUTE**

    *STR* name --
    *INT* age --
    *INT* attr1, ..., attr20 --

    **CLASS ATTRIBUTE**

    *none* -- 
    """

    def __init__(self, name="Alain", age="36"):
        """Constructor

        **INPUTS**

        *ANY* name="Alain" -- undocumented 

        *ANY* age="36" -- undocumented 


        **OUTPUTS**

        *none* -- 
        """
        self.__dict__['name'] = name
        self.__dict__['age'] = age
        self.__dict__['attr1'] = 1
        self.__dict__['attr2'] = 1
        self.__dict__['attr3'] = 1
        self.__dict__['attr4'] = 1
        self.__dict__['attr5'] = 1
        self.__dict__['attr6'] = 1
        self.__dict__['attr7'] = 1
        self.__dict__['attr8'] = 1
        self.__dict__['attr9'] = 1
        self.__dict__['attr10'] = 1
        self.__dict__['attr11'] = 1
        self.__dict__['attr12'] = 1
        self.__dict__['attr13'] = 1
        self.__dict__['attr14'] = 1
        self.__dict__['attr15'] = 1
        self.__dict__['attr16'] = 1
        self.__dict__['attr17'] = 1
        self.__dict__['attr18'] = 1
        self.__dict__['attr19'] = 1
        self.__dict__['attr20'] = 1        

class SmallNonObject:
    """A \"raw\" test object with many attributes.

    This class is used to profile the performance of attribute access
    methods for large objects which are not subclasses of Object.

    **INSTANCE ATTRIBUTE**

    *STR* name --
    *INT* age --

    **CLASS ATTRIBUTE**

    *none* -- 
    """

    def __init__(self, name="Alain", age=36):
        """Constructor

        **INPUTS**

        *STR* name="Alain" -- undocumented 

        *INT* age=36 -- undocumented 


        **OUTPUTS**

        *none* -- 
        """
        self.__dict__['name'] = 'Alain'
        self.__dict__['age'] = 36

class LargeNonObject:
    """A \"raw\" test object with many attributes.

    This class is used to profile the performance of attribute access
    methods for large objects which are not subclasses of Object.

    **INSTANCE ATTRIBUTE**

    *STR* name --
    *INT* age --
    *INT* attr1, ..., attr20 --

    **CLASS ATTRIBUTE**

    *none* -- 
    """

    def __init__(self, name="Alain", age=36):
        """Constructor

        **INPUTS**

        *STR* name="Alain" -- undocumented 

        *INT* age=36 -- undocumented 


        **OUTPUTS**

        *none* -- 
        """
        self.__dict__['name'] = name
        self.__dict__['age'] = age
        self.__dict__['attr1'] = 1
        self.__dict__['attr2'] = 1
        self.__dict__['attr3'] = 1
        self.__dict__['attr4'] = 1
        self.__dict__['attr5'] = 1
        self.__dict__['attr6'] = 1
        self.__dict__['attr7'] = 1
        self.__dict__['attr8'] = 1
        self.__dict__['attr9'] = 1
        self.__dict__['attr10'] = 1
        self.__dict__['attr11'] = 1
        self.__dict__['attr12'] = 1
        self.__dict__['attr13'] = 1
        self.__dict__['attr14'] = 1
        self.__dict__['attr15'] = 1
        self.__dict__['attr16'] = 1
        self.__dict__['attr17'] = 1
        self.__dict__['attr18'] = 1
        self.__dict__['attr19'] = 1
        self.__dict__['attr20'] = 1
        
def profConstrSmallObj(num_times):
    """Profile performance of constructor

    This method profiles the performance of constructors for classes
    that *are* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the constructor 

    **OUTPUTS**

    *none* -- 
    """
    for index in range(num_times):
        obj = SmallObject(name='Janet', age=42)

def profConstrLargeObj(num_times):
    """Profile performance of constructor

    This method profiles the performance of constructors for classes
    that *are* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the constructor

    **OUTPUTS**

    *none* -- 
    """
    for index in range(num_times):
        obj = LargeObject(name='Janet', age=42)

def profConstrSmallNonObj(num_times):
    """Profile performance of constructor

    This method profiles the performance of constructors for classes
    that *are not* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the constructor 

    **OUTPUTS**

    *none* -- 
    """
    for index in range(num_times):
        obj = SmallNonObject(name='Janet', age=42)

def profConstrLargeNonObj(num_times):
    """Profile performance of constructor

    This method profiles the performance of constructors for classes
    that *are not* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the constructor 

    **OUTPUTS**

    *none* -- 
    """
    for index in range(num_times):
        obj = LargeNonObject(name='Janet', age=42)


def profGetSmallObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *get*  classes
    that *are* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = SmallObject(name='Janet', age=42)
    for index in range(num_times):
        her_age = obj.age


def profGetLargeObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *get*  classes
    that *are* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = LargeObject(name='Janet', age=42)
    for index in range(num_times):
        her_age = obj.age

def profGetSmallNonObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *get*  classes
    that *are not* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = SmallNonObject(name='Janet', age=42)
    for index in range(num_times):
        her_age = obj.age

def profGetLargeNonObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *get*  classes
    that *are not* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = LargeNonObject(name='Janet', age=42)
    for index in range(num_times):
        her_age = obj.age

def profSetSmallObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *set*  classes
    that *are* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = SmallObject(name='Janet', age=42)
    for index in range(num_times):
        obj.age = 1

def profSetLargeObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *set*  classes
    that *are* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = LargeObject(name='Janet', age=42)
    for index in range(num_times):
        obj.age = 1

def profSetSmallNonObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *set*  classes
    that *are not* subclasses of Object and have *few* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = SmallNonObject(name='Janet', age=42)
    for index in range(num_times):
        obj.age = 1                

def profSetLargeNonObj(num_times):
    """Profile performance of attribute *get*

    This method profiles the performance of attribute *set*  classes
    that *are not* subclasses of Object and have *many* attributes

    **INPUTS**

    *INT* num_times -- number of times to invoke the get 

    **OUTPUTS**

    *none* -- 
    """

    obj = LargeNonObject(name='Janet', age=42)
    for index in range(num_times):
        obj.age = 1                


def profObject(num_times):
    """Profile the performance of the Object class

    **INPUTS**

    *INT* num_times -- number of times to carry out the various tests


    **OUTPUTS**

    *none* -- 
    """
    profConstrSmallObj(num_times)
    profConstrLargeObj(num_times)
    profConstrSmallNonObj(num_times)
    profConstrLargeNonObj(num_times)
    profGetSmallObj(num_times)
    profGetLargeObj(num_times)
    profGetSmallNonObj(num_times)
    profGetLargeNonObj(num_times)	
    profSetSmallObj(num_times)
    profSetLargeObj(num_times)
    profSetSmallNonObj(num_times)
    profSetLargeNonObj(num_times)

def try_attribute(obj, name, operation):
    """Test setting/getting attributes

    **INPUTS**

    *ANY* obj -- object on which we will get/set attributes 

    *STR* name -- name of attribute to get/set 

    *STR* operation -- *'get'* or *'set'*

    **OUTPUTS**

    *none* -- 
    """
    sys.stdout.write("\nTrying to %s the value of attribute '%s'\n   -> " % (operation, name))
    if (operation == 'set'):
        code = "obj." + name + " = '999'"
    else:
        code = "x = obj." + name
    x = 0
    try:
        exec(code)
    except AttributeError, exc:
        sys.stdout.write("Caught AttributeError exception: '%s'" % [exc.__dict__])
    else:
        sys.stdout.write("Caught NO AttributeError exception. ")
        str = "obj.%s=%s, x=%s" % (name, obj.name, x)
        sys.stdout.write(str)
    sys.stdout.write("\n\n")
        

def prof_test():
    sys.stdout.write('\n$PY_DEBUG_OBJECT is: ')
    if (os.environ.has_key('PY_DEBUG_OBJECT')):
        sys.stdout.write(os.environ['PY_DEBUG_OBJECT'])
    else:
        sys.stdout.write('not defined')
    sys.stdout.write("\n\n")

    sys.stdout.write("Profiling speed of Object constructor/get/set.\n\n")
    profile.run("profObject(1000)")
#    profObject(1000)

def self_test():
    obj = SmallObject()

    sys.stdout.write("Testing exceptions for get/set\n\n")
    try_attribute(obj, 'name', 'get')
    try_attribute(obj, 'name', 'set')
    try_attribute(obj, 'nonexistant', 'get')
    try_attribute(obj, 'nonexistant', 'set')

auto_test.add_test('Object', self_test, 'self-test for Object.py')

if (__name__ == "__main__"):
    self_test()
    prof_test()
			

