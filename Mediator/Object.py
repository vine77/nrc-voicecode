# import sys
# import os
# import profile

#  class Object:
#  	"""A base class for objects with safe attribute access methods

#  This class defines attribute *setting* methods, which raise an exception when trying to set the value of an inexistant attribute.

#  For performance reasons, these safe attribute setting methods are only invoked if environment variable *PY_DEBUG_OBJECT* is set to 1.

#  Note that this class does not define safe attribute *getting* methods because Python already raises an exception when trying to get the value of an inexistant attribute.
#  	"""
	
#  	if (os.environ.has_key('PY_DEBUG_OBJECT') and (os.environ['PY_DEBUG_OBJECT'] != '0')):
#  		sys.stdout.write('Using safe attribute setting method\n')
#  		execfile('D:\VoiceCode\PythonExamples\safe_setattr.py')
	
			
#  class SmallObject(Object):
#  	"""A test object with few attributes

#  This class is used to profile the performance of access methods when accessing attribute from a small Object subclass.
#  	"""

#  	def __init__(self, name="Alain", age=36):
#  		self.__dict__['name'] = name
#  		self.__dict__['age'] = age

#  class LargeObject(Object):
#  	"""A test object with many attributes

#  This class is used to profile the performance of access methods when accessing attributes of a large Object subclass.
#  	"""

#  	def __init__(self, name="Alain", age=36):
#  		self.__dict__['name'] = name
#  		self.__dict__['age'] = age
#  		self.__dict__['attr1'] = 1
#  		self.__dict__['attr2'] = 1
#  		self.__dict__['attr3'] = 1
#  		self.__dict__['attr4'] = 1
#  		self.__dict__['attr5'] = 1
#  		self.__dict__['attr6'] = 1
#  		self.__dict__['attr7'] = 1
#  		self.__dict__['attr8'] = 1
#  		self.__dict__['attr9'] = 1
#  		self.__dict__['attr10'] = 1
#  		self.__dict__['attr11'] = 1
#  		self.__dict__['attr12'] = 1
#  		self.__dict__['attr13'] = 1
#  		self.__dict__['attr14'] = 1
#  		self.__dict__['attr15'] = 1
#  		self.__dict__['attr16'] = 1
#  		self.__dict__['attr17'] = 1
#  		self.__dict__['attr18'] = 1
#  		self.__dict__['attr19'] = 1
#  		self.__dict__['attr20'] = 1

#  class SmallNonObject:
#  	"""A \"raw\" test object with few attributes.

#  This class is used to profile the performance of access methods for small objects which are not subclasses of Object.
#  	"""

#  	def __init__(self, name="Alain", age=36):
#  		self.name = name
#  		self.age = age

#  class LargeNonObject(Object):
#  	"""A \"raw\" test object with many attributes.

#  This class is used to profile the performance of attribute access methods for large objects which are not subclasses of Object.
#  	"""

	
#  	def __init__(self, name="Alain", age=36):
#  		self.__dict__['name'] = name
#  		self.__dict__['age'] = age
#  		self.__dict__['attr1'] = 1
#  		self.__dict__['attr2'] = 1
#  		self.__dict__['attr3'] = 1
#  		self.__dict__['attr4'] = 1
#  		self.__dict__['attr5'] = 1
#  		self.__dict__['attr6'] = 1
#  		self.__dict__['attr7'] = 1
#  		self.__dict__['attr8'] = 1
#  		self.__dict__['attr9'] = 1
#  		self.__dict__['attr10'] = 1
#  		self.__dict__['attr11'] = 1
#  		self.__dict__['attr12'] = 1
#  		self.__dict__['attr13'] = 1
#  		self.__dict__['attr14'] = 1
#  		self.__dict__['attr15'] = 1
#  		self.__dict__['attr16'] = 1
#  		self.__dict__['attr17'] = 1
#  		self.__dict__['attr18'] = 1
#  		self.__dict__['attr19'] = 1
#  		self.__dict__['attr20'] = 1

#  #
#  # Used to profile the performance of constructor for classes
#  # that are subclasses of Object (both large and small)
#  #
#  def profConstrSmallObj(num_times):
#          """Profile performance of constructor

#  	This method profiles the performance of constructors for classes that 
#  	are subclasses of Object (both large and small)

#  -	num_times: number of times to do the attribute accesses.

#  -       blah: an other one
#  	"""
#    	for index in range(num_times):
#    		obj = SmallObject(name='Janet', age=42)
#  def profConstrLargeObj(num_times):
#    	for index in range(num_times):
#    		obj = LargeObject(name='Janet', age=42)

#  #
#  # Used to profile the performance of constructor
#  # of instances that are not subclasses of Object (large and small)
#  #
#  def profConstrSmallNonObj(num_times):
#          """Profile performance of constructor

#  	This method profiles the performance of constructors for classes that 
#  	are subclasses of Object (both large and small)

#  -	num_times: number of times to do the attribute accesses.
#    	for index in range(num_times):
#    		obj = SmallNonObject(name='Janet', age=42)
#  def profConstrLargeNonObj(num_times):
#    	for index in range(num_times):
#    		obj = LargeNonObject(name='Janet', age=42)

#  #
#  # Used to profile the performance of attribute gets for Objects
#  # (large and small)
#  #
#  def profGetSmallObj(num_times):
#  	obj = SmallObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		her_age = obj.age
#  def profGetLargeObj(num_times):
#  	obj = LargeObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		her_age = obj.age

#  #
#  # Used to profile the performance of attribute gets for non Objects
#  # (large and small)
#  #
#  def profGetSmallNonObj(num_times):
#  	obj = SmallNonObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		her_age = obj.age
#  def profGetLargeNonObj(num_times):
#  	obj = LargeNonObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		her_age = obj.age		

#  #
#  # Used to profile the performance of attribute sets for Objects
#  # (large and small)
#  #
#  def profSetSmallObj(num_times):
#  	obj = SmallObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		obj.age = 1
#  def profSetLargeObj(num_times):
#  	obj = LargeObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		obj.age = 1

#  #
#  # Used to profile the performance of attribute sets for non Objects
#  # (large and small)
#  #
#  def profSetSmallNonObj(num_times):
#  	obj = SmallNonObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		obj.age = 1
#  def profSetLargeNonObj(num_times):
#  	obj = LargeNonObject(name='Janet', age=42)
#  	for index in range(num_times):
#  		obj.age = 1


#  #
#  # Used to profile the performance of various Object operations.
#  #
#  def profObject(num_times):
#  	sys.stdout.write('\nPY_DEBUG_OBJECT=\'%s\'\n\n' % os.environ['PY_DEBUG_OBJECT'])
#  	profConstrSmallObj(num_times)
#  	profConstrLargeObj(num_times)
#  	profConstrSmallNonObj(num_times)
#  	profConstrLargeNonObj(num_times)
#  	profGetSmallObj(num_times)
#  	profGetLargeObj(num_times)
#  	profGetSmallNonObj(num_times)
#  	profGetLargeNonObj(num_times)	
#  	profSetSmallObj(num_times)
#  	profSetLargeObj(num_times)
#  	profSetSmallNonObj(num_times)
#  	profSetLargeNonObj(num_times)

#  #
#  # Used to test attribute setting/getting methods
#  #
#  def try_attribute(obj, name, operation):
#  	sys.stdout.write("\nTrying to %s the value of attribute '%s'\n   -> " % (operation, name))
#  	if (operation == 'set'):
#  		code = "obj." + name + " = '999';sys.stdout.write('obj.' + obj." + name + ")"
#  	else:
#  		code = "sys.stdout.write(obj." + name + ")"
#  #	sys.stdout.write('code=%s\n', (code))
#  	sys.stdout.write('code=' + code + '\n')
#  	try:
#  		exec(code)
#  	except:
#  		"Raised exception\n"
#  	else:
#  		"NO exception raised\n"
			
#  if (__name__ == "__main__"):

#  	obj.age = 1
#	obj.age = obj.nonexistant
#	obj.nonexistant = 2
#  	sys.stdout.write('PY_DEBUG_OBJECT environment variable is: ')
#  	if (os.environ.has_key('PY_DEBUG_OBJECT')):
#  		sys.stdout.write('defined\n')
#  	else:
#  		sys.stdout.write('NOT defined\n')
	
#          profile.run("profObject(10)")

#  	obj = SmallObject()
#  	try_attribute(obj, 'age', 'get')
#  	try_attribute(obj, 'age', 'set')
#  	try_attribute(obj, 'nonexistant', 'get')
#  	try_attribute(obj, 'nonexistant', 'set')
