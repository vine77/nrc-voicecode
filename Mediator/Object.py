import exceptions, os, posixpath, profile, sys

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
    - when *$PY_DEBUG_OBJECT=1*, attribute *sets* are about 150% slower for Object instances than for non-Object instances

    **INSTANCE ATTRIBUTE**

    *none* --

    **CLASS ATTRIBUTE**

    *none* --     
    """

    if (os.environ.has_key('PY_DEBUG_OBJECT') and (os.environ['PY_DEBUG_OBJECT'] != '0')):
        code_file = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Mediator' + os.sep + 'safe_setattr.py')
        execfile(code_file)
	
    
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

        *untyped* name="Alain" -- undocumented 

        *untyped* age="36" -- undocumented 


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

    *untyped* obj -- object on which we will get/set attributes 

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
    except AttributeError:
        sys.stdout.write("Caught AttributeError exception.")
    else:
        sys.stdout.write("Caught NO AttributeError exception. ")
        str = "obj.%s=%s, x=%s" % (name, obj.name, x)
        sys.stdout.write(str)
    sys.stdout.write("\n\n")
        

			
if (__name__ == "__main__"):

    sys.stdout.write('\n$PY_DEBUG_OBJECT is: ')
    if (os.environ.has_key('PY_DEBUG_OBJECT')):
        sys.stdout.write(os.environ['PY_DEBUG_OBJECT'])
    else:
        sys.stdout.write('not defined')
    sys.stdout.write("\n\n")

    sys.stdout.write("Profiling speed of Object constructor/get/set.\n\n")
    profile.run("profObject(1000)")

    obj = SmallObject()

    sys.stdout.write("Testing exceptions for get/set\n\n")
    try_attribute(obj, 'name', 'get')
    try_attribute(obj, 'name', 'set')
    try_attribute(obj, 'nonexistant', 'get')
    try_attribute(obj, 'nonexistant', 'set')

