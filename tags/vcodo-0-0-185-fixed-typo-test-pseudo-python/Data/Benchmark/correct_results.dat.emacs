creating wxMediator
Loading test definitions...
Configuring the mediator...
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Finished wxMediator init...
starting...
Starting server threads...
universal instance named "emacs(0)"


*******************************************************************************
* Name        : CmdInterp
* Description : self-test for CmdInterp.py
*******************************************************************************

EdSim instance EdSim(0) connected


>>> Testing command interpreter



>>> Interpreting in a C buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: <CURSOR>
  4: void move(float x, y)
  5: {
  6:   move_horiz(x);
>>> Interpreting: ['for loop', 'loop body']
>>> Interpreting: ['for', 'loop', 'loop', 'body']

>>> Buffer is now:
  4:    {
  5: for (=0;  <= ; ++)
  6:    {
  7: <CURSOR>   
  8:    }
  9:    
 10:    }

>>> Interpreting in a Python buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: # This is a small test buffer for Python
  2: 
  3: 
  4: <CURSOR>
  5: class AClass(ASuper):
  6:     """This is a dummy class"""
  7:     
>>> Interpreting: ['for loop', 'loop body']

>>> Buffer is now:
  2: 
  3: 
  4: for :
  5:    <CURSOR>
  6: class AClass(ASuper):
  7:     """This is a dummy class"""
  8:     


*******************************************************************************
* Name        : EdSim
* Description : self-test for EdSim.py
*******************************************************************************

>>> Testing EdSim.py


>>> Opening a buffer
*** Start of source buffer ***
  1: <CURSOR>/* This is a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)


>>> Moving to position 5
*** Start of source buffer ***
  1: /* Th<CURSOR>is is a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)


>>> Testing breadcrumbs

>>> Dropping one here
*** Start of source buffer ***
  1: /* Th<CURSOR>is is a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)

>>> Dropping one here
*** Start of source buffer ***
  1: /* This is<CURSOR> a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)

>>> Popping 2 crumbs -> end up here:
*** Start of source buffer ***
  1: /* Th<CURSOR>is is a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)

>>> Dropping one here
*** Start of source buffer ***
  1: /* Th<CURSOR>is is a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)

>>> Dropping one here
*** Start of source buffer ***
  1: /* This is<CURSOR> a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)
*** Start of source buffer ***
  1: /* This is a small t<CURSOR>est buffer for C */
  2: 
  3: 
  4: void move(float x, y)

>>> Popping 1 crumb -> end up here...
*** Start of source buffer ***
  1: /* This is<CURSOR> a small test buffer for C */
  2: 
  3: 
  4: void move(float x, y)


>>> Testing code indentation. Inserting for loop.
  3: 
  4: for (ii=0; ii <= maxValue; ii++)
  5: {
  6: <CURSOR>
  7: }
  8: void move(float x, y)
  9: {


*******************************************************************************
* Name        : EdSim_alloc_cleanup
* Description : Testing EdSim allocation and cleanup.
*******************************************************************************


*** testing cleanup with single buffer EdSim

EdSim.__init__
SourceBuff.__init__: 
EdSim instance EdSim(0) connected
SourceBuff.remove_other_references: 
SourceBuff.__del__: 
SourceBuff.__init__: %VCODE_HOME%\Data\TestData\small_buff.c


>>> Testing command interpreter



>>> Interpreting in a C buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: <CURSOR>
  4: void move(float x, y)
  5: {
  6:   move_horiz(x);
>>> Interpreting: ['for loop', 'loop body']
>>> Interpreting: ['for', 'loop', 'loop', 'body']

>>> Buffer is now:
  4:    {
  5: for (=0;  <= ; ++)
  6:    {
  7: <CURSOR>   
  8:    }
  9:    
 10:    }
SourceBuff.remove_other_references: %VCODE_HOME%\Data\TestData\small_buff.c
SourceBuff.__del__: %VCODE_HOME%\Data\TestData\small_buff.c
SourceBuff.__init__: %VCODE_HOME%\Data\TestData\small_buff.py

>>> Interpreting in a Python buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: # This is a small test buffer for Python
  2: 
  3: 
  4: <CURSOR>
  5: class AClass(ASuper):
  6:     """This is a dummy class"""
  7:     
>>> Interpreting: ['for loop', 'loop body']

>>> Buffer is now:
  2: 
  3: 
  4: for :
  5:    <CURSOR>
  6: class AClass(ASuper):
  7:     """This is a dummy class"""
  8:     
EdSim.remove_other_references
SourceBuff.remove_other_references: %VCODE_HOME%\Data\TestData\small_buff.py
SourceBuff.__del__: %VCODE_HOME%\Data\TestData\small_buff.py
EdSim.__del__

*** testing cleanup with multi-buffer EdSim

EdSim.__init__
SourceBuff.__init__: 
EdSim instance EdSim(0) connected
SourceBuff.__init__: %VCODE_HOME%\Data\TestData\small_buff.c


>>> Testing command interpreter



>>> Interpreting in a C buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: <CURSOR>
  4: void move(float x, y)
  5: {
  6:   move_horiz(x);
>>> Interpreting: ['for loop', 'loop body']
>>> Interpreting: ['for', 'loop', 'loop', 'body']

>>> Buffer is now:
  4:    {
  5: for (=0;  <= ; ++)
  6:    {
  7: <CURSOR>   
  8:    }
  9:    
 10:    }
SourceBuff.__init__: %VCODE_HOME%\Data\TestData\small_buff.py

>>> Interpreting in a Python buffer

>>> Current buffer is:

*** Start of source buffer ***
  1: # This is a small test buffer for Python
  2: 
  3: 
  4: <CURSOR>
  5: class AClass(ASuper):
  6:     """This is a dummy class"""
  7:     
>>> Interpreting: ['for loop', 'loop body']

>>> Buffer is now:
  2: 
  3: 
  4: for :
  5:    <CURSOR>
  6: class AClass(ASuper):
  7:     """This is a dummy class"""
  8:     
EdSim.remove_other_references
SourceBuff.remove_other_references: %VCODE_HOME%\Data\TestData\small_buff.c
SourceBuff.__del__: %VCODE_HOME%\Data\TestData\small_buff.c
SourceBuff.remove_other_references: %VCODE_HOME%\Data\TestData\small_buff.py
SourceBuff.__del__: %VCODE_HOME%\Data\TestData\small_buff.py
SourceBuff.remove_other_references: 
SourceBuff.__del__: 
EdSim.__del__


*******************************************************************************
* Name        : Object
* Description : self-test for Object.py
*******************************************************************************

Testing exceptions for get/set


Trying to get the value of attribute 'name', $PY_DEBUG_OBJECT=None
   -> Caught NO AttributeError exception. obj.name=Alain, x=Alain


Trying to set the value of attribute 'name', $PY_DEBUG_OBJECT=None
   -> Caught NO AttributeError exception. obj.name=999, x=0


Trying to get the value of attribute 'nonexistant', $PY_DEBUG_OBJECT=None
   -> Caught AttributeError exception: '[{'args': ('nonexistant',)}]'


Trying to set the value of attribute 'nonexistant', $PY_DEBUG_OBJECT=None
   -> Caught NO AttributeError exception. obj.nonexistant=999, x=0

Testing inheritance of constructor arguments
   Employee1(name='Alain', salary='not enough') -> {'salary': 'not enough', 'name': 'Alain', 'citizenship': None}


Redefining default value of *citizenship*
   MyPerson(name='Alain') -> result={'salary': 'not enough', 'name': 'Alain', 'citizenship': None}

Overriding redefined default value of *citizenship*
   MyPerson(name='Alain', citizenship='US citizen') -> result={'marital_status': None, 'name': 'Alain', 'citizenship': 'US citizen'}

Enforcing 'Canadian eh?' as the value of *citizenship*
   Canadian(name='Alain') -> result={'name': 'Alain', 'citizenship': 'Canadian eh?'}

Trying to change enforced value 'Canadian eh?' of *citizenship*
   Canadian(citizenship='US') -> Test OK. EnforcedConstrArg was correctly raised: 'The value of argument citizenship in <class __main__.Canadian at 2444970>.__init__ is enforced at 'Canadian eh?', and cannot be changed.'

Person2.__init__ received init_file=C:/temp.txt
Class with private *init_file* attribute*
   Person2(init_file='C:/temp.txt') -> result={'name': None, 'citizenship': None}

Subclassing from non-standard class AnimatedCharacter.*
   AnimatedPerson(name='Alain', animation_file='C:/People/Alain.dat') -> result={'name': 'Alain', 'frames_per_sec': 40, 'animation_file': 'C:/People/Alain.dat', 'citizenship': None}


*******************************************************************************
* Name        : SymDict
* Description : self-test for SymDict.py
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
EdSim instance EdSim(0) connected
*** Compiling symbols from file: %VCODE_HOME%\Data\TestData\small_buff.c ***
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


Parsed symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 
Unresolved abbreviations are:
'abbrev': appears in ['this_sym_has_an_other_abbrev']
'unres': appears in ['this_sym_is_unres', 'this_sym_is_unres_too']

*** End of compilation test ***

*** Compiling symbols from file: %VCODE_HOME%\Data\TestData\large_buff.py ***
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


Parsed symbols are: 
AttributeError: ['attribute error']
LargeNonObject: ['large non object']
LargeObject: ['large object']
Object: ['object']
SmallNonObject: ['small non object']
SmallObject: ['small object']
__bases__: ['bases']
__dict__: ['dict', 'dictionary']
__init__: ['init', 'initial', 'initialize', 'intial']
__name__: ['name']
a_base: ['a base']
add_test: ['add test']
age: ['age']
an_attr_def: ['an attr def', 'an attr definition', 'an attr default', 'an attr define', 'an attr defined', 'an attr deaf', 'an attribute def', 'an attribute definition', 'an attribute default', 'an attribute define', 'an attribute defined', 'an attribute deaf']
an_attr_init: ['an attr init', 'an attr initial', 'an attr initialize', 'an attr intial', 'an attribute init', 'an attribute initial', 'an attribute initialize', 'an attribute intial']
and: ['and']
attrs: ['attributes']
attrs_superclasses: ['attributes superclasses']
attrs_this_class: ['attributes this class']
autoTst: ['auto tst']
auto_test: ['auto test']
class: ['class']
code: ['code']
code_file: ['code file']
deep_construct: ['deep construct']
def: ['def', 'definition', 'default', 'define', 'defined', 'deaf']
else: ['else']
environ: ['environ', 'environment']
exc: ['exc', 'exception']
except: ['except']
exceptions: ['exceptions']
exclude_bases: ['exclude bases']
exec: ['exec', 'execute', 'executable']
execfile: ['execfile']
expandvars: ['expandvars']
for: ['for']
has_key: ['has key']
her_age: ['her age']
if: ['if']
import: ['import']
in: ['in']
index: ['index']
init_attrs: ['init attributes', 'initial attributes', 'initialize attributes', 'intial attributes']
items: ['items']
name: ['name']
not: ['not']
num_times: ['num times', 'number times']
obj: ['obj', 'object']
operation: ['operation']
os: ['os', 'operating system', 'o s']
pass: ['pass']
posixpath: ['posixpath']
profConstrLargeNonObj: ['prof constr large non obj', 'prof constr large non object', 'profile constr large non obj', 'profile constr large non object', 'profiling constr large non obj', 'profiling constr large non object', 'professional constr large non obj', 'professional constr large non object']
profConstrLargeObj: ['prof constr large obj', 'prof constr large object', 'profile constr large obj', 'profile constr large object', 'profiling constr large obj', 'profiling constr large object', 'professional constr large obj', 'professional constr large object']
profConstrSmallNonObj: ['prof constr small non obj', 'prof constr small non object', 'profile constr small non obj', 'profile constr small non object', 'profiling constr small non obj', 'profiling constr small non object', 'professional constr small non obj', 'professional constr small non object']
profConstrSmallObj: ['prof constr small obj', 'prof constr small object', 'profile constr small obj', 'profile constr small object', 'profiling constr small obj', 'profiling constr small object', 'professional constr small obj', 'professional constr small object']
profGetLargeNonObj: ['prof get large non obj', 'prof get large non object', 'profile get large non obj', 'profile get large non object', 'profiling get large non obj', 'profiling get large non object', 'professional get large non obj', 'professional get large non object']
profGetLargeObj: ['prof get large obj', 'prof get large object', 'profile get large obj', 'profile get large object', 'profiling get large obj', 'profiling get large object', 'professional get large obj', 'professional get large object']
profGetSmallNonObj: ['prof get small non obj', 'prof get small non object', 'profile get small non obj', 'profile get small non object', 'profiling get small non obj', 'profiling get small non object', 'professional get small non obj', 'professional get small non object']
profGetSmallObj: ['prof get small obj', 'prof get small object', 'profile get small obj', 'profile get small object', 'profiling get small obj', 'profiling get small object', 'professional get small obj', 'professional get small object']
profObject: ['prof object', 'profile object', 'profiling object', 'professional object']
profSetLargeNonObj: ['prof set large non obj', 'prof set large non object', 'profile set large non obj', 'profile set large non object', 'profiling set large non obj', 'profiling set large non object', 'professional set large non obj', 'professional set large non object']
profSetLargeObj: ['prof set large obj', 'prof set large object', 'profile set large obj', 'profile set large object', 'profiling set large obj', 'profiling set large object', 'professional set large obj', 'professional set large object']
profSetSmallNonObj: ['prof set small non obj', 'prof set small non object', 'profile set small non obj', 'profile set small non object', 'profiling set small non obj', 'profiling set small non object', 'professional set small non obj', 'professional set small non object']
profSetSmallObj: ['prof set small obj', 'prof set small object', 'profile set small obj', 'profile set small object', 'profiling set small obj', 'profiling set small object', 'professional set small obj', 'professional set small object']
prof_test: ['prof test', 'profile test', 'profiling test', 'professional test']
profile: ['profile']
range: ['range']
run: ['run']
self: ['self']
self_test: ['self test']
sep: ['sep', 'separator']
setattr: ['setattr']
stdout: ['stdout']
str: ['str', 'string']
sys: ['sys', 'system']
this_class: ['this class']
try: ['try']
try_attribute: ['try attribute']
write: ['write']
x: ['x']
_cached_symbols_as_one_string is:
    autoTst  import  auto_test  exceptions  os  posixpath  profile  sys  class  Object  if  environ  has_key  and  code_file  expandvars  sep  execfile  def  __init__  self  pass  deep_construct  this_class  attrs_this_class  attrs_superclasses  exclude_bases  for  a_base  in  __bases__  not  an_attr_def  items  __dict__  init_attrs  attrs  an_attr_init  setattr  SmallObject  name  age  LargeObject  SmallNonObject  LargeNonObject  profConstrSmallObj  num_times  index  range  obj  profConstrLargeObj  profConstrSmallNonObj  profConstrLargeNonObj  profGetSmallObj  her_age  profGetLargeObj  profGetSmallNonObj  profGetLargeNonObj  profSetSmallObj  profSetLargeObj  profSetSmallNonObj  profSetLargeNonObj  profObject  try_attribute  operation  stdout  write  code  else  x  try  exec  except  AttributeError  exc  str  prof_test  run  self_test  add_test  __name__ 
Unresolved abbreviations are:
'constr': appears in ['profConstrLargeNonObj', 'profConstrSmallObj', 'profConstrLargeObj', 'profConstrSmallNonObj']
'execfile': appears in ['execfile']
'expandvars': appears in ['expandvars']
'posixpath': appears in ['posixpath']
'setattr': appears in ['setattr']
'stdout': appears in ['stdout']

*** End of compilation test ***

*** Pseudo symbol match test***
   Source files are: ['%VCODE_HOME%\\Data\\TestData\\large_buff.py']
   Symbols are: ['set attribute', 'expand variables', 'execute file', 'profile Constructor Large Object', 'profile construct large object', 'auto test']


Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
'set attribute' matches: [setattr, set_attribute, SetAttribute, setAttribute, SET_ATTRIBUTE, setattribute, SETATTRIBUTE, ]
'expand variables' matches: [expandvars, expand_variables, ExpandVariables, expandVariables, EXPAND_VARIABLES, expandvariables, EXPANDVARIABLES, ]
'execute file' matches: [execfile, execute_file, ExecuteFile, executeFile, EXECUTE_FILE, executefile, EXECUTEFILE, ]
'profile Constructor Large Object' matches: [profConstrLargeObj, profile_constructor_large_object, ProfileConstructorLargeObject, profileConstructorLargeObject, PROFILE_CONSTRUCTOR_LARGE_OBJECT, profileconstructorlargeobject, PROFILECONSTRUCTORLARGEOBJECT, ]
'profile construct large object' matches: [profConstrLargeObj, profile_construct_large_object, ProfileConstructLargeObject, profileConstructLargeObject, PROFILE_CONSTRUCT_LARGE_OBJECT, profileconstructlargeobject, PROFILECONSTRUCTLARGEOBJECT, ]
'auto test' matches: [auto_test, autoTst, AutoTest, autoTest, AUTO_TEST, autotest, AUTOTEST, ]

*** End of Pseudo Symbol Match test ***


*** Accept symbol match test. source='%VCODE_HOME%\Data\TestData\small_buff.c' ***
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Parsed symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


Unresolved abbreviations are:
'abbrev': appears in ['this_sym_has_an_other_abbrev']
'unres': appears in ['this_sym_is_unres', 'this_sym_is_unres_too']


Accepting: 'this symbol is unresolved' -> 'this_sym_is_unres', 


After accepting those symbols, known symbols are:

API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this sym is unresolved', 'this symbol is unres', 'this symbol is unresolved']
this_sym_is_unres_too: ['this sym is unres too', 'this sym is unresolved too', 'this symbol is unres too', 'this symbol is unresolved too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


Unresolved abbreviations are:
'abbrev': appears in ['this_sym_has_an_other_abbrev']

*** End of accept symbol match test ***

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


*******************************************************************************
* Name        : am_dictionaries
* Description : Testing AppMgr dictionary management.
*******************************************************************************

new instance of emacs 1

state {
application:  emacs
instance:  emacs(0)
known windows []
} state

new window 14
SelectWinGramDummy for buffer None, window 14
init
new window 20
SelectWinGramDummy for buffer None, window 20
init

state {
application:  emacs
instance:  emacs(0)
window 14
window 20
known windows [14, 20]
} state

new instance of emacs 2
with window 10
SelectWinGramDummy for buffer None, window 10
init

state {
application:  emacs
instance:  emacs(0)
window 14
window 20
instance:  emacs(1)
window 10
known windows [10, 14, 20]
} state

new instance of Vim 3
delete window 20
SelectWinGramDummy for buffer None, window 20
deactivating
SelectWinGramDummy for buffer None, window 20
del

state {
application:  Vim
instance:  Vim(0)
application:  emacs
instance:  emacs(0)
window 14
instance:  emacs(1)
window 10
known windows [10, 14]
} state

delete instance emacs(1)
SelectWinGramDummy for buffer None, window 10
deactivating
SelectWinGramDummy for buffer None, window 10
del
new instance of emacs 4
with window 7
SelectWinGramDummy for buffer None, window 7
init

state {
application:  Vim
instance:  Vim(0)
application:  emacs
instance:  emacs(0)
window 14
instance:  emacs(2)
window 7
known windows [7, 14]
} state

delete instance emacs(0)
SelectWinGramDummy for buffer None, window 14
deactivating
SelectWinGramDummy for buffer None, window 14
del

state {
application:  Vim
instance:  Vim(0)
application:  emacs
instance:  emacs(2)
window 7
known windows [7]
} state

delete instance Vim(0)
delete instance emacs(2)
SelectWinGramDummy for buffer None, window 7
deactivating
SelectWinGramDummy for buffer None, window 7
del

state {
application:  Vim
application:  emacs
known windows []
} state

new instance of emacs 5
with window 94
SelectWinGramDummy for buffer None, window 94
init
new instance of emacs 6
with window 94
SelectWinGramDummy for buffer None, window 94
init

state {
application:  Vim
application:  emacs
instance:  emacs(3)
window 94
instance:  emacs(4)
window 94
known windows [94]
} state

SelectWinGramDummy for buffer None, window 94
deactivating
SelectWinGramDummy for buffer None, window 94
del

state {
application:  Vim
application:  emacs
instance:  emacs(3)
instance:  emacs(4)
window 94
known windows [94]
} state


state {
application:  Vim
application:  emacs
instance:  emacs(4)
window 94
known windows [94]
} state

SelectWinGramDummy for buffer None, window 94
deactivating
SelectWinGramDummy for buffer None, window 94
del

state {
application:  Vim
application:  emacs
known windows []
} state



*******************************************************************************
* Name        : automatic_abbreviations
* Description : testing automatic creation of abbreviations
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file('blah.c')

WARNING: source file 'blah.c' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
'H:\\Projects\\VoiceCode\\VCode\\Data\\TestData'


>>> Testing console command: compile_symbols([r'H:\Projects\VoiceCode\VCode\Data\TestData\small_buff.c'])

Compiling symbols for file '%VCODE_HOME%\Data\TestData\small_buff.c'
>>> Known symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: print_abbreviations(1)

List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations

'abbrev': appears in ['this_sym_has_an_other_abbrev']
'unres': appears in ['this_sym_is_unres', 'this_sym_is_unres_too']


>>> Testing console command: say(['this', 'symbol', 'is', 'unresolved', ', \\comma'], user_input='1\n')
Heard this symbol is unresolved comma
Associate 'this symbol is unresolved' with symbol (Enter selection):

  '0': no association
  '1': this_sym_is_unres
  '2': this_symbol_is_unresolved (*new*)
  '3': ThisSymbolIsUnresolved (*new*)
  '4': thisSymbolIsUnresolved (*new*)
  '5': THIS_SYMBOL_IS_UNRESOLVED (*new*)
  '6': thissymbolisunresolved (*new*)
  '7': THISSYMBOLISUNRESOLVED (*new*)

> *** Start of source buffer ***
  1: this_sym_is_unres, <CURSOR>

*** End of source buffer ***


>>> Testing console command: print_abbreviations(1)

List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'unres' expands to ['unresolved']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations

'abbrev': appears in ['this_sym_has_an_other_abbrev']


>>> Testing console command: print_symbols()

API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this sym is unresolved', 'this symbol is unres', 'this symbol is unresolved']
this_sym_is_unres_too: ['this sym is unres too', 'this sym is unresolved too', 'this symbol is unres too', 'this symbol is unresolved too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: say(['this_sym_is_unres_too\\this symbol is unresolved too', ', \\comma'], user_input='None')
Heard this symbol is unresolved too comma
*** Start of source buffer ***
  1: this_sym_is_unres, this_sym_is_unres_too, <CURSOR>

*** End of source buffer ***


>>> Testing console command: print_symbols()

API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this sym is unresolved', 'this symbol is unres', 'this symbol is unresolved']
this_sym_is_unres_too: ['this sym is unres too', 'this sym is unresolved too', 'this symbol is unres too', 'this symbol is unresolved too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: print_abbreviations(1)

List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'unres' expands to ['unresolved']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations

'abbrev': appears in ['this_sym_has_an_other_abbrev']


>>> Testing console command: say(['file', 'name', ', \\comma'], user_input='1\n')
Heard file name comma
Associate 'file name' with symbol (Enter selection):

  '0': no association
  '1': f_name
  '2': file_name (*new*)
  '3': FileName (*new*)
  '4': fileName (*new*)
  '5': FILE_NAME (*new*)
  '6': filename (*new*)
  '7': FILENAME (*new*)

> WARNING: abbreviation 'f' not added (length < 2)
*** Start of source buffer ***
  1: this_sym_is_unres, this_sym_is_unres_too, f_name, <CURSOR>

*** End of source buffer ***


>>> Testing console command: print_symbols()

API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this sym is unresolved', 'this symbol is unres', 'this symbol is unresolved']
this_sym_is_unres_too: ['this sym is unres too', 'this sym is unresolved too', 'this symbol is unres too', 'this symbol is unresolved too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: print_abbreviations(1)

List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'unres' expands to ['unresolved']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations

'abbrev': appears in ['this_sym_has_an_other_abbrev']


>>> Testing console command: say(['application', 'programming', 'interface', 'function', ', \\comma'], user_input='1\n')
Heard application programming interface function comma
Associate 'application programming interface function' with symbol (Enter selection):

  '0': no association
  '1': API_function
  '2': application_programming_interface_function (*new*)
  '3': ApplicationProgrammingInterfaceFunction (*new*)
  '4': applicationProgrammingInterfaceFunction (*new*)
  '5': APPLICATION_PROGRAMMING_INTERFACE_FUNCTION (*new*)
  '6': applicationprogramminginterfacefunction (*new*)
  '7': APPLICATIONPROGRAMMINGINTERFACEFUNCTION (*new*)

> *** Start of source buffer ***
  1: this_sym_is_unres, this_sym_is_unres_too, f_name, API_function, <CURSOR>

*** End of source buffer ***


>>> Testing console command: print_abbreviations(1)

List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'api' expands to ['application programming interface']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'unres' expands to ['unresolved']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations

'abbrev': appears in ['this_sym_has_an_other_abbrev']


>>> Testing console command: quit(save_speech_files=0, disconnect=0)



*******************************************************************************
* Name        : basic_correction
* Description : Testing basic correction infrastructure with ResMgr.
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***

***Testing initial state***


0 stored utterances, as expected


recent dictation is empty, as expected


***Some simple dictation***



>>> Testing console command: say(['class', 'clown', 'inherits', 'from', 'student'], user_input='0
0
')
Heard class clown inherits from student
Associate 'clown' with symbol (Enter selection):

  '0': no association
  '1': clown (*new*)
  '2': Clown (*new*)
  '3': CLOWN (*new*)

> Associate 'student' with symbol (Enter selection):

  '0': no association
  '1': student (*new*)
  '2': Student (*new*)
  '3': STUDENT (*new*)

> *** Start of source buffer ***
  1: class clown(student<CURSOR>):
  2:    

*** End of source buffer ***


>>> Testing console command: say(['class', 'body'], user_input='')
Heard class body
*** Start of source buffer ***
  1: class clown(student):
  2:    <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['define', 'method', 'popularity', 'method', 'body'], user_input='0
')
Heard define method popularity method body
Associate 'popularity' with symbol (Enter selection):

  '0': no association
  '1': popularity (*new*)
  '2': Popularity (*new*)
  '3': POPULARITY (*new*)

> *** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['return', '8'], user_input='')
Heard return 8
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8<CURSOR>

*** End of source buffer ***

***Testing state***


4 stored utterances, as expected


4 recently dictated utterances, as expected


***Testing scratch that***

scratching 1

*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8<CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***
scratch 1 succeeded as expected

3 stored utterances, as expected


3 recently dictated utterances, as expected


***Moving cursor manually***

*** Start of source buffer ***
  1: <CURSOR>class clown(student):
  2:    def popularity(self):
  3:       

*** End of source buffer ***

***Testing scratch that following manual move***

scratching 1

*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class clown(student):
  2:    <CURSOR>

*** End of source buffer ***
scratch 1 succeeded as expected

2 stored utterances, as expected


2 recently dictated utterances, as expected



>>> Testing console command: say(['define', 'method', 'grades', 'method', 'body', 'return', 'B.'], user_input='0
2
')
Heard define method grades method body return B.
Associate 'grades' with symbol (Enter selection):

  '0': no association
  '1': grades (*new*)
  '2': Grades (*new*)
  '3': GRADES (*new*)

> Associate 'B.' with symbol (Enter selection):

  '0': no association
  '1': b (*new*)
  '2': B (*new*)

> *** Start of source buffer ***
  1: class clown(student):
  2:    def grades(self):
  3:       return B<CURSOR>

*** End of source buffer ***

3 stored utterances, as expected


3 recently dictated utterances, as expected



>>> Testing console command: say(['select', 'clown'], user_input='None')
Heard select clown
*** Start of source buffer ***
  1: class <SEL_START>clown<SEL_END>(student):
  2:    def grades(self):
  3:       return B

*** End of source buffer ***

***Manually changing text

*** Start of source buffer ***
  1: class president<CURSOR>(student):
  2:    def grades(self):
  3:       return B

*** End of source buffer ***

***Testing scratch that following manual change***

scratching 1

scratch 1 failed as expected
WARNING: source file 'blahblah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['class', 'cloud', 'inherits', 'from', 'student'], user_input='0
0
')
Heard class cloud inherits from student
Associate 'cloud' with symbol (Enter selection):

  '0': no association
  '1': cloud (*new*)
  '2': Cloud (*new*)
  '3': CLOUD (*new*)

> Associate 'student' with symbol (Enter selection):

  '0': no association
  '1': student (*new*)
  '2': Student (*new*)
  '3': STUDENT (*new*)

> *** Start of source buffer ***
  1: class cloud(student<CURSOR>):
  2:    

*** End of source buffer ***


>>> Testing console command: say(['class', 'body'], user_input='')
Heard class body
*** Start of source buffer ***
  1: class cloud(student):
  2:    <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['fine', 'method', 'popularity', 'method', 'body'], user_input='0
')
Heard fine method popularity method body
Associate 'fine method popularity' with symbol (Enter selection):

  '0': no association
  '1': fine_method_popularity (*new*)
  '2': FineMethodPopularity (*new*)
  '3': fineMethodPopularity (*new*)
  '4': FINE_METHOD_POPULARITY (*new*)
  '5': finemethodpopularity (*new*)
  '6': FINEMETHODPOPULARITY (*new*)

> *** Start of source buffer ***
  1: class cloud(student):
  2:    fine method popularity<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['return', '8'], user_input='')
Heard return 8
*** Start of source buffer ***
  1: class cloud(student):
  2:    fine method popularityreturn 8<CURSOR>

*** End of source buffer ***

***Testing state***


4 stored utterances, as expected


4 recently dictated utterances, as expected


***Testing correction of recent utterance***

detecting changes
utterance 2: change = {'fine': 'define'}
word fine being replaced with define
utterance 2 was changed 
utterance 2 was corrected
about to reinterpret
*** Start of source buffer ***
  1: class cloud(student):
  2:    fine method popularityreturn 8<CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student):
  2:    fine method popularity<CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student):
  2:    <CURSOR>

*** End of source buffer ***
Associate 'popularity' with symbol (Enter selection):

  '0': no association
  '1': popularity (*new*)
  '2': Popularity (*new*)
  '3': POPULARITY (*new*)

> *** Start of source buffer ***
  1: class cloud(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student):
  2:    def popularity(self):
  3:       return 8<CURSOR>

*** End of source buffer ***

all utterances from 2 to the present
were reinterpreted, as expected


***Testing state***


4 stored utterances, as expected


4 recently dictated utterances, as expected


***Testing correction of another recent utterance***

detecting changes
utterance 4: change = {'cloud': 'clown'}
word cloud being replaced with clown
utterance 4 was changed 
utterance 4 was corrected
about to reinterpret
*** Start of source buffer ***
  1: class cloud(student):
  2:    def popularity(self):
  3:       return 8<CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student):
  2:    <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class cloud(student<CURSOR>):
  2:    

*** End of source buffer ***
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
Associate 'clown' with symbol (Enter selection):

  '0': no association
  '1': clown (*new*)
  '2': Clown (*new*)
  '3': CLOWN (*new*)

> Associate 'student' with symbol (Enter selection):

  '0': no association
  '1': student (*new*)
  '2': Student (*new*)
  '3': STUDENT (*new*)

> *** Start of source buffer ***
  1: class clown(student<CURSOR>):
  2:    

*** End of source buffer ***
*** Start of source buffer ***
  1: class clown(student):
  2:    <CURSOR>

*** End of source buffer ***
Associate 'popularity' with symbol (Enter selection):

  '0': no association
  '1': popularity (*new*)
  '2': Popularity (*new*)
  '3': POPULARITY (*new*)

> *** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8<CURSOR>

*** End of source buffer ***

all utterances from 4 to the present
were reinterpreted, as expected


***Testing state***


4 stored utterances, as expected


4 recently dictated utterances, as expected



>>> Testing console command: say(['new', 'line'], user_input='')
Heard new line
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4:    <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back indent'], user_input='')
Heard back indent
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['excess', 'equals', '0'], user_input='0
')
Heard excess equals 0
Associate 'excess' with symbol (Enter selection):

  '0': no association
  '1': excess (*new*)
  '2': Excess (*new*)
  '3': EXCESS (*new*)

> *** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4: excess = 0<CURSOR>

*** End of source buffer ***

***Manually changing text

*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4: excess<CURSOR>

*** End of source buffer ***

***Testing state***


7 stored utterances, as expected


7 recently dictated utterances, as expected


***Testing failed correction of a recent utterance***

detecting changes
utterance 0: change = {'excess': 'success'}

reinterpretation failed, as expected


***Fixing error manually***

*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4: <CURSOR>

*** End of source buffer ***

***Testing state***


7 stored utterances, as expected


7 recently dictated utterances, as expected



>>> Testing console command: say(['excess', 'equals', '1', 'new', 'line'], user_input='0
')
Heard excess equals 1 new line
Associate 'excess' with symbol (Enter selection):

  '0': no association
  '1': excess (*new*)
  '2': Excess (*new*)
  '3': EXCESS (*new*)

>   2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back indent'], user_input='')
Heard back indent
  2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['results', 'at', 'index', '0', 'jump', 'out', 'equals', '0'], user_input='0
')
Heard results at index 0 jump out equals 0
Associate 'results' with symbol (Enter selection):

  '0': no association
  '1': results (*new*)
  '2': Results (*new*)
  '3': RESULTS (*new*)

>   2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: results[0] = 0<CURSOR>

*** End of source buffer ***

***Testing state***


10 stored utterances, as expected


10 recently dictated utterances, as expected


***Testing scratch that***

scratching 1

  2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: results[0] = 0<CURSOR>

*** End of source buffer ***
  2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: <CURSOR>

*** End of source buffer ***
scratch 1 succeeded as expected

***Testing state***


9 stored utterances, as expected


9 recently dictated utterances, as expected


***Testing correction after scratch that***

detecting changes
utterance 2: change = {'excess': 'access'}
word excess being replaced with access
utterance 2 was changed 
utterance 2 was corrected
about to reinterpret
  2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: <CURSOR>

*** End of source buffer ***
  2:    def popularity(self):
  3:       return 8
  4: excess = 1
  5: <CURSOR>

*** End of source buffer ***
*** Start of source buffer ***
  1: class clown(student):
  2:    def popularity(self):
  3:       return 8
  4: <CURSOR>

*** End of source buffer ***
Associate 'access' with symbol (Enter selection):

  '0': no association
  '1': access (*new*)
  '2': Access (*new*)
  '3': ACCESS (*new*)

>   2:    def popularity(self):
  3:       return 8
  4: access = 1
  5: <CURSOR>

*** End of source buffer ***
  2:    def popularity(self):
  3:       return 8
  4: access = 1
  5: <CURSOR>

*** End of source buffer ***

all utterances from 2 to the present
were reinterpreted, as expected


***Testing state***


9 stored utterances, as expected


9 recently dictated utterances, as expected



*******************************************************************************
* Name        : change_direction
* Description : testing changing direction of last command
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file(r'H:\Projects\VoiceCode\VCode\Data\TestData\large_buff.py')

*** Start of source buffer ***
  1: <CURSOR>
  2: # This symbol is here because it is homophonic with auto_test. Just checking
  3: # to make sure that symbol match works with homophonic symbols.
  4: autoTst = 0


>>> Testing console command: say(['after hyphen'])

Heard after hyphen
 11:     This class implements various useful behaviors for generic
 12:     objects, such as:
 13: 
 14:     - <CURSOR>safe attribute setting
 15:     - deep constructor
 16:     - pretty printing???
 17:     


>>> Testing console command: say(['again'])

Heard again
 12:     objects, such as:
 13: 
 14:     - safe attribute setting
 15:     - <CURSOR>deep constructor
 16:     - pretty printing???
 17:     
 18: 


>>> Testing console command: say(['again'])

Heard again
 13: 
 14:     - safe attribute setting
 15:     - deep constructor
 16:     - <CURSOR>pretty printing???
 17:     
 18: 
 19:     **SAFE ATTRIBUTE SETTING***


>>> Testing console command: say(['previous one'])

Heard previous one
 12:     objects, such as:
 13: 
 14:     - safe attribute setting
 15:     - <CURSOR>deep constructor
 16:     - pretty printing???
 17:     
 18: 


>>> Testing console command: say(['previous one'])

Heard previous one
 11:     This class implements various useful behaviors for generic
 12:     objects, such as:
 13: 
 14:     - <CURSOR>safe attribute setting
 15:     - deep constructor
 16:     - pretty printing???
 17:     


>>> Testing console command: say(['next one'])

Heard next one
 12:     objects, such as:
 13: 
 14:     - safe attribute setting
 15:     - <CURSOR>deep constructor
 16:     - pretty printing???
 17:     
 18: 


*******************************************************************************
* Name        : compile_symbols
* Description : Testing voice command for compiling symbols
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
*** Start of source buffer ***
  1: <CURSOR># This is a small test buffer for Python
  2: 
  3: 
  4: 
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Before compiling symbols, symbols are:

_cached_symbols_as_one_string is:
   
Heard compile symbols
Compiling symbols for None
Done compiling symbols
*** Start of source buffer ***
  1: <CURSOR># This is a small test buffer for Python
  2: 
  3: 
  4: 
After compiling symbols, symbols are:

AClass: ['a class']
ASuper: ['a super']
a_method: ['a method']
class: ['class']
def: ['def', 'definition', 'default', 'define', 'defined', 'deaf']
print: ['print']
self: ['self']
x: ['x']
_cached_symbols_as_one_string is:
    class  AClass  ASuper  def  a_method  self  x  print 


*******************************************************************************
* Name        : dummy_grammars
* Description : Testing WinGramMgr grammar management with dummy grammars.
*******************************************************************************

EdSim.__init__
SourceBuff.__init__: 
new buffer fish.C
with window 5
SourceBuff.__init__: fish.C
SelectWinGramDummy for buffer None, window 5
init
DictWinGramDummy for buffer = 'fish.C', window 5
init
new buffer fowl.py
with window 5
SourceBuff.__init__: fowl.py
DictWinGramDummy for buffer = 'fowl.py', window 5
init
activating buffer fish.C for window 5
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;
DictWinGramDummy for buffer = 'fowl.py', window 5
deactivating
SelectWinGramDummy for buffer 'fish.C', window 5
activating:  5  
DictWinGramDummy for buffer = 'fish.C', window 5
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', window 5
activating:  5  
new window 7
SelectWinGramDummy for buffer None, window 7
init
new buffer dog.pl
with window 7
SourceBuff.__init__: dog.pl
DictWinGramDummy for buffer = 'dog.pl', window 7
init
new buffer fish.h
with window 7
SourceBuff.__init__: fish.h
DictWinGramDummy for buffer = 'fish.h', window 7
init
activating buffer dog.pl for window 7
 10:     $dirSep = "\";
 11:     $curDirCom = 'cd';
 12: } else {
 13:     $dirSep = <CURSOR>'/';
 14:     $curDirCom = 'pwd';
 15: };
 16: 

*** End of source buffer ***
DictWinGramDummy for buffer = 'fish.h', window 7
deactivating
SelectWinGramDummy for buffer 'dog.pl', window 7
activating:  7  
DictWinGramDummy for buffer = 'dog.pl', window 7
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', window 7
activating:  7  
activating buffer fish.h for window 7
*** Start of source buffer ***
  1: void move(float x, y);<CURSOR>
  2: 

*** End of source buffer ***
DictWinGramDummy for buffer = 'dog.pl', window 7
deactivating
SelectWinGramDummy for buffer 'fish.h', window 7
activating:  7  
DictWinGramDummy for buffer = 'fish.h', window 7
setting context: before = [ x, y);], after = []
DictWinGramDummy for buffer = 'fish.h', window 7
activating:  7  
activating buffer fowl.py for window 5
*** Start of source buffer ***
  1: import sys
  2: 
  3: def something(value):
  4:     print <CURSOR>value
  5: 
  6: if __name__ == '__main__':
  7:     something('nice')
DictWinGramDummy for buffer = 'fish.C', window 5
deactivating
SelectWinGramDummy for buffer 'fowl.py', window 5
activating:  5  
DictWinGramDummy for buffer = 'fowl.py', window 5
setting context: before = [ something(value):
    print ], after = [value

if ]
DictWinGramDummy for buffer = 'fowl.py', window 5
activating:  5  
SourceBuff.remove_other_references: fowl.py
SourceBuff.__del__: fowl.py
close buffer fowl.py
DictWinGramDummy for buffer = 'fowl.py', window 5
del
deactivate all for window 5
SelectWinGramDummy for buffer 'fowl.py', window 5
deactivating
DictWinGramDummy for buffer = 'fish.C', window 5
deactivating
delete window 7
SelectWinGramDummy for buffer 'fish.h', window 7
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 7
deactivating
DictWinGramDummy for buffer = 'fish.h', window 7
deactivating
SelectWinGramDummy for buffer 'fish.h', window 7
del
DictWinGramDummy for buffer = 'dog.pl', window 7
del
DictWinGramDummy for buffer = 'fish.h', window 7
del
SourceBuff.remove_other_references: dog.pl
SourceBuff.__del__: dog.pl
close buffer dog.pl
activating buffer fish.C for window 5
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;
SelectWinGramDummy for buffer 'fish.C', window 5
activating:  5  
DictWinGramDummy for buffer = 'fish.C', window 5
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', window 5
activating:  5  
deactivate all
SelectWinGramDummy for buffer 'fish.C', window 5
deactivating
DictWinGramDummy for buffer = 'fish.C', window 5
deactivating
close all buffers
SourceBuff.remove_other_references: fish.h
SourceBuff.__del__: fish.h
SourceBuff.remove_other_references: fish.C
SourceBuff.__del__: fish.C
SourceBuff.remove_other_references: 
SourceBuff.__del__: 
cleanup app
EdSim.remove_other_references
cleanup manager
SelectWinGramDummy for buffer 'fish.C', window 5
deactivating
DictWinGramDummy for buffer = 'fish.C', window 5
deactivating
SelectWinGramDummy for buffer 'fish.C', window 5
del
DictWinGramDummy for buffer = 'fish.C', window 5
del
test ending - expect dels of manager, app
EdSim.__del__


*******************************************************************************
* Name        : dummy_grammars_global
* Description : Testing WinGramMgr grammar management with global, exclusive dummy grammars.
*******************************************************************************

EdSim.__init__
SourceBuff.__init__: 
new buffer fish.C
with window 5
SourceBuff.__init__: fish.C
SelectWinGramDummy for buffer None, global
init
DictWinGramDummy for buffer = 'fish.C', global
init
new buffer fowl.py
with window 5
SourceBuff.__init__: fowl.py
DictWinGramDummy for buffer = 'fowl.py', global
init
activating buffer fish.C for window 5
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;
DictWinGramDummy for buffer = 'fowl.py', global
deactivating
SelectWinGramDummy for buffer 'fish.C', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'fish.C', global
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', global
activating:  global  exclusive 

new window 7
SelectWinGramDummy for buffer None, global
init
new buffer dog.pl
with window 7
SourceBuff.__init__: dog.pl
DictWinGramDummy for buffer = 'dog.pl', global
init
new buffer fish.h
with window 7
SourceBuff.__init__: fish.h
DictWinGramDummy for buffer = 'fish.h', global
init
activating buffer dog.pl for window 7
 10:     $dirSep = "\";
 11:     $curDirCom = 'cd';
 12: } else {
 13:     $dirSep = <CURSOR>'/';
 14:     $curDirCom = 'pwd';
 15: };
 16: 

*** End of source buffer ***
DictWinGramDummy for buffer = 'fish.h', global
deactivating
DictWinGramDummy for buffer = 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'fowl.py', global
deactivating
SelectWinGramDummy for buffer 'dog.pl', global
activating:  global  exclusive 

SelectWinGramDummy for buffer 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'dog.pl', global
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', global
activating:  global  exclusive 

activating buffer fish.h for window 7
*** Start of source buffer ***
  1: void move(float x, y);<CURSOR>
  2: 

*** End of source buffer ***
DictWinGramDummy for buffer = 'dog.pl', global
deactivating
DictWinGramDummy for buffer = 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'fowl.py', global
deactivating
SelectWinGramDummy for buffer 'fish.h', global
activating:  global  exclusive 

SelectWinGramDummy for buffer 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'fish.h', global
setting context: before = [ x, y);], after = []
DictWinGramDummy for buffer = 'fish.h', global
activating:  global  exclusive 

activating buffer fowl.py for window 5
*** Start of source buffer ***
  1: import sys
  2: 
  3: def something(value):
  4:     print <CURSOR>value
  5: 
  6: if __name__ == '__main__':
  7:     something('nice')
DictWinGramDummy for buffer = 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'dog.pl', global
deactivating
DictWinGramDummy for buffer = 'fish.h', global
deactivating
SelectWinGramDummy for buffer 'fowl.py', global
activating:  global  exclusive 

SelectWinGramDummy for buffer 'fish.h', global
deactivating
DictWinGramDummy for buffer = 'fowl.py', global
setting context: before = [ something(value):
    print ], after = [value

if ]
DictWinGramDummy for buffer = 'fowl.py', global
activating:  global  exclusive 

SourceBuff.remove_other_references: fowl.py
SourceBuff.__del__: fowl.py
close buffer fowl.py
DictWinGramDummy for buffer = 'fowl.py', global
del
deactivate all for window 5
SelectWinGramDummy for buffer 'fish.h', global
deactivating
DictWinGramDummy for buffer = 'dog.pl', global
deactivating
DictWinGramDummy for buffer = 'fish.h', global
deactivating
SelectWinGramDummy for buffer 'fowl.py', global
deactivating
DictWinGramDummy for buffer = 'fish.C', global
deactivating
delete window 7
SelectWinGramDummy for buffer 'fish.h', global
deactivating
DictWinGramDummy for buffer = 'dog.pl', global
deactivating
DictWinGramDummy for buffer = 'fish.h', global
deactivating
SelectWinGramDummy for buffer 'fish.h', global
del
DictWinGramDummy for buffer = 'dog.pl', global
del
DictWinGramDummy for buffer = 'fish.h', global
del
SourceBuff.remove_other_references: dog.pl
SourceBuff.__del__: dog.pl
close buffer dog.pl
activating buffer fish.C for window 5
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;
SelectWinGramDummy for buffer 'fish.C', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'fish.C', global
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', global
activating:  global  exclusive 

deactivate all
SelectWinGramDummy for buffer 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'fish.C', global
deactivating
close all buffers
SourceBuff.remove_other_references: fish.h
SourceBuff.__del__: fish.h
SourceBuff.remove_other_references: fish.C
SourceBuff.__del__: fish.C
SourceBuff.remove_other_references: 
SourceBuff.__del__: 
cleanup app
EdSim.remove_other_references
cleanup manager
SelectWinGramDummy for buffer 'fish.C', global
deactivating
DictWinGramDummy for buffer = 'fish.C', global
deactivating
SelectWinGramDummy for buffer 'fish.C', global
del
DictWinGramDummy for buffer = 'fish.C', global
del
test ending - expect dels of manager, app
EdSim.__del__


*******************************************************************************
* Name        : insert_delete
* Description : Testing insertion and deletion commands
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['this', 'is', 'a', 'very', 'long', 'variable', 'name', 'but', 'never', 'mind'], user_input='1
1
1
1
1
1
1
1
1
')
Heard this is a very long variable name but never mind
Associate 'this' with symbol (Enter selection):

  '0': no association
  '1': this (*new*)
  '2': This (*new*)
  '3': THIS (*new*)

> Associate 'a very long variable name but never mind' with symbol (Enter selection):

  '0': no association
  '1': a_very_long_variable_name_but_never_mind (*new*)
  '2': AVeryLongVariableNameButNeverMind (*new*)
  '3': aVeryLongVariableNameButNeverMind (*new*)
  '4': A_VERY_LONG_VARIABLE_NAME_BUT_NEVER_MIND (*new*)
  '5': averylongvariablenamebutnevermind (*new*)
  '6': AVERYLONGVARIABLENAMEBUTNEVERMIND (*new*)

> *** Start of source buffer ***
  1: this is a_very_long_variable_name_but_never_mind<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back space'], user_input='None')
Heard back space
*** Start of source buffer ***
  1: this is a_very_long_variable_name_but_never_min<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['2 times'], user_input='None')
Heard 2 times
*** Start of source buffer ***
  1: this is a_very_long_variable_name_but_never_mi<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back space 2'], user_input='None')
Heard back space 2
*** Start of source buffer ***
  1: this is a_very_long_variable_name_but_never_<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back space 3'], user_input='None')
Heard back space 3
*** Start of source buffer ***
  1: this is a_very_long_variable_name_but_nev<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back space 4'], user_input='None')
Heard back space 4
*** Start of source buffer ***
  1: this is a_very_long_variable_name_but<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['back space 5'], user_input='None')
Heard back space 5
*** Start of source buffer ***
  1: this is a_very_long_variable_nam<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['select', 'additional'], user_input='None')
Heard select additional
*** Start of source buffer ***
  1: some <SEL_START>additional<SEL_END> text

*** End of source buffer ***


>>> Testing console command: say(['back space'], user_input='None')
Heard back space
*** Start of source buffer ***
  1: some <CURSOR> text

*** End of source buffer ***


>>> Testing console command: say(['select', 'additional'], user_input='None')
Heard select additional
*** Start of source buffer ***
  1: some <SEL_START>additional<SEL_END> text

*** End of source buffer ***


>>> Testing console command: say(['back space 2'], user_input='None')
Heard back space 2
*** Start of source buffer ***
  1: some<CURSOR> text

*** End of source buffer ***


*******************************************************************************
* Name        : large_messages
* Description : Send a message that has more than 1024 character (length of a message chunk)
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
WARNING: source file 'tmp.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
111: 12345678
112: 12345678
113: 12345678
114: 1234567<CURSOR>

*** End of source buffer ***


*******************************************************************************
* Name        : mediator_console
* Description : testing mediator console commands
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: clear_symbols()    

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file('blah.c')

WARNING: source file 'blah.c' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
List of abbreviations

'abs' expands to ['absolute']
'addr' expands to ['address']
'alnum' expands to ['all numeric', 'all numberical']
'alt' expands to ['alternate', 'alternative']
'arg' expands to ['argument']
'argv' expands to ['arg v', 'argument value']
'asc' expands to ['ascii']
'atan' expands to ['arc tangent']
'atof' expands to ['a to f']
'atol' expands to ['a to l']
'attr' expands to ['attribute']
'avail' expands to ['available']
'avg' expands to ['average']
'beg' expands to ['begin', 'beginning']
'bg' expands to ['back ground']
'blk' expands to ['block', 'blocking']
'buf' expands to ['buffer']
'buff' expands to ['buffer']
'builtin' expands to ['built in']
'calc' expands to ['calculate', 'calculated', 'calculation']
'cgi' expands to ['c g i']
'char' expands to ['character']
'chdir' expands to ['change dir', 'change directory']
'chg' expands to ['change', 'changed']
'chmod' expands to ['change mode']
'chr' expands to ['character']
'clr' expands to ['clear']
'cmd' expands to ['command']
'cmp' expands to ['compare']
'cntrl' expands to ['control']
'col' expands to ['column']
'concat' expands to ['concatenate']
'cond' expands to ['condition']
'conf' expands to ['configure', 'configuration']
'config' expands to ['configuration', 'configure']
'conn' expands to ['connection', 'connected']
'cont' expands to ['control']
'cos' expands to ['co sine']
'cpp' expands to ['c plus plus']
'ctl' expands to ['control']
'ctrl' expands to ['control']
'cur' expands to ['cursor', 'current']
'curr' expands to ['current']
'db' expands to ['d b', 'data base']
'decl' expands to ['declaration', 'declare']
'def' expands to ['definition', 'default', 'define', 'defined', 'deaf']
'delim' expands to ['delimiter']
'dev' expands to ['develop', 'development', 'device']
'dict' expands to ['dictionary']
'dir' expands to ['directory', 'direction']
'div' expands to ['divide']
'doc' expands to ['document', 'documentation']
'dom' expands to ['domain']
'dst' expands to ['distance']
'dtd' expands to ['d t d']
'elem' expands to ['element']
'ent' expands to ['entry']
'env' expands to ['environment']
'environ' expands to ['environment']
'eol' expands to ['e o l', 'end of line']
'eval' expands to ['e val', 'evaluate']
'ex' expands to ['example']
'exc' expands to ['exception']
'exec' expands to ['execute', 'executable']
'expr' expands to ['expression']
'fg' expands to ['foreground']
'fifo' expands to ['first in first out']
'fmt' expands to ['format']
'fp' expands to ['file pointer']
'func' expands to ['function']
'gen' expands to ['general', 'generic']
'getattr' expands to ['get attribute']
'gid' expands to ['g i d', 'group i d']
'glob' expands to ['global']
'goto' expands to ['go to']
'gr' expands to ['group']
'hex' expands to ['hexadecimal']
'horiz' expands to ['horizontal', 'horizontally']
'html' expands to ['h t m l']
'http' expands to ['h t t p']
'imap' expands to ['i map']
'impl' expands to ['implementation']
'inc' expands to ['increment', 'include']
'incl' expands to ['include', 'included']
'info' expands to ['information']
'init' expands to ['initial', 'initialize', 'intial']
'ins' expands to ['insert']
'int' expands to ['integer']
'interp' expands to ['interpreter']
'intro' expands to ['introduction']
'io' expands to ['i o']
'ip' expands to ['i p']
'lambd' expands to ['lambda']
'len' expands to ['length']
'ln' expands to ['line']
'lnk' expands to ['link']
'loc' expands to ['location']
'login' expands to ['log in']
'mem' expands to ['memory']
'mk' expands to ['make']
'mnt' expands to ['mount', 'mounted']
'mod' expands to ['mode', 'modify']
'msec' expands to ['millisecond']
'msg' expands to ['message']
'mtime' expands to ['m time']
'nam' expands to ['name']
'nntp' expands to ['n n t p']
'no' expands to ['number']
'num' expands to ['number']
'obj' expands to ['object']
'oct' expands to ['octal']
'opt' expands to ['optional', 'option', 'optimize']
'os' expands to ['operating system', 'o s']
'osf' expands to ['o s f']
'par' expands to ['parameter']
'param' expands to ['parameter']
'pat' expands to ['pattern']
'perm' expands to ['permission']
'pkg' expands to ['package']
'pos' expands to ['position', 'positioning']
'prof' expands to ['profile', 'profiling', 'professional']
'proto' expands to ['prototype', 'protocol']
'pty' expands to ['p t y']
'punct' expands to ['punctuation']
'py' expands to ['python', 'p y']
'rand' expands to ['random']
'rd' expands to ['read']
'rect' expands to ['rectangle']
'ref' expands to ['reference']
'reg' expands to ['regular', 'regular expression']
'regexp' expands to ['regular expression']
'rel' expands to ['relative']
'repr' expands to ['represent', 'representation']
'req' expands to ['request']
'rexp' expands to ['regular expression']
'rgb' expands to ['r g b']
'rm' expands to ['remove']
'scr' expands to ['screen']
'sec' expands to ['second']
'sep' expands to ['separator']
'seq' expands to ['sequence']
'serv' expands to ['server']
'sig' expands to ['signal', 'special interest group']
'sin' expands to ['sine']
'smtp' expands to ['s m t p']
'sock' expands to ['socket']
'soundex' expands to ['soundex']
'spc' expands to ['space']
'src' expands to ['source']
'st' expands to ['standard']
'stat' expands to ['statistic', 'static']
'stdin' expands to ['s t d in', 'standard input']
'str' expands to ['string']
'sub' expands to ['sub routine']
'sym' expands to ['symbol']
'sync' expands to ['synchronize']
'sys' expands to ['system']
'temp' expands to ['temporary']
'termid' expands to ['term i d', 'terminal i d']
'tmp' expands to ['temporary']
'tok' expands to ['token']
'trans' expands to ['transition', 'transport', 'transform', 'transformation']
'tty' expands to ['t t y']
'uid' expands to ['u i d', 'user i d']
'undef' expands to ['undefined']
'uniq' expands to ['unique']
'url' expands to ['u r l']
'uu' expands to ['u u']
'var' expands to ['variable']
'vert' expands to ['vertical', 'vertically']
'win' expands to ['window']
'xml' expands to ['x m l']


List of unresolved abbreviations



>>> Testing console command: compile_symbols([r'H:\Projects\VoiceCode\VCode\Data\TestData\small_buff.c'])

Compiling symbols for file '%VCODE_HOME%\Data\TestData\small_buff.c'
>>> Known symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: say(['for', 'loop', 'horiz_pos\\horizontal position', 'loop', 'body'], user_input='None')
Heard for loop horizontal position loop body
*** Start of source buffer ***
  1: for (horiz_pos=0;  <= ; ++)
  2: {
  3: <CURSOR>
  4: }
  5: 

*** End of source buffer ***


>>> Testing console command: say(['select', 'horiz_pos\horizontal position', '=\equals'])

Heard select horizontal position equals
*** Start of source buffer ***
  1: for (<SEL_START>horiz_pos=<SEL_END>0;  <= ; ++)
  2: {
  3: 
  4: }


>>> Testing console command: quit(save_speech_files=0, disconnect=0)



*******************************************************************************
* Name        : misc_bugs
* Description : Testing a series of miscellaneous bugs that might reoccur.
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file(r'blah.py')

WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['<\less-than', '>\greater-than', '=\equal-sign'])

Heard less than greater than equal sign
*** Start of source buffer ***
  1:  <> =<CURSOR>

*** End of source buffer ***


*******************************************************************************
* Name        : persistence
* Description : testing persistence between VoiceCode sessions
*******************************************************************************



>>> Starting mediator with persistence
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Error reading <SymDict.SymDict instance at 27a7f20> from file 'H:\Projects\VoiceCode\VCode\Data\Tmp\tmp_symdict.pkl'
[Errno 2] No such file or directory: 'H:\\Projects\\VoiceCode\\VCode\\Data\\Tmp\\tmp_symdict.pkl'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: compile_symbols([r'H:\Projects\VoiceCode\VCode\Data\TestData\small_buff.c'])

Compiling symbols for file '%VCODE_HOME%\Data\TestData\small_buff.c'
>>> Known symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Restarting mediator with persistence. Compiled symbols should still be in the dictionary.



>>> Testing console command: quit(save_speech_files=0, disconnect=0)

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: print_symbols()

_cached_symbols_as_one_string is:
   


>>> Restarting mediator WITHOUT persistence. There should be NO symbols in the dictionary.



>>> Testing console command: quit(save_speech_files=0, disconnect=0)

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: print_symbols()

_cached_symbols_as_one_string is:
   


>>> Testing console command: quit(save_speech_files=0, disconnect=0)



*******************************************************************************
* Name        : punctuation
* Description : testing the various Python CSCs and LSAs
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' \\blank space', ' = \\equals', ' \\space bar', 'index', '*\\asterisk', '2', '**\\double asterisk', '8', '\012\\newline']
Heard variable blank space equals space bar index asterisk 2 double asterisk 8 newline
Associate 'variable' with symbol (Enter selection):

  '0': no association
  '1': variable (*new*)
  '2': Variable (*new*)
  '3': VARIABLE (*new*)

> Associate 'index' with symbol (Enter selection):

  '0': no association
  '1': index (*new*)
  '2': Index (*new*)
  '3': INDEX (*new*)

> *** Start of source buffer ***
  1: variable  =  Index*2**8
  2: <CURSOR>

*** End of source buffer ***
Saying: ['variable', 'equals', 'variable', '/\\slash', '2', '+\\plus sign', '1', '-\\minus sign', 'index', 'new statement']
Heard variable equals variable slash 2 plus sign 1 minus sign index new statement
*** Start of source buffer ***
  1: variable  =  Index*2**8
  2: variable = variable/2+1-Index
  3: <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' = \\equals', 'index', '%\\percent', '2', ' + \\plus', 'index', '%\\percent sign', '3', 'new statement']
Heard variable equals index percent 2 plus index percent sign 3 new statement
*** Start of source buffer ***
  1: variable  =  Index*2**8
  2: variable = variable/2+1-Index
  3: variable = Index%2 + Index%3
  4: <CURSOR>

*** End of source buffer ***
Saying: ['if', 'index', '&\\and percent', 'variable', 'then']
Heard if index and percent variable then
  2: variable = variable/2+1-Index
  3: variable = Index%2 + Index%3
  4: if Index&variable:
  5:    <CURSOR>

*** End of source buffer ***
Saying: ['if', 'index', '|\\pipe', 'variable', '|\\pipe sign', 'index', '|\\vertical bar', 'value', 'then']
Heard if index pipe variable pipe sign index vertical bar value then
Associate 'value' with symbol (Enter selection):

  '0': no association
  '1': value (*new*)
  '2': Value (*new*)
  '3': VALUE (*new*)

>   3: variable = Index%2 + Index%3
  4: if Index&variable:
  5:    if Index|variable|Index|Value:
  6:       <CURSOR>

*** End of source buffer ***
Saying: ['index', ' = \\equals', '0', ';\\semicolon', 'variable', ' = \\equals', '0', ';\\semi', 'new statement']
Heard index equals 0 semicolon variable equals 0 semi new statement
  4: if Index&variable:
  5:    if Index|variable|Index|Value:
  6:       Index = 0;variable = 0;
  7:       <CURSOR>

*** End of source buffer ***
Saying: ['index', '.\\dot', 'function', '()\\without arguments', 'new statement']
Heard index dot function without arguments new statement
Associate 'function' with symbol (Enter selection):

  '0': no association
  '1': function (*new*)
  '2': Function (*new*)
  '3': FUNCTION (*new*)

>   5:    if Index|variable|Index|Value:
  6:       Index = 0;variable = 0;
  7:       Index.Function()
  8:       <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' = \\equals', 'new', 'list', '0', '...\\ellipsis', '10', 'new statement']
Heard variable equals new list 0 ellipsis 10 new statement
  6:       Index = 0;variable = 0;
  7:       Index.Function()
  8:       variable = [0...10]
  9:       <CURSOR>

*** End of source buffer ***
Saying: ['#\\pound', '!\\bang', 'python', 'new statement']
Heard pound bang python new statement
Associate 'python' with symbol (Enter selection):

  '0': no association
  '1': python (*new*)
  '2': Python (*new*)
  '3': PYTHON (*new*)

>   7:       Index.Function()
  8:       variable = [0...10]
  9:       #!Python
 10:       <CURSOR>

*** End of source buffer ***
Saying: ['#\\pound sign', '!\\exclamation mark', 'python', 'new statement']
Heard pound sign exclamation mark python new statement
  8:       variable = [0...10]
  9:       #!Python
 10:       #!Python
 11:       <CURSOR>

*** End of source buffer ***
Saying: ['if', '~\\tilde', 'index', 'and', '~\\squiggle', 'variable', 'then']
Heard if tilde index and squiggle variable then
  9:       #!Python
 10:       #!Python
 11:       if ~Index and ~variable:
 12:          <CURSOR>

*** End of source buffer ***
Saying: ['variable', '::\\double colon', 'index', '::\\colon colon', 'field', 'new statement']
Heard variable double colon index colon colon field new statement
Associate 'field' with symbol (Enter selection):

  '0': no association
  '1': field (*new*)
  '2': Field (*new*)
  '3': FIELD (*new*)

>  10:       #!Python
 11:       if ~Index and ~variable:
 12:          variable::Index::Field
 13:          <CURSOR>

*** End of source buffer ***
Saying: ['if', 'index', '<\\less sign', '0', ' and \\and', 'index', '>\\greater sign', '-\\minus sign', '1', 'then']
Heard if index less sign 0 and index greater sign minus sign 1 then
 11:       if ~Index and ~variable:
 12:          variable::Index::Field
 13:          if Index<0 and Index>-1:
 14:             <CURSOR>

*** End of source buffer ***
Saying: ['index', '=\\equal sign', '0', 'new statement']
Heard index equal sign 0 new statement
 12:          variable::Index::Field
 13:          if Index<0 and Index>-1:
 14:             Index=0
 15:             <CURSOR>

*** End of source buffer ***
Saying: ['function', '(\\open paren', '0', ')\\close paren', 'new statement']
Heard function open paren 0 close paren new statement
 13:          if Index<0 and Index>-1:
 14:             Index=0
 15:             Function(0)
 16:             <CURSOR>

*** End of source buffer ***
Saying: ['function', 'parens', '0', 'new statement']
Heard function parens 0 new statement
 14:             Index=0
 15:             Function(0)
 16:             Function(0)
 17:             <CURSOR>

*** End of source buffer ***
Saying: ['function', '()\\empty parens', 'new statement']
Heard function empty parens new statement
 15:             Function(0)
 16:             Function(0)
 17:             Function()
 18:             <CURSOR>

*** End of source buffer ***
Saying: ['list', '[\\open bracket', '0', ']\\close bracket', 'new statement']
Heard list open bracket 0 close bracket new statement
Associate 'list' with symbol (Enter selection):

  '0': no association
  '1': list (*new*)
  '2': List (*new*)
  '3': LIST (*new*)

>  16:             Function(0)
 17:             Function()
 18:             List[0]
 19:             <CURSOR>

*** End of source buffer ***
Saying: ['list', 'brackets', '0', 'new statement']
Heard list brackets 0 new statement
 17:             Function()
 18:             List[0]
 19:             List[0]
 20:             <CURSOR>

*** End of source buffer ***
Saying: ['list', '[]\\empty brackets', 'new statement']
Heard list empty brackets new statement
 18:             List[0]
 19:             List[0]
 20:             List[]
 21:             <CURSOR>

*** End of source buffer ***
Saying: ['dictionary', 'braces', '0', 'new statement']
Heard dictionary braces 0 new statement
Associate 'dictionary' with symbol (Enter selection):

  '0': no association
  '1': dictionary (*new*)
  '2': Dictionary (*new*)
  '3': DICTIONARY (*new*)

>  19:             List[0]
 20:             List[]
 21:             Dictionary{0}
 22:             <CURSOR>

*** End of source buffer ***
Saying: ['<\\open angled', 'head', '>\\close angled', 'new statement']
Heard open angled head close angled new statement
Associate 'head' with symbol (Enter selection):

  '0': no association
  '1': head (*new*)
  '2': Head (*new*)
  '3': HEAD (*new*)

>  20:             List[]
 21:             Dictionary{0}
 22:             <Head>
 23:             <CURSOR>

*** End of source buffer ***
Saying: ['angled brackets', 'head', 'new statement']
Heard angled brackets head new statement
 21:             Dictionary{0}
 22:             <Head>
 23:             <Head>
 24:             <CURSOR>

*** End of source buffer ***
Saying: ['<>\\empty angled', 'new statement']
Heard empty angled new statement
 22:             <Head>
 23:             <Head>
 24:             <>
 25:             <CURSOR>

*** End of source buffer ***
Saying: ['string', ' = \\equals', "'\\open single quote", 'message', "'\\close single quote", 'new statement']
Heard string equals open single quote message close single quote new statement
Associate 'string' with symbol (Enter selection):

  '0': no association
  '1': string (*new*)
  '2': String (*new*)
  '3': STRING (*new*)

> Associate 'message' with symbol (Enter selection):

  '0': no association
  '1': message (*new*)
  '2': Message (*new*)
  '3': MESSAGE (*new*)

>  23:             <Head>
 24:             <>
 25:             String = 'Message'
 26:             <CURSOR>

*** End of source buffer ***
Saying: ['string', 'equals', 'single', 'quotes', 'message', 'new statement']
Heard string equals single quotes message new statement
 24:             <>
 25:             String = 'Message'
 26:             String = 'Message'
 27:             <CURSOR>

*** End of source buffer ***
Saying: ["''\\empty single quotes", 'new statement']
Heard empty single quotes new statement
 25:             String = 'Message'
 26:             String = 'Message'
 27:             ''
 28:             <CURSOR>

*** End of source buffer ***
Saying: ['string', ' = \\equals', '"\\open quote', 'message', '"\\close quote', 'new statement']
Heard string equals open quote message close quote new statement
 26:             String = 'Message'
 27:             ''
 28:             String = "Message"
 29:             <CURSOR>

*** End of source buffer ***
Saying: ['string', 'equals', 'quotes', 'message', 'new statement']
Heard string equals quotes message new statement
 27:             ''
 28:             String = "Message"
 29:             String = "Message"
 30:             <CURSOR>

*** End of source buffer ***
Saying: ['""\\empty quotes', 'new statement']
Heard empty quotes new statement
 28:             String = "Message"
 29:             String = "Message"
 30:             ""
 31:             <CURSOR>

*** End of source buffer ***
Saying: ['string', ' = \\equals', '`\\open back quote', 'message', '`\\close back quote', 'new statement']
Heard string equals open back quote message close back quote new statement
 29:             String = "Message"
 30:             ""
 31:             String = `Message`
 32:             <CURSOR>

*** End of source buffer ***
Saying: ['string', ' = \\equals', 'back', 'quotes', 'message', 'new statement']
Heard string equals back quotes message new statement
 30:             ""
 31:             String = `Message`
 32:             String = `Message`
 33:             <CURSOR>

*** End of source buffer ***
Saying: ['``\\empty back quotes', 'new statement']
Heard empty back quotes new statement
 31:             String = `Message`
 32:             String = `Message`
 33:             ``
 34:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 31:             String = `Message`
 32:             String = `Message`
 33:             ``
 34:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\a\\back slash a.', 'new statement']
Heard back slash a new statement
 32:             String = `Message`
 33:             ``
 34:             "\a"
 35:             <CURSOR>

*** End of source buffer ***
Saying: ['\\a\\back slash alpha', 'new statement']
Heard back slash alpha new statement
 33:             ``
 34:             "\a"
 35:             \a
 36:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 33:             ``
 34:             "\a"
 35:             \a
 36:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\b\\back slash b.']
Heard back slash b
 33:             ``
 34:             "\a"
 35:             \a
 36:             "\b<CURSOR>"

*** End of source buffer ***
Saying: ['\\b\\back slash bravo']
Heard back slash bravo
 33:             ``
 34:             "\a"
 35:             \a
 36:             "\b\b<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 34:             "\a"
 35:             \a
 36:             "\b\b"
 37:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 34:             "\a"
 35:             \a
 36:             "\b\b"
 37:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\c\\back slash c.']
Heard back slash c
 34:             "\a"
 35:             \a
 36:             "\b\b"
 37:             "\c<CURSOR>"

*** End of source buffer ***
Saying: ['\\c\\back slash charlie']
Heard back slash charlie
 34:             "\a"
 35:             \a
 36:             "\b\b"
 37:             "\c\c<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 35:             \a
 36:             "\b\b"
 37:             "\c\c"
 38:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 35:             \a
 36:             "\b\b"
 37:             "\c\c"
 38:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\d\\back slash d.']
Heard back slash d
 35:             \a
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d<CURSOR>"

*** End of source buffer ***
Saying: ['\\d\\back slash delta']
Heard back slash delta
 35:             \a
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d\d<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d\d"
 39:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d\d"
 39:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\e\\back slash e.']
Heard back slash e
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e<CURSOR>"

*** End of source buffer ***
Saying: ['\\e\\back slash echo']
Heard back slash echo
 36:             "\b\b"
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e\e<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e\e"
 40:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e\e"
 40:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\f\\back slash f.']
Heard back slash f
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f<CURSOR>"

*** End of source buffer ***
Saying: ['\\f\\back slash foxtrot']
Heard back slash foxtrot
 37:             "\c\c"
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f\f<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f\f"
 41:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f\f"
 41:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\g\\back slash g.']
Heard back slash g
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g<CURSOR>"

*** End of source buffer ***
Saying: ['\\g\\back slash golf']
Heard back slash golf
 38:             "\d\d"
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g\g<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g\g"
 42:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g\g"
 42:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\h\\back slash h.']
Heard back slash h
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h<CURSOR>"

*** End of source buffer ***
Saying: ['\\h\\back slash hotel']
Heard back slash hotel
 39:             "\e\e"
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h\h<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h\h"
 43:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h\h"
 43:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\i\\back slash i.']
Heard back slash i
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i<CURSOR>"

*** End of source buffer ***
Saying: ['\\i\\back slash india']
Heard back slash india
 40:             "\f\f"
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i\i<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i\i"
 44:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i\i"
 44:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\j\\back slash j.']
Heard back slash j
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j<CURSOR>"

*** End of source buffer ***
Saying: ['\\j\\back slash juliett']
Heard back slash juliett
 41:             "\g\g"
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j\j<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j\j"
 45:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j\j"
 45:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\k\\back slash k.']
Heard back slash k
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k<CURSOR>"

*** End of source buffer ***
Saying: ['\\k\\back slash kilo']
Heard back slash kilo
 42:             "\h\h"
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k\k<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k\k"
 46:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k\k"
 46:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\l\\back slash l.']
Heard back slash l
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l<CURSOR>"

*** End of source buffer ***
Saying: ['\\l\\back slash lima']
Heard back slash lima
 43:             "\i\i"
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l\l<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l\l"
 47:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l\l"
 47:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\m\\back slash m.']
Heard back slash m
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m<CURSOR>"

*** End of source buffer ***
Saying: ['\\m\\back slash mike']
Heard back slash mike
 44:             "\j\j"
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m\m<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m\m"
 48:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m\m"
 48:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\n\\back slash n.']
Heard back slash n
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n<CURSOR>"

*** End of source buffer ***
Saying: ['\\n\\back slash november']
Heard back slash november
 45:             "\k\k"
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n\n<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n\n"
 49:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n\n"
 49:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\o\\back slash o.']
Heard back slash o
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o<CURSOR>"

*** End of source buffer ***
Saying: ['\\o\\back slash oscar']
Heard back slash oscar
 46:             "\l\l"
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o\o<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o\o"
 50:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o\o"
 50:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\p\\back slash p.']
Heard back slash p
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p<CURSOR>"

*** End of source buffer ***
Saying: ['\\p\\back slash papa']
Heard back slash papa
 47:             "\m\m"
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p\p<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p\p"
 51:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p\p"
 51:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\q\\back slash q.']
Heard back slash q
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q<CURSOR>"

*** End of source buffer ***
Saying: ['\\q\\back slash quebec']
Heard back slash quebec
 48:             "\n\n"
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q\q<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q\q"
 52:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q\q"
 52:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\r\\back slash r.']
Heard back slash r
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r<CURSOR>"

*** End of source buffer ***
Saying: ['\\r\\back slash romeo']
Heard back slash romeo
 49:             "\o\o"
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r\r<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r\r"
 53:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r\r"
 53:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\s\\back slash s.']
Heard back slash s
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s<CURSOR>"

*** End of source buffer ***
Saying: ['\\s\\back slash sierra']
Heard back slash sierra
 50:             "\p\p"
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s\s<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s\s"
 54:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s\s"
 54:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\t\\back slash t.']
Heard back slash t
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t<CURSOR>"

*** End of source buffer ***
Saying: ['\\t\\back slash tango']
Heard back slash tango
 51:             "\q\q"
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t\t<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t\t"
 55:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t\t"
 55:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\u\\back slash u.']
Heard back slash u
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u<CURSOR>"

*** End of source buffer ***
Saying: ['\\u\\back slash uniform']
Heard back slash uniform
 52:             "\r\r"
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u\u<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u\u"
 56:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u\u"
 56:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\v\\back slash v.']
Heard back slash v
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v<CURSOR>"

*** End of source buffer ***
Saying: ['\\v\\back slash victor']
Heard back slash victor
 53:             "\s\s"
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v\v<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v\v"
 57:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v\v"
 57:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\w\\back slash w.']
Heard back slash w
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w<CURSOR>"

*** End of source buffer ***
Saying: ['\\w\\back slash whiskey']
Heard back slash whiskey
 54:             "\t\t"
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w\w<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w\w"
 58:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w\w"
 58:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\x\\back slash x.']
Heard back slash x
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x<CURSOR>"

*** End of source buffer ***
Saying: ['\\x\\back slash xray']
Heard back slash xray
 55:             "\u\u"
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x\x<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x\x"
 59:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x\x"
 59:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\y\\back slash y.']
Heard back slash y
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y<CURSOR>"

*** End of source buffer ***
Saying: ['\\y\\back slash yankee']
Heard back slash yankee
 56:             "\v\v"
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y\y<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y\y"
 60:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y\y"
 60:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\z\\back slash z.']
Heard back slash z
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y\y"
 60:             "\z<CURSOR>"

*** End of source buffer ***
Saying: ['\\z\\back slash zulu']
Heard back slash zulu
 57:             "\w\w"
 58:             "\x\x"
 59:             "\y\y"
 60:             "\z\z<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 58:             "\x\x"
 59:             "\y\y"
 60:             "\z\z"
 61:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 58:             "\x\x"
 59:             "\y\y"
 60:             "\z\z"
 61:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\A\\back slash cap a.']
Heard back slash cap a
 58:             "\x\x"
 59:             "\y\y"
 60:             "\z\z"
 61:             "\A<CURSOR>"

*** End of source buffer ***
Saying: ['\\A\\back slash cap alpha', 'new statement']
Heard back slash cap alpha new statement
 59:             "\y\y"
 60:             "\z\z"
 61:             "\A\A"
 62:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 59:             "\y\y"
 60:             "\z\z"
 61:             "\A\A"
 62:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\B\\back slash cap b.']
Heard back slash cap b
 59:             "\y\y"
 60:             "\z\z"
 61:             "\A\A"
 62:             "\B<CURSOR>"

*** End of source buffer ***
Saying: ['\\B\\back slash cap bravo', 'new statement']
Heard back slash cap bravo new statement
 60:             "\z\z"
 61:             "\A\A"
 62:             "\B\B"
 63:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 60:             "\z\z"
 61:             "\A\A"
 62:             "\B\B"
 63:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\D\\back slash cap d.']
Heard back slash cap d
 60:             "\z\z"
 61:             "\A\A"
 62:             "\B\B"
 63:             "\D<CURSOR>"

*** End of source buffer ***
Saying: ['\\D\\back slash cap delta', 'new statement']
Heard back slash cap delta new statement
 61:             "\A\A"
 62:             "\B\B"
 63:             "\D\D"
 64:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 61:             "\A\A"
 62:             "\B\B"
 63:             "\D\D"
 64:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\E\\back slash cap e.']
Heard back slash cap e
 61:             "\A\A"
 62:             "\B\B"
 63:             "\D\D"
 64:             "\E<CURSOR>"

*** End of source buffer ***
Saying: ['\\E\\back slash cap echo', 'new statement']
Heard back slash cap echo new statement
 62:             "\B\B"
 63:             "\D\D"
 64:             "\E\E"
 65:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 62:             "\B\B"
 63:             "\D\D"
 64:             "\E\E"
 65:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\F\\back slash cap f.']
Heard back slash cap f
 62:             "\B\B"
 63:             "\D\D"
 64:             "\E\E"
 65:             "\F<CURSOR>"

*** End of source buffer ***
Saying: ['\\F\\back slash cap foxtrot', 'new statement']
Heard back slash cap foxtrot new statement
 63:             "\D\D"
 64:             "\E\E"
 65:             "\F\F"
 66:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 63:             "\D\D"
 64:             "\E\E"
 65:             "\F\F"
 66:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\G\\back slash cap g.']
Heard back slash cap g
 63:             "\D\D"
 64:             "\E\E"
 65:             "\F\F"
 66:             "\G<CURSOR>"

*** End of source buffer ***
Saying: ['\\G\\back slash cap golf', 'new statement']
Heard back slash cap golf new statement
 64:             "\E\E"
 65:             "\F\F"
 66:             "\G\G"
 67:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 64:             "\E\E"
 65:             "\F\F"
 66:             "\G\G"
 67:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\H\\back slash cap h.']
Heard back slash cap h
 64:             "\E\E"
 65:             "\F\F"
 66:             "\G\G"
 67:             "\H<CURSOR>"

*** End of source buffer ***
Saying: ['\\H\\back slash cap hotel', 'new statement']
Heard back slash cap hotel new statement
 65:             "\F\F"
 66:             "\G\G"
 67:             "\H\H"
 68:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 65:             "\F\F"
 66:             "\G\G"
 67:             "\H\H"
 68:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\I\\back slash cap i.']
Heard back slash cap i
 65:             "\F\F"
 66:             "\G\G"
 67:             "\H\H"
 68:             "\I<CURSOR>"

*** End of source buffer ***
Saying: ['\\I\\back slash cap india', 'new statement']
Heard back slash cap india new statement
 66:             "\G\G"
 67:             "\H\H"
 68:             "\I\I"
 69:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 66:             "\G\G"
 67:             "\H\H"
 68:             "\I\I"
 69:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\J\\back slash cap j.']
Heard back slash cap j
 66:             "\G\G"
 67:             "\H\H"
 68:             "\I\I"
 69:             "\J<CURSOR>"

*** End of source buffer ***
Saying: ['\\J\\back slash cap juliett', 'new statement']
Heard back slash cap juliett new statement
 67:             "\H\H"
 68:             "\I\I"
 69:             "\J\J"
 70:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 67:             "\H\H"
 68:             "\I\I"
 69:             "\J\J"
 70:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\K\\back slash cap k.']
Heard back slash cap k
 67:             "\H\H"
 68:             "\I\I"
 69:             "\J\J"
 70:             "\K<CURSOR>"

*** End of source buffer ***
Saying: ['\\K\\back slash cap kilo', 'new statement']
Heard back slash cap kilo new statement
 68:             "\I\I"
 69:             "\J\J"
 70:             "\K\K"
 71:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 68:             "\I\I"
 69:             "\J\J"
 70:             "\K\K"
 71:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\L\\back slash cap l.']
Heard back slash cap l
 68:             "\I\I"
 69:             "\J\J"
 70:             "\K\K"
 71:             "\L<CURSOR>"

*** End of source buffer ***
Saying: ['\\L\\back slash cap lima', 'new statement']
Heard back slash cap lima new statement
 69:             "\J\J"
 70:             "\K\K"
 71:             "\L\L"
 72:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 69:             "\J\J"
 70:             "\K\K"
 71:             "\L\L"
 72:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\M\\back slash cap m.']
Heard back slash cap m
 69:             "\J\J"
 70:             "\K\K"
 71:             "\L\L"
 72:             "\M<CURSOR>"

*** End of source buffer ***
Saying: ['\\M\\back slash cap mike', 'new statement']
Heard back slash cap mike new statement
 70:             "\K\K"
 71:             "\L\L"
 72:             "\M\M"
 73:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 70:             "\K\K"
 71:             "\L\L"
 72:             "\M\M"
 73:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\N\\back slash cap n.']
Heard back slash cap n
 70:             "\K\K"
 71:             "\L\L"
 72:             "\M\M"
 73:             "\N<CURSOR>"

*** End of source buffer ***
Saying: ['\\N\\back slash cap november', 'new statement']
Heard back slash cap november new statement
 71:             "\L\L"
 72:             "\M\M"
 73:             "\N\N"
 74:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 71:             "\L\L"
 72:             "\M\M"
 73:             "\N\N"
 74:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\O\\back slash cap o.']
Heard back slash cap o
 71:             "\L\L"
 72:             "\M\M"
 73:             "\N\N"
 74:             "\O<CURSOR>"

*** End of source buffer ***
Saying: ['\\O\\back slash cap oscar', 'new statement']
Heard back slash cap oscar new statement
 72:             "\M\M"
 73:             "\N\N"
 74:             "\O\O"
 75:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 72:             "\M\M"
 73:             "\N\N"
 74:             "\O\O"
 75:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\P\\back slash cap p.']
Heard back slash cap p
 72:             "\M\M"
 73:             "\N\N"
 74:             "\O\O"
 75:             "\P<CURSOR>"

*** End of source buffer ***
Saying: ['\\P\\back slash cap papa', 'new statement']
Heard back slash cap papa new statement
 73:             "\N\N"
 74:             "\O\O"
 75:             "\P\P"
 76:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 73:             "\N\N"
 74:             "\O\O"
 75:             "\P\P"
 76:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\Q\\back slash cap q.']
Heard back slash cap q
 73:             "\N\N"
 74:             "\O\O"
 75:             "\P\P"
 76:             "\Q<CURSOR>"

*** End of source buffer ***
Saying: ['\\Q\\back slash cap quebec', 'new statement']
Heard back slash cap quebec new statement
 74:             "\O\O"
 75:             "\P\P"
 76:             "\Q\Q"
 77:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 74:             "\O\O"
 75:             "\P\P"
 76:             "\Q\Q"
 77:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\R\\back slash cap r.']
Heard back slash cap r
 74:             "\O\O"
 75:             "\P\P"
 76:             "\Q\Q"
 77:             "\R<CURSOR>"

*** End of source buffer ***
Saying: ['\\R\\back slash cap romeo', 'new statement']
Heard back slash cap romeo new statement
 75:             "\P\P"
 76:             "\Q\Q"
 77:             "\R\R"
 78:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 75:             "\P\P"
 76:             "\Q\Q"
 77:             "\R\R"
 78:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\S\\back slash cap s.']
Heard back slash cap s
 75:             "\P\P"
 76:             "\Q\Q"
 77:             "\R\R"
 78:             "\S<CURSOR>"

*** End of source buffer ***
Saying: ['\\S\\back slash cap sierra', 'new statement']
Heard back slash cap sierra new statement
 76:             "\Q\Q"
 77:             "\R\R"
 78:             "\S\S"
 79:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 76:             "\Q\Q"
 77:             "\R\R"
 78:             "\S\S"
 79:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\T\\back slash cap t.']
Heard back slash cap t
 76:             "\Q\Q"
 77:             "\R\R"
 78:             "\S\S"
 79:             "\T<CURSOR>"

*** End of source buffer ***
Saying: ['\\T\\back slash cap tango', 'new statement']
Heard back slash cap tango new statement
 77:             "\R\R"
 78:             "\S\S"
 79:             "\T\T"
 80:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 77:             "\R\R"
 78:             "\S\S"
 79:             "\T\T"
 80:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\U\\back slash cap u.']
Heard back slash cap u
 77:             "\R\R"
 78:             "\S\S"
 79:             "\T\T"
 80:             "\U<CURSOR>"

*** End of source buffer ***
Saying: ['\\U\\back slash cap uniform', 'new statement']
Heard back slash cap uniform new statement
 78:             "\S\S"
 79:             "\T\T"
 80:             "\U\U"
 81:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 78:             "\S\S"
 79:             "\T\T"
 80:             "\U\U"
 81:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\V\\back slash cap v.']
Heard back slash cap v
 78:             "\S\S"
 79:             "\T\T"
 80:             "\U\U"
 81:             "\V<CURSOR>"

*** End of source buffer ***
Saying: ['\\V\\back slash cap victor', 'new statement']
Heard back slash cap victor new statement
 79:             "\T\T"
 80:             "\U\U"
 81:             "\V\V"
 82:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 79:             "\T\T"
 80:             "\U\U"
 81:             "\V\V"
 82:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\W\\back slash cap w.']
Heard back slash cap w
 79:             "\T\T"
 80:             "\U\U"
 81:             "\V\V"
 82:             "\W<CURSOR>"

*** End of source buffer ***
Saying: ['\\W\\back slash cap whiskey', 'new statement']
Heard back slash cap whiskey new statement
 80:             "\U\U"
 81:             "\V\V"
 82:             "\W\W"
 83:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 80:             "\U\U"
 81:             "\V\V"
 82:             "\W\W"
 83:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\X\\back slash cap x.']
Heard back slash cap x
 80:             "\U\U"
 81:             "\V\V"
 82:             "\W\W"
 83:             "\X<CURSOR>"

*** End of source buffer ***
Saying: ['\\X\\back slash cap xray', 'new statement']
Heard back slash cap xray new statement
 81:             "\V\V"
 82:             "\W\W"
 83:             "\X\X"
 84:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 81:             "\V\V"
 82:             "\W\W"
 83:             "\X\X"
 84:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\Y\\back slash cap y.']
Heard back slash cap y
 81:             "\V\V"
 82:             "\W\W"
 83:             "\X\X"
 84:             "\Y<CURSOR>"

*** End of source buffer ***
Saying: ['\\Y\\back slash cap yankee', 'new statement']
Heard back slash cap yankee new statement
 82:             "\W\W"
 83:             "\X\X"
 84:             "\Y\Y"
 85:             <CURSOR>

*** End of source buffer ***
Saying: ['quotes']
Heard quotes
 82:             "\W\W"
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "<CURSOR>"

*** End of source buffer ***
Saying: ['\\Z\\back slash cap z.']
Heard back slash cap z
 82:             "\W\W"
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z<CURSOR>"

*** End of source buffer ***
Saying: ['\\Z\\back slash cap zulu', 'new statement']
Heard back slash cap zulu new statement
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             <CURSOR>

*** End of source buffer ***
Saying: ['index', 'semi', 'variable', 'semi']
Heard index semi variable semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;<CURSOR>

*** End of source buffer ***
Saying: ['previous semi', 'previous semi']
Heard previous semi previous semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;<CURSOR>variable;

*** End of source buffer ***
Saying: ['after semi']
Heard after semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;<CURSOR>

*** End of source buffer ***
Saying: ['before previous semi']
Heard before previous semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable<CURSOR>;

*** End of source buffer ***
Saying: ['after semi']
Heard after semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;<CURSOR>

*** End of source buffer ***
Saying: ['before semi']
Heard before semi
 83:             "\X\X"
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;<CURSOR>

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' = \\equals', 'brackets', '0', ',\\comma', '1', ',\\comma', '3']
Heard variable equals brackets 0 comma 1 comma 3
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3<CURSOR>]

*** End of source buffer ***
Saying: ['previous comma']
Heard previous comma
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, <CURSOR>3]

*** End of source buffer ***
Saying: ['after comma']
Heard after comma
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, <CURSOR>3]

*** End of source buffer ***
Saying: ['before previous comma']
Heard before previous comma
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1<CURSOR>, 3]

*** End of source buffer ***
Saying: ['before next comma']
Heard before next comma
 84:             "\Y\Y"
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1<CURSOR>, 3]

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', '.\\dot', 'field', '.\\dot', 'value']
Heard variable dot field dot value
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value<CURSOR>

*** End of source buffer ***
Saying: ['previous dot', 'previous dot']
Heard previous dot previous dot
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.<CURSOR>Field.Value

*** End of source buffer ***
Saying: ['after dot']
Heard after dot
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.<CURSOR>Value

*** End of source buffer ***
Saying: ['before previous dot']
Heard before previous dot
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field<CURSOR>.Value

*** End of source buffer ***
Saying: ['before next dot']
Heard before next dot
 85:             "\Z\Z"
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field<CURSOR>.Value

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             <CURSOR>

*** End of source buffer ***
Saying: ['braces', 'variable', ': \\colon', '0', 'value', ': \\colon', '0']
Heard braces variable colon 0 value colon 0
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0<CURSOR>}

*** End of source buffer ***
Saying: ['previous colon', 'previous colon']
Heard previous colon previous colon
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: <CURSOR>0 Value: 0}

*** End of source buffer ***
Saying: ['after colon']
Heard after colon
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: <CURSOR>0}

*** End of source buffer ***
Saying: ['before previous colon']
Heard before previous colon
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value<CURSOR>: 0}

*** End of source buffer ***
Saying: ['before next colon']
Heard before next colon
 86:             Index;variable;
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value<CURSOR>: 0}

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' = \\equals', '2', '*\\asterisk', '3', '*\\asterisk', '4']
Heard variable equals 2 asterisk 3 asterisk 4
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4<CURSOR>

*** End of source buffer ***
Saying: ['previous asterisk', 'previous star']
Heard previous asterisk previous star
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*<CURSOR>3*4

*** End of source buffer ***
Saying: ['after star']
Heard after star
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*<CURSOR>4

*** End of source buffer ***
Saying: ['before previous asterisk']
Heard before previous asterisk
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3<CURSOR>*4

*** End of source buffer ***
Saying: ['before next star']
Heard before next star
 87:             variable = [0, 1, 3]
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3<CURSOR>*4

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', 'equals', '2', '/\\slash', '3', '/\\slash', '4']
Heard variable equals 2 slash 3 slash 4
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4<CURSOR>

*** End of source buffer ***
Saying: ['previous slash', 'previous slash']
Heard previous slash previous slash
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/<CURSOR>3/4

*** End of source buffer ***
Saying: ['after slash']
Heard after slash
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/<CURSOR>4

*** End of source buffer ***
Saying: ['before previous slash']
Heard before previous slash
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3<CURSOR>/4

*** End of source buffer ***
Saying: ['before next slash']
Heard before next slash
 88:             variable.Field.Value
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3<CURSOR>/4

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', ' = \\equals', '2', ' + \\plus', '3', ' + \\plus', '4']
Heard variable equals 2 plus 3 plus 4
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4<CURSOR>

*** End of source buffer ***
Saying: ['previous plus', 'previous plus']
Heard previous plus previous plus
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + <CURSOR>3 + 4

*** End of source buffer ***
Saying: ['after plus']
Heard after plus
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + <CURSOR>4

*** End of source buffer ***
Saying: ['before previous plus']
Heard before previous plus
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3<CURSOR> + 4

*** End of source buffer ***
Saying: ['before next plus']
Heard before next plus
 89:             {variable: 0 Value: 0}
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3<CURSOR> + 4

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', 'equals', '2', ' - \\minus', '3', ' - \\minus', '4']
Heard variable equals 2 minus 3 minus 4
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4<CURSOR>

*** End of source buffer ***
Saying: ['previous minus', 'previous minus']
Heard previous minus previous minus
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - <CURSOR>3 - 4

*** End of source buffer ***
Saying: ['after minus']
Heard after minus
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - <CURSOR>4

*** End of source buffer ***
Saying: ['before previous minus']
Heard before previous minus
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3<CURSOR> - 4

*** End of source buffer ***
Saying: ['before next minus']
Heard before next minus
 90:             variable = 2*3*4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3<CURSOR> - 4

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             <CURSOR>

*** End of source buffer ***
Saying: ['variable', 'equals', '2', ' % \\modulo', '3', ' % \\modulo', '4']
Heard variable equals 2 modulo 3 modulo 4
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4<CURSOR>

*** End of source buffer ***
Saying: ['previous percent', 'previous percent']
Heard previous percent previous percent
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % <CURSOR>3 % 4

*** End of source buffer ***
Saying: ['after percent']
Heard after percent
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % <CURSOR>4

*** End of source buffer ***
Saying: ['before previous percent']
Heard before previous percent
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3<CURSOR> % 4

*** End of source buffer ***
Saying: ['before next percent']
Heard before next percent
 91:             variable = 2/3/4
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3<CURSOR> % 4

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '&\\and percent', '1', '&\\and percent', '2']
Heard 0 and percent 1 and percent 2
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2<CURSOR>

*** End of source buffer ***
Saying: ['previous and percent', 'previous and percent']
Heard previous and percent previous and percent
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&<CURSOR>1&2

*** End of source buffer ***
Saying: ['after and percent']
Heard after and percent
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&<CURSOR>2

*** End of source buffer ***
Saying: ['before previous and percent']
Heard before previous and percent
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1<CURSOR>&2

*** End of source buffer ***
Saying: ['before next and percent']
Heard before next and percent
 92:             variable = 2 + 3 + 4
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1<CURSOR>&2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '|\\pipe', '1', '|\\pipe', '2']
Heard 0 pipe 1 pipe 2
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2<CURSOR>

*** End of source buffer ***
Saying: ['previous pipe', 'previous pipe']
Heard previous pipe previous pipe
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|<CURSOR>1|2

*** End of source buffer ***
Saying: ['after pipe']
Heard after pipe
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|<CURSOR>2

*** End of source buffer ***
Saying: ['before previous pipe']
Heard before previous pipe
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1<CURSOR>|2

*** End of source buffer ***
Saying: ['before next pipe']
Heard before next pipe
 93:             variable = 2 - 3 - 4
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1<CURSOR>|2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '...\\ellipsis', '1', '...\\ellipsis', '2']
Heard 0 ellipsis 1 ellipsis 2
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2<CURSOR>

*** End of source buffer ***
Saying: ['previous ellipsis', 'previous ellipsis']
Heard previous ellipsis previous ellipsis
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             0...<CURSOR>1...2

*** End of source buffer ***
Saying: ['after ellipsis']
Heard after ellipsis
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             0...1...<CURSOR>2

*** End of source buffer ***
Saying: ['before previous ellipsis']
Heard before previous ellipsis
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             0...1<CURSOR>...2

*** End of source buffer ***
Saying: ['before next ellipsis']
Heard before next ellipsis
 94:             variable = 2 % 3 % 4
 95:             0&1&2
 96:             0|1|2
 97:             0...1<CURSOR>...2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '!\\bang', '1', '!\\bang', '2']
Heard 0 bang 1 bang 2
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2<CURSOR>

*** End of source buffer ***
Saying: ['previous bang', 'previous bang']
Heard previous bang previous bang
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             0!<CURSOR>1!2

*** End of source buffer ***
Saying: ['after bang']
Heard after bang
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             0!1!<CURSOR>2

*** End of source buffer ***
Saying: ['before previous bang']
Heard before previous bang
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             0!1<CURSOR>!2

*** End of source buffer ***
Saying: ['before next bang']
Heard before next bang
 95:             0&1&2
 96:             0|1|2
 97:             0...1...2
 98:             0!1<CURSOR>!2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '?\\question mark', '1', '?\\question mark', '2']
Heard 0 question mark 1 question mark 2
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2<CURSOR>

*** End of source buffer ***
Saying: ['previous question mark', 'previous question mark']
Heard previous question mark previous question mark
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             0?<CURSOR>1?2

*** End of source buffer ***
Saying: ['after question mark']
Heard after question mark
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             0?1?<CURSOR>2

*** End of source buffer ***
Saying: ['before previous question mark']
Heard before previous question mark
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             0?1<CURSOR>?2

*** End of source buffer ***
Saying: ['before next question mark']
Heard before next question mark
 96:             0|1|2
 97:             0...1...2
 98:             0!1!2
 99:             0?1<CURSOR>?2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '#\\pound', 'sign', '1', '#\\pound', 'sign', '2']
Heard 0 pound sign 1 pound sign 2
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             0#1#2<CURSOR>

*** End of source buffer ***
Saying: ['previous pound sign', 'previous pound sign']
Heard previous pound sign previous pound sign
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             0#<CURSOR>1#2

*** End of source buffer ***
Saying: ['after pound sign']
Heard after pound sign
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             0#1#<CURSOR>2

*** End of source buffer ***
Saying: ['before previous pound sign']
Heard before previous pound sign
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             0#1<CURSOR>#2

*** End of source buffer ***
Saying: ['before next pound sign']
Heard before next pound sign
 97:             0...1...2
 98:             0!1!2
 99:             0?1?2
100:             0#1<CURSOR>#2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '::\\double colon', '1', '::\\double colon', '2']
Heard 0 double colon 1 double colon 2
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             0::1::2<CURSOR>

*** End of source buffer ***
Saying: ['previous double colon', 'previous double colon']
Heard previous double colon previous double colon
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             0::<CURSOR>1::2

*** End of source buffer ***
Saying: ['after double colon']
Heard after double colon
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             0::1::<CURSOR>2

*** End of source buffer ***
Saying: ['before previous double colon']
Heard before previous double colon
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             0::1<CURSOR>::2

*** End of source buffer ***
Saying: ['before next double colon']
Heard before next double colon
 98:             0!1!2
 99:             0?1?2
100:             0#1#2
101:             0::1<CURSOR>::2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '~\\tilde', '1', '~\\tilde', '2']
Heard 0 tilde 1 tilde 2
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             0~1~2<CURSOR>

*** End of source buffer ***
Saying: ['previous tilde', 'previous tilde']
Heard previous tilde previous tilde
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             0~<CURSOR>1~2

*** End of source buffer ***
Saying: ['after tilde']
Heard after tilde
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             0~1~<CURSOR>2

*** End of source buffer ***
Saying: ['before previous tilde']
Heard before previous tilde
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             0~1<CURSOR>~2

*** End of source buffer ***
Saying: ['before next tilde']
Heard before next tilde
 99:             0?1?2
100:             0#1#2
101:             0::1::2
102:             0~1<CURSOR>~2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '<\\less sign', '1', '<\\less sign', '2']
Heard 0 less sign 1 less sign 2
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             0<1<2<CURSOR>

*** End of source buffer ***
Saying: ['previous less sign', 'previous less sign']
Heard previous less sign previous less sign
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             0<<CURSOR>1<2

*** End of source buffer ***
Saying: ['after less sign']
Heard after less sign
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             0<1<<CURSOR>2

*** End of source buffer ***
Saying: ['before previous less sign']
Heard before previous less sign
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             0<1<CURSOR><2

*** End of source buffer ***
Saying: ['before next less sign']
Heard before next less sign
100:             0#1#2
101:             0::1::2
102:             0~1~2
103:             0<1<CURSOR><2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '>\\greater sign', '1', '>\\greater sign', '2']
Heard 0 greater sign 1 greater sign 2
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             0>1>2<CURSOR>

*** End of source buffer ***
Saying: ['previous greater sign', 'previous greater sign']
Heard previous greater sign previous greater sign
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             0><CURSOR>1>2

*** End of source buffer ***
Saying: ['after greater sign']
Heard after greater sign
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             0>1><CURSOR>2

*** End of source buffer ***
Saying: ['before previous greater sign']
Heard before previous greater sign
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             0>1<CURSOR>>2

*** End of source buffer ***
Saying: ['before next greater sign']
Heard before next greater sign
101:             0::1::2
102:             0~1~2
103:             0<1<2
104:             0>1<CURSOR>>2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             <CURSOR>

*** End of source buffer ***
Saying: ['0', '=\\equal sign', '1', '=\\equal sign', '2']
Heard 0 equal sign 1 equal sign 2
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             0=1=2<CURSOR>

*** End of source buffer ***
Saying: ['previous equal sign', 'previous equal sign']
Heard previous equal sign previous equal sign
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             0=<CURSOR>1=2

*** End of source buffer ***
Saying: ['after equal sign']
Heard after equal sign
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             0=1=<CURSOR>2

*** End of source buffer ***
Saying: ['before previous equal sign']
Heard before previous equal sign
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             0=1<CURSOR>=2

*** End of source buffer ***
Saying: ['before next equal sign']
Heard before next equal sign
102:             0~1~2
103:             0<1<2
104:             0>1>2
105:             0=1<CURSOR>=2

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             <CURSOR>

*** End of source buffer ***
Saying: ['between parens', '1']
Heard between parens 1
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (1<CURSOR>)

*** End of source buffer ***
Saying: ['before previous paren']
Heard before previous paren
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:            <CURSOR> (1)

*** End of source buffer ***
Saying: ['after paren']
Heard after paren
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (<CURSOR>1)

*** End of source buffer ***
Saying: ['before paren']
Heard before paren
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (1<CURSOR>)

*** End of source buffer ***
Saying: ['previous paren']
Heard previous paren
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (<CURSOR>1)

*** End of source buffer ***
Saying: ['out of parens']
Heard out of parens
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (1)<CURSOR>

*** End of source buffer ***
Saying: ['before previous paren']
Heard before previous paren
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:             (1<CURSOR>)

*** End of source buffer ***
Saying: ['back out of parens']
Heard back out of parens
103:             0<1<2
104:             0>1>2
105:             0=1=2
106:            <CURSOR> (1)

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
104:             0>1>2
105:             0=1=2
106:             (1)
107:             <CURSOR>

*** End of source buffer ***
Saying: ['between brackets', '1']
Heard between brackets 1
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [1<CURSOR>]

*** End of source buffer ***
Saying: ['before previous bracket']
Heard before previous bracket
104:             0>1>2
105:             0=1=2
106:             (1)
107:            <CURSOR> [1]

*** End of source buffer ***
Saying: ['after bracket']
Heard after bracket
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [<CURSOR>1]

*** End of source buffer ***
Saying: ['before bracket']
Heard before bracket
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [1<CURSOR>]

*** End of source buffer ***
Saying: ['previous bracket']
Heard previous bracket
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [<CURSOR>1]

*** End of source buffer ***
Saying: ['out of brackets']
Heard out of brackets
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [1]<CURSOR>

*** End of source buffer ***
Saying: ['before previous bracket']
Heard before previous bracket
104:             0>1>2
105:             0=1=2
106:             (1)
107:             [1<CURSOR>]

*** End of source buffer ***
Saying: ['back out of brackets']
Heard back out of brackets
104:             0>1>2
105:             0=1=2
106:             (1)
107:            <CURSOR> [1]

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
105:             0=1=2
106:             (1)
107:             [1]
108:             <CURSOR>

*** End of source buffer ***
Saying: ['between braces', '1']
Heard between braces 1
105:             0=1=2
106:             (1)
107:             [1]
108:             {1<CURSOR>}

*** End of source buffer ***
Saying: ['before previous brace']
Heard before previous brace
105:             0=1=2
106:             (1)
107:             [1]
108:            <CURSOR> {1}

*** End of source buffer ***
Saying: ['after brace']
Heard after brace
105:             0=1=2
106:             (1)
107:             [1]
108:             {<CURSOR>1}

*** End of source buffer ***
Saying: ['before brace']
Heard before brace
105:             0=1=2
106:             (1)
107:             [1]
108:             {1<CURSOR>}

*** End of source buffer ***
Saying: ['previous brace']
Heard previous brace
105:             0=1=2
106:             (1)
107:             [1]
108:             {<CURSOR>1}

*** End of source buffer ***
Saying: ['out of braces']
Heard out of braces
105:             0=1=2
106:             (1)
107:             [1]
108:             {1}<CURSOR>

*** End of source buffer ***
Saying: ['before previous brace']
Heard before previous brace
105:             0=1=2
106:             (1)
107:             [1]
108:             {1<CURSOR>}

*** End of source buffer ***
Saying: ['back out of braces']
Heard back out of braces
105:             0=1=2
106:             (1)
107:             [1]
108:            <CURSOR> {1}

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
106:             (1)
107:             [1]
108:             {1}
109:             <CURSOR>

*** End of source buffer ***
Saying: ['between angled', '1']
Heard between angled 1
106:             (1)
107:             [1]
108:             {1}
109:             <1<CURSOR>>

*** End of source buffer ***
Saying: ['before previous angled']
Heard before previous angled
106:             (1)
107:             [1]
108:             {1}
109:            <CURSOR> <1>

*** End of source buffer ***
Saying: ['after angled']
Heard after angled
106:             (1)
107:             [1]
108:             {1}
109:             <<CURSOR>1>

*** End of source buffer ***
Saying: ['before angled']
Heard before angled
106:             (1)
107:             [1]
108:             {1}
109:             <1<CURSOR>>

*** End of source buffer ***
Saying: ['previous angled']
Heard previous angled
106:             (1)
107:             [1]
108:             {1}
109:             <1<CURSOR>>

*** End of source buffer ***
Saying: ['out of angled']
Heard out of angled
106:             (1)
107:             [1]
108:             {1}
109:             <1><CURSOR>

*** End of source buffer ***
Saying: ['before previous angled']
Heard before previous angled
106:             (1)
107:             [1]
108:             {1}
109:             <1<CURSOR>>

*** End of source buffer ***
Saying: ['back out of angled']
Heard back out of angled
106:             (1)
107:             [1]
108:             {1}
109:            <CURSOR> <1>

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
107:             [1]
108:             {1}
109:             <1>
110:             <CURSOR>

*** End of source buffer ***
Saying: ['between single quotes', '1']
Heard between single quotes 1
107:             [1]
108:             {1}
109:             <1>
110:             '1<CURSOR>'

*** End of source buffer ***
Saying: ['before previous single quote']
Heard before previous single quote
107:             [1]
108:             {1}
109:             <1>
110:            <CURSOR> '1'

*** End of source buffer ***
Saying: ['after single quote']
Heard after single quote
107:             [1]
108:             {1}
109:             <1>
110:             '<CURSOR>1'

*** End of source buffer ***
Saying: ['before single quote']
Heard before single quote
107:             [1]
108:             {1}
109:             <1>
110:             '1<CURSOR>'

*** End of source buffer ***
Saying: ['previous single quote']
Heard previous single quote
107:             [1]
108:             {1}
109:             <1>
110:             '1<CURSOR>'

*** End of source buffer ***
Saying: ['out of single quotes']
Heard out of single quotes
107:             [1]
108:             {1}
109:             <1>
110:             '1'<CURSOR>

*** End of source buffer ***
Saying: ['before previous single quote']
Heard before previous single quote
107:             [1]
108:             {1}
109:             <1>
110:             '1<CURSOR>'

*** End of source buffer ***
Saying: ['back out of single quotes']
Heard back out of single quotes
107:             [1]
108:             {1}
109:             <1>
110:            <CURSOR> '1'

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
108:             {1}
109:             <1>
110:             '1'
111:             <CURSOR>

*** End of source buffer ***
Saying: ['between quotes', '1']
Heard between quotes 1
108:             {1}
109:             <1>
110:             '1'
111:             "1<CURSOR>"

*** End of source buffer ***
Saying: ['before previous quote']
Heard before previous quote
108:             {1}
109:             <1>
110:             '1'
111:            <CURSOR> "1"

*** End of source buffer ***
Saying: ['after quote']
Heard after quote
108:             {1}
109:             <1>
110:             '1'
111:             "<CURSOR>1"

*** End of source buffer ***
Saying: ['before quote']
Heard before quote
108:             {1}
109:             <1>
110:             '1'
111:             "1<CURSOR>"

*** End of source buffer ***
Saying: ['previous quote']
Heard previous quote
108:             {1}
109:             <1>
110:             '1'
111:             "1<CURSOR>"

*** End of source buffer ***
Saying: ['out of quotes']
Heard out of quotes
108:             {1}
109:             <1>
110:             '1'
111:             "1"<CURSOR>

*** End of source buffer ***
Saying: ['before previous quote']
Heard before previous quote
108:             {1}
109:             <1>
110:             '1'
111:             "1<CURSOR>"

*** End of source buffer ***
Saying: ['back out of quotes']
Heard back out of quotes
108:             {1}
109:             <1>
110:             '1'
111:             "1<CURSOR>"

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
109:             <1>
110:             '1'
111:             "1"
112:             <CURSOR>

*** End of source buffer ***
Saying: ['between back quotes', '1']
Heard between back quotes 1
109:             <1>
110:             '1'
111:             "1"
112:             `1<CURSOR>`

*** End of source buffer ***
Saying: ['before previous back quote']
Heard before previous back quote
109:             <1>
110:             '1'
111:             "1"
112:            <CURSOR> `1`

*** End of source buffer ***
Saying: ['after back quote']
Heard after back quote
109:             <1>
110:             '1'
111:             "1"
112:             `<CURSOR>1`

*** End of source buffer ***
Saying: ['before back quote']
Heard before back quote
109:             <1>
110:             '1'
111:             "1"
112:             `1<CURSOR>`

*** End of source buffer ***
Saying: ['previous back quote']
Heard previous back quote
109:             <1>
110:             '1'
111:             "1"
112:             `1<CURSOR>`

*** End of source buffer ***
Saying: ['out of back quotes']
Heard out of back quotes
109:             <1>
110:             '1'
111:             "1"
112:             `1`<CURSOR>

*** End of source buffer ***
Saying: ['before previous back quote']
Heard before previous back quote
109:             <1>
110:             '1'
111:             "1"
112:             `1<CURSOR>`

*** End of source buffer ***
Saying: ['back out of back quotes']
Heard back out of back quotes
109:             <1>
110:             '1'
111:             "1"
112:            <CURSOR> `1`

*** End of source buffer ***
Saying: ['new statement']
Heard new statement
110:             '1'
111:             "1"
112:             `1`
113:             <CURSOR>

*** End of source buffer ***


*******************************************************************************
* Name        : python
* Description : testing the various CSCs and LSAs for dictating Python from scratch
*******************************************************************************

>>> Dictating Python when all symbols are known <<<

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Data\TestData\native_python.py'
>>> Known symbols are: 
AppState: ['app state']
CSC_consumes: ['csc consumes']
CSCmd: ['cs cmd', 'cs command']
CSCs: ['cs cs']
CmdInterp: ['cmd interp', 'cmd interpreter', 'command interp', 'command interpreter']
ContC: ['cont c', 'control c']
ContPy: ['cont py', 'cont python', 'cont p y', 'control py', 'control python', 'control p y']
EdSim: ['ed sim']
LSA_consumes: ['lsa consumes']
None: ['none']
Object: ['object']
SymDict: ['sym dict', 'sym dictionary', 'symbol dict', 'symbol dictionary']
__init__: ['init', 'initial', 'initialize', 'intial']
_untranslated_text_end: ['untranslated text end']
_untranslated_text_start: ['untranslated text start']
aCSC: ['a csc']
a_match: ['a match']
a_spoken_form: ['a spoken form']
a_word: ['a word']
accept_symbol_match: ['accept symbol match']
acmd: ['acmd']
actions_C_Cpp: ['actions c cpp', 'actions c c plus plus']
actions_py: ['actions py', 'actions python', 'actions p y']
active_language: ['active language']
active_language_LSAs: ['active language ls as']
addWord: ['add word']
add_voc_entry: ['add voc entry']
all_language_LSAs: ['all language ls as']
and: ['and']
answer: ['answer']
answer_match: ['answer match']
attrs: ['attributes']
auto_test: ['auto test']
aword: ['aword']
break: ['break']
choice_index: ['choice index']
choices: ['choices']
choose_best_symbol: ['choose best symbol']
chop_CSC: ['chop csc']
chop_LSA: ['chop lsa']
chop_symbol: ['chop symbol']
chop_word: ['chop word']
chopped_CSC: ['chopped csc']
chopped_LSA: ['chopped lsa']
chopped_symbol: ['chopped symbol']
chopped_word: ['chopped word']
chosen_match: ['chosen match']
class: ['class']
clean_for: ['clean for']
clean_written: ['clean written']
clean_written_form: ['clean written form']
cmd: ['cmd', 'command']
cmd_index: ['cmd index', 'command index']
cmd_without_CSC: ['cmd without csc', 'command without csc']
cmd_without_LSA: ['cmd without lsa', 'command without lsa']
cmd_without_symbol: ['cmd without symbol', 'command without symbol']
cmd_without_word: ['cmd without word', 'command without word']
cmds_this_spoken_form: ['commands this spoken form']
command: ['command']
consumed: ['consumed']
cont_gen: ['cont gen', 'cont general', 'cont generic', 'control gen', 'control general', 'control generic']
content: ['content']
csc_applied: ['csc applied']
cur_pos: ['cur pos', 'cur position', 'cur positioning', 'cursor pos', 'cursor position', 'cursor positioning', 'current pos', 'current position', 'current positioning']
curr_buffer: ['curr buffer', 'current buffer']
decl_attrs: ['decl attributes', 'declaration attributes', 'declare attributes']
deep_construct: ['deep construct']
def: ['def', 'definition', 'default', 'define', 'defined', 'deaf']
deleteWord: ['delete word']
dlg_select_symbol_match: ['dlg select symbol match']
dummy: ['dummy']
else: ['else']
end: ['end']
environ: ['environ', 'environment']
first: ['first']
for: ['for']
from: ['from']
global: ['global']
good_answer: ['good answer']
group: ['group']
has_key: ['has key']
head_was_translated: ['head was translated']
if: ['if']
ii: ['ii']
import: ['import']
in: ['in']
index_csc: ['index csc']
insert_indent: ['insert indent']
insert_untranslated_text: ['insert untranslated text']
int: ['int', 'integer']
interpret: ['interpret']
interpret_NL_cmd: ['interpret nl cmd', 'interpret nl command']
is_new: ['is new']
join: ['join']
known_symbols: ['known symbols']
language: ['language']
language_specific_aliases: ['language specific aliases']
last_language: ['last language']
last_loaded_language: ['last loaded language']
leading_spaces: ['leading spaces']
leading_word: ['leading word']
len: ['len', 'length']
load_language_specific_aliases: ['load language specific aliases']
lower: ['lower']
massage_command: ['massage command']
match: ['match']
match_pseudo_symbol: ['match pseudo symbol']
match_untranslated_text: ['match untranslated text']
max: ['max']
mod_command: ['mod command', 'mode command', 'modify command']
most_consumed: ['most consumed']
move_to: ['move to']
native_symbol: ['native symbol']
natlink: ['natlink']
new_pos: ['new pos', 'new position', 'new positioning']
not: ['not']
num_match: ['num match', 'number match']
old_pos: ['old pos', 'old position', 'old positioning']
on_app: ['on app']
or: ['or']
os: ['os', 'operating system', 'o s']
print: ['print']
print_buff_content: ['print buff content', 'print buffer content']
re: ['re']
readline: ['readline']
reg: ['reg', 'regular', 'regular expression']
regexp: ['regexp', 'regular expression']
regexp_is_dirty: ['regexp is dirty', 'regular expression is dirty']
regexp_this_word: ['regexp this word', 'regular expression this word']
rest: ['rest']
return: ['return']
s: ['s']
self: ['self']
split: ['split']
spoken: ['spoken']
spoken_as: ['spoken as']
spoken_form: ['spoken form']
spoken_form_info: ['spoken form info', 'spoken form information']
spoken_form_regexp: ['spoken form regexp', 'spoken form regular expression']
spoken_forms: ['spoken forms']
spoken_written_form: ['spoken written form']
sr_interface: ['sr interface']
start: ['start']
stdin: ['stdin', 's t d in', 'standard input']
stdout: ['stdout']
string: ['string']
sub: ['sub', 'sub routine']
symbol_consumes: ['symbol consumes']
symbol_info: ['symbol info', 'symbol information']
symbol_matches: ['symbol matches']
symbols: ['symbols']
symdict_pickle_file: ['symdict pickle file']
sys: ['sys', 'system']
text: ['text']
text_no_spaces: ['text no spaces', 'text number spaces']
untranslated_text: ['untranslated text']
upper: ['upper']
upto: ['upto']
vc_globals: ['vc globals']
vocabulary_entry: ['vocabulary entry']
while: ['while']
word_consumes: ['word consumes']
words: ['words']
write: ['write']
written: ['written']
written_as: ['written as']
_cached_symbols_as_one_string is:
    import  os  re  string  sys  auto_test  natlink  vc_globals  from  actions_C_Cpp  actions_py  AppState  cont_gen  ContC  ContPy  CSCmd  EdSim  Object  SymDict  sr_interface  class  CmdInterp  def  __init__  self  on_app  None  symdict_pickle_file  attrs  decl_attrs  deep_construct  spoken_form_regexp  spoken_form  words  split  regexp  for  aword  in  first  rest  regexp_this_word  lower  upper  if  not  return  interpret_NL_cmd  cmd  print  _untranslated_text_start  _untranslated_text_end  massage_command  while  len  curr_buffer  cur_pos  print_buff_content  chopped_CSC  CSC_consumes  cmd_without_CSC  chop_CSC  chopped_LSA  LSA_consumes  cmd_without_LSA  chop_LSA  chopped_symbol  symbol_consumes  cmd_without_symbol  chop_symbol  chopped_word  word_consumes  cmd_without_word  chop_word  most_consumed  max  head_was_translated  s  CSCs  cmd_index  csc_applied  aCSC  interpret  break  else  and  insert_indent  insert_untranslated_text  or  match_untranslated_text  untranslated_text  content  command  mod_command  a_word  spoken  written  spoken_written_form  clean_written_form  clean_for  sub  vocabulary_entry  clean_written  text  a_match  match  text_no_spaces  group  leading_spaces  reg  num_match  known_symbols  symbol_info  has_key  symbol_matches  match_pseudo_symbol  dlg_select_symbol_match  good_answer  ii  stdout  write  native_symbol  is_new  answer  stdin  readline  answer_match  choice_index  int  chosen_match  accept_symbol_match  old_pos  start  end  new_pos  move_to  consumed  dummy  upto  a_spoken_form  join  leading_word  active_language_LSAs  language_specific_aliases  active_language  all_language_LSAs  spoken_form_info  choose_best_symbol  symbols  choices  index_csc  acmd  add_voc_entry  global  regexp_is_dirty  spoken_forms  cmds_this_spoken_form  environ  addWord  load_language_specific_aliases  language  last_language  last_loaded_language  deleteWord  spoken_as  written_as 
AppState: ['app state']
CSC_consumes: ['csc consumes']
CSCmd: ['cs cmd', 'cs command']
CSCs: ['cs cs']
CmdInterp: ['cmd interp', 'cmd interpreter', 'command interp', 'command interpreter']
ContC: ['cont c', 'control c']
ContPy: ['cont py', 'cont python', 'cont p y', 'control py', 'control python', 'control p y']
EdSim: ['ed sim']
LSA_consumes: ['lsa consumes']
None: ['none']
Object: ['object']
SymDict: ['sym dict', 'sym dictionary', 'symbol dict', 'symbol dictionary']
__init__: ['init', 'initial', 'initialize', 'intial']
_untranslated_text_end: ['untranslated text end']
_untranslated_text_start: ['untranslated text start']
aCSC: ['a csc']
a_match: ['a match']
a_spoken_form: ['a spoken form']
a_word: ['a word']
accept_symbol_match: ['accept symbol match']
acmd: ['acmd']
actions_C_Cpp: ['actions c cpp', 'actions c c plus plus']
actions_py: ['actions py', 'actions python', 'actions p y']
active_language: ['active language']
active_language_LSAs: ['active language ls as']
addWord: ['add word']
add_voc_entry: ['add voc entry']
all_language_LSAs: ['all language ls as']
and: ['and']
answer: ['answer']
answer_match: ['answer match']
attrs: ['attributes']
auto_test: ['auto test']
aword: ['aword']
break: ['break']
choice_index: ['choice index']
choices: ['choices']
choose_best_symbol: ['choose best symbol']
chop_CSC: ['chop csc']
chop_LSA: ['chop lsa']
chop_symbol: ['chop symbol']
chop_word: ['chop word']
chopped_CSC: ['chopped csc']
chopped_LSA: ['chopped lsa']
chopped_symbol: ['chopped symbol']
chopped_word: ['chopped word']
chosen_match: ['chosen match']
class: ['class']
clean_for: ['clean for']
clean_written: ['clean written']
clean_written_form: ['clean written form']
cmd: ['cmd', 'command']
cmd_index: ['cmd index', 'command index']
cmd_without_CSC: ['cmd without csc', 'command without csc']
cmd_without_LSA: ['cmd without lsa', 'command without lsa']
cmd_without_symbol: ['cmd without symbol', 'command without symbol']
cmd_without_word: ['cmd without word', 'command without word']
cmds_this_spoken_form: ['commands this spoken form']
command: ['command']
consumed: ['consumed']
cont_gen: ['cont gen', 'cont general', 'cont generic', 'control gen', 'control general', 'control generic']
content: ['content']
csc_applied: ['csc applied']
cur_pos: ['cur pos', 'cur position', 'cur positioning', 'cursor pos', 'cursor position', 'cursor positioning', 'current pos', 'current position', 'current positioning']
curr_buffer: ['curr buffer', 'current buffer']
decl_attrs: ['decl attributes', 'declaration attributes', 'declare attributes']
deep_construct: ['deep construct']
def: ['def', 'definition', 'default', 'define', 'defined', 'deaf']
deleteWord: ['delete word']
dlg_select_symbol_match: ['dlg select symbol match']
dummy: ['dummy']
else: ['else']
end: ['end']
environ: ['environ', 'environment']
first: ['first']
for: ['for']
from: ['from']
global: ['global']
good_answer: ['good answer']
group: ['group']
has_key: ['has key']
head_was_translated: ['head was translated']
if: ['if']
ii: ['ii']
import: ['import']
in: ['in']
index_csc: ['index csc']
insert_indent: ['insert indent']
insert_untranslated_text: ['insert untranslated text']
int: ['int', 'integer']
interpret: ['interpret']
interpret_NL_cmd: ['interpret nl cmd', 'interpret nl command']
is_new: ['is new']
join: ['join']
known_symbols: ['known symbols']
language: ['language']
language_specific_aliases: ['language specific aliases']
last_language: ['last language']
last_loaded_language: ['last loaded language']
leading_spaces: ['leading spaces']
leading_word: ['leading word']
len: ['len', 'length']
load_language_specific_aliases: ['load language specific aliases']
lower: ['lower']
massage_command: ['massage command']
match: ['match']
match_pseudo_symbol: ['match pseudo symbol']
match_untranslated_text: ['match untranslated text']
max: ['max']
mod_command: ['mod command', 'mode command', 'modify command']
most_consumed: ['most consumed']
move_to: ['move to']
native_symbol: ['native symbol']
natlink: ['natlink']
new_pos: ['new pos', 'new position', 'new positioning']
not: ['not']
num_match: ['num match', 'number match']
old_pos: ['old pos', 'old position', 'old positioning']
on_app: ['on app']
or: ['or']
os: ['os', 'operating system', 'o s']
print: ['print']
print_buff_content: ['print buff content', 'print buffer content']
re: ['re']
readline: ['readline']
reg: ['reg', 'regular', 'regular expression']
regexp: ['regexp', 'regular expression']
regexp_is_dirty: ['regexp is dirty', 'regular expression is dirty']
regexp_this_word: ['regexp this word', 'regular expression this word']
rest: ['rest']
return: ['return']
s: ['s']
self: ['self']
split: ['split']
spoken: ['spoken']
spoken_as: ['spoken as']
spoken_form: ['spoken form']
spoken_form_info: ['spoken form info', 'spoken form information']
spoken_form_regexp: ['spoken form regexp', 'spoken form regular expression']
spoken_forms: ['spoken forms']
spoken_written_form: ['spoken written form']
sr_interface: ['sr interface']
start: ['start']
stdin: ['stdin', 's t d in', 'standard input']
stdout: ['stdout']
string: ['string']
sub: ['sub', 'sub routine']
symbol_consumes: ['symbol consumes']
symbol_info: ['symbol info', 'symbol information']
symbol_matches: ['symbol matches']
symbols: ['symbols']
symdict_pickle_file: ['symdict pickle file']
sys: ['sys', 'system']
text: ['text']
text_no_spaces: ['text no spaces', 'text number spaces']
untranslated_text: ['untranslated text']
upper: ['upper']
upto: ['upto']
vc_globals: ['vc globals']
vocabulary_entry: ['vocabulary entry']
while: ['while']
word_consumes: ['word consumes']
words: ['words']
write: ['write']
written: ['written']
written_as: ['written as']
_cached_symbols_as_one_string is:
    import  os  re  string  sys  auto_test  natlink  vc_globals  from  actions_C_Cpp  actions_py  AppState  cont_gen  ContC  ContPy  CSCmd  EdSim  Object  SymDict  sr_interface  class  CmdInterp  def  __init__  self  on_app  None  symdict_pickle_file  attrs  decl_attrs  deep_construct  spoken_form_regexp  spoken_form  words  split  regexp  for  aword  in  first  rest  regexp_this_word  lower  upper  if  not  return  interpret_NL_cmd  cmd  print  _untranslated_text_start  _untranslated_text_end  massage_command  while  len  curr_buffer  cur_pos  print_buff_content  chopped_CSC  CSC_consumes  cmd_without_CSC  chop_CSC  chopped_LSA  LSA_consumes  cmd_without_LSA  chop_LSA  chopped_symbol  symbol_consumes  cmd_without_symbol  chop_symbol  chopped_word  word_consumes  cmd_without_word  chop_word  most_consumed  max  head_was_translated  s  CSCs  cmd_index  csc_applied  aCSC  interpret  break  else  and  insert_indent  insert_untranslated_text  or  match_untranslated_text  untranslated_text  content  command  mod_command  a_word  spoken  written  spoken_written_form  clean_written_form  clean_for  sub  vocabulary_entry  clean_written  text  a_match  match  text_no_spaces  group  leading_spaces  reg  num_match  known_symbols  symbol_info  has_key  symbol_matches  match_pseudo_symbol  dlg_select_symbol_match  good_answer  ii  stdout  write  native_symbol  is_new  answer  stdin  readline  answer_match  choice_index  int  chosen_match  accept_symbol_match  old_pos  start  end  new_pos  move_to  consumed  dummy  upto  a_spoken_form  join  leading_word  active_language_LSAs  language_specific_aliases  active_language  all_language_LSAs  spoken_form_info  choose_best_symbol  symbols  choices  index_csc  acmd  add_voc_entry  global  regexp_is_dirty  spoken_forms  cmds_this_spoken_form  environ  addWord  load_language_specific_aliases  language  last_language  last_loaded_language  deleteWord  spoken_as  written_as 
WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'O.', 'S.', ', \\comma', 'R.', 'E.', ', \\comma', 'string', ', \\comma', 'system', 'new', 'statement']
Heard import modules O. S. comma R. E. comma string comma system new statement
Associate 'R. E.' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': Re (*new*)
  '3': RE (*new*)

> *** Start of source buffer ***
  1: import os, re, string, sys
  2: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'auto', 'test', ', \\comma', 'natural', 'link', ', \\comma', 'V.', 'C.', 'globals', 'new', 'statement']
Heard import modules auto test comma natural link comma V. C. globals new statement
Associate 'natural link' with symbol (Enter selection):

  '0': no association
  '1': natlink
  '2': natural_link (*new*)
  '3': NaturalLink (*new*)
  '4': naturalLink (*new*)
  '5': NATURAL_LINK (*new*)
  '6': naturallink (*new*)
  '7': NATURALLINK (*new*)

> Associate 'V. C. globals' with symbol (Enter selection):

  '0': no association
  '1': vc_globals
  '2': VcGlobals (*new*)
  '3': vcGlobals (*new*)
  '4': VC_GLOBALS (*new*)
  '5': vcglobals (*new*)
  '6': VCGLOBALS (*new*)

> *** Start of source buffer ***
  1: import os, re, string, sys
  2: import auto_test, natlink, vc_globals
  3: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'actions', 'C.', 'C.', 'P.', 'P.', ' import all\\import all', 'new', 'statement']
Heard from module actions C. C. P. P. import all new statement
Associate 'actions C. C. P. P.' with symbol (Enter selection):

  '0': no association
  '1': actions_C_Cpp
  '2': actions_ccpp (*new*)
  '3': ActionsCcpp (*new*)
  '4': actionsCcpp (*new*)
  '5': ACTIONS_CCPP (*new*)
  '6': actionsccpp (*new*)
  '7': ACTIONSCCPP (*new*)

> *** Start of source buffer ***
  1: import os, re, string, sys
  2: import auto_test, natlink, vc_globals
  3: from actions_C_Cpp import all
  4: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'application', 'state', 'import', 'symbols', 'application', 'state', 'new', 'statement']
Heard from module application state import symbols application state new statement
Associate 'application state' with symbol (Enter selection):

  '0': no association
  '1': AppState
  '2': application_state (*new*)
  '3': ApplicationState (*new*)
  '4': applicationState (*new*)
  '5': APPLICATION_STATE (*new*)
  '6': applicationstate (*new*)
  '7': APPLICATIONSTATE (*new*)

> Associate 'application state' with symbol (Enter selection):

  '0': no association
  '1': AppState
  '2': application_state (*new*)
  '3': ApplicationState (*new*)
  '4': applicationState (*new*)
  '5': APPLICATION_STATE (*new*)
  '6': applicationstate (*new*)
  '7': APPLICATIONSTATE (*new*)

>   2: import auto_test, natlink, vc_globals
  3: from actions_C_Cpp import all
  4: from AppState import AppState
  5: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'context', 'generic', 'import', 'symbols', 'context', 'C.', 'comma', 'context', 'python', 'new', 'statement']
Heard from module context generic import symbols context C. comma context python new statement
Associate 'context generic' with symbol (Enter selection):

  '0': no association
  '1': cont_gen
  '2': context_generic (*new*)
  '3': ContextGeneric (*new*)
  '4': contextGeneric (*new*)
  '5': CONTEXT_GENERIC (*new*)
  '6': contextgeneric (*new*)
  '7': CONTEXTGENERIC (*new*)

> Associate 'context C.' with symbol (Enter selection):

  '0': no association
  '1': ContC
  '2': context_c (*new*)
  '3': ContextC (*new*)
  '4': contextC (*new*)
  '5': CONTEXT_C (*new*)
  '6': contextc (*new*)
  '7': CONTEXTC (*new*)

> WARNING: abbreviation 'c' not added (length < 2)
Associate 'context python' with symbol (Enter selection):

  '0': no association
  '1': ContPy
  '2': context_python (*new*)
  '3': ContextPython (*new*)
  '4': contextPython (*new*)
  '5': CONTEXT_PYTHON (*new*)
  '6': contextpython (*new*)
  '7': CONTEXTPYTHON (*new*)

>   3: from actions_C_Cpp import all
  4: from AppState import AppState
  5: from cont_gen import ContC, ContPy
  6: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'context', 'sensitive', 'command', 'import', 'symbols', 'context', 'sensitive', 'command', 'new', 'statement']
Heard from module context sensitive command import symbols context sensitive command new statement
Associate 'context sensitive cmd' with symbol (Enter selection):

  '0': no association
  '1': CSCmd
  '2': context_sensitive_cmd (*new*)
  '3': ContextSensitiveCmd (*new*)
  '4': contextSensitiveCmd (*new*)
  '5': CONTEXT_SENSITIVE_CMD (*new*)
  '6': contextsensitivecmd (*new*)
  '7': CONTEXTSENSITIVECMD (*new*)

> Associate 'context sensitive cmd' with symbol (Enter selection):

  '0': no association
  '1': CSCmd
  '2': context_sensitive_cmd (*new*)
  '3': ContextSensitiveCmd (*new*)
  '4': contextSensitiveCmd (*new*)
  '5': CONTEXT_SENSITIVE_CMD (*new*)
  '6': contextsensitivecmd (*new*)
  '7': CONTEXTSENSITIVECMD (*new*)

>   4: from AppState import AppState
  5: from cont_gen import ContC, ContPy
  6: from CSCmd import CSCmd
  7: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'Ed', 'simulator', 'import', 'symbol', 'Ed', 'simulator', 'new', 'statement']
Heard from module Ed simulator import symbol Ed simulator new statement
Associate 'Ed simulator' with symbol (Enter selection):

  '0': no association
  '1': EdSim
  '2': ed_simulator (*new*)
  '3': EdSimulator (*new*)
  '4': edSimulator (*new*)
  '5': ED_SIMULATOR (*new*)
  '6': edsimulator (*new*)
  '7': EDSIMULATOR (*new*)

> Associate 'Ed simulator' with symbol (Enter selection):

  '0': no association
  '1': EdSim
  '2': ed_simulator (*new*)
  '3': EdSimulator (*new*)
  '4': edSimulator (*new*)
  '5': ED_SIMULATOR (*new*)
  '6': edsimulator (*new*)
  '7': EDSIMULATOR (*new*)

>   5: from cont_gen import ContC, ContPy
  6: from CSCmd import CSCmd
  7: from EdSim import EdSim
  8: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'object', 'import', 'symbol', 'object', 'new', 'statement']
Heard from module object import symbol object new statement
  6: from CSCmd import CSCmd
  7: from EdSim import EdSim
  8: from Object import Object
  9: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'Ed', 'simulator', 'comma', 'symbol', 'dictionary', 'new', 'statement']
Heard import modules Ed simulator comma symbol dictionary new statement
Associate 'Ed simulator' with symbol (Enter selection):

  '0': no association
  '1': EdSim
  '2': ed_simulator (*new*)
  '3': EdSimulator (*new*)
  '4': edSimulator (*new*)
  '5': ED_SIMULATOR (*new*)
  '6': edsimulator (*new*)
  '7': EDSIMULATOR (*new*)

>   7: from EdSim import EdSim
  8: from Object import Object
  9: import EdSim, SymDict
 10: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'module', 'S.', 'R.', 'interface', 'new', 'statement']
Heard import module S. R. interface new statement
Associate 'S. R. interface' with symbol (Enter selection):

  '0': no association
  '1': sr_interface
  '2': SrInterface (*new*)
  '3': srInterface (*new*)
  '4': SR_INTERFACE (*new*)
  '5': srinterface (*new*)
  '6': SRINTERFACE (*new*)

>   8: from Object import Object
  9: import EdSim, SymDict
 10: import sr_interface
 11: <CURSOR>

*** End of source buffer ***
Saying: ['define', 'class', 'command', 'interpreter', 'sub class\\sub class', 'of', 'object', 'class', 'body']
Heard define class command interpreter sub class of object class body
  9: import EdSim, SymDict
 10: import sr_interface
 11: class CmdInterp(Object):
 12:    <CURSOR>

*** End of source buffer ***
Saying: ['define', 'method', 'initialize', 'add', 'argument', 'on', 'application', 'equals', 'none', 'comma']
Heard define method initialize add argument on application equals none comma
Associate 'on application' with symbol (Enter selection):

  '0': no association
  '1': on_app
  '2': on_application (*new*)
  '3': OnApplication (*new*)
  '4': onApplication (*new*)
  '5': ON_APPLICATION (*new*)
  '6': onapplication (*new*)
  '7': ONAPPLICATION (*new*)

>   9: import EdSim, SymDict
 10: import sr_interface
 11: class CmdInterp(Object):
 12:    def __init__(self, on_app = None, <CURSOR>):
 13:       

*** End of source buffer ***
Saying: ['symbol', 'dictionary', 'pickle', 'file', 'equals', 'none', 'comma', 'double', 'asterisk', 'attributes', 'method', 'body']
Heard symbol dictionary pickle file equals none comma double asterisk attributes method body
Associate 'SymDict pickle file' with symbol (Enter selection):

  '0': no association
  '1': symdict_pickle_file
  '2': SymdictPickleFile (*new*)
  '3': symdictPickleFile (*new*)
  '4': SYMDICT_PICKLE_FILE (*new*)
  '5': symdictpicklefile (*new*)
  '6': SYMDICTPICKLEFILE (*new*)

>  10: import sr_interface
 11: class CmdInterp(Object):
 12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       <CURSOR>

*** End of source buffer ***
Saying: ['self', 'dot', 'declare', 'attributes', 'with', 'arguments', 'brace', 'pair']
Heard self dot declare attributes with arguments brace pair
 10: import sr_interface
 11: class CmdInterp(Object):
 12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       self.decl_attrs({<CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'un', 'translated', 'text', 'start', 'jump', 'out', ':\\colon', 'none', 'comma']
Heard single quotes un translated text start jump out colon none comma
Associate 'un translated text start' with symbol (Enter selection):

  '0': no association
  '1': _untranslated_text_start
  '2': un_translated_text_start (*new*)
  '3': UnTranslatedTextStart (*new*)
  '4': unTranslatedTextStart (*new*)
  '5': UN_TRANSLATED_TEXT_START (*new*)
  '6': untranslatedtextstart (*new*)
  '7': UNTRANSLATEDTEXTSTART (*new*)

>  10: import sr_interface
 11: class CmdInterp(Object):
 12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       self.decl_attrs({'_untranslated_text_start': None, <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'un', 'translated', 'text', 'end', 'jump', 'out', ':\\colon', 'none', 'new', 'statement']
Heard single quotes un translated text end jump out colon none new statement
Associate 'un translated text end' with symbol (Enter selection):

  '0': no association
  '1': _untranslated_text_end
  '2': un_translated_text_end (*new*)
  '3': UnTranslatedTextEnd (*new*)
  '4': unTranslatedTextEnd (*new*)
  '5': UN_TRANSLATED_TEXT_END (*new*)
  '6': untranslatedtextend (*new*)
  '7': UNTRANSLATEDTEXTEND (*new*)

>  11: class CmdInterp(Object):
 12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       self.decl_attrs({'_untranslated_text_start': None, '_untranslated_text_end': None})
 14:       <CURSOR>

*** End of source buffer ***
Saying: ['self', 'dot', 'deep', 'construct', 'with', 'arguments', 'command', 'interpreter', 'comma', 'continue', 'statement']
Heard self dot deep construct with arguments command interpreter comma continue statement
 12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       self.decl_attrs({'_untranslated_text_start': None, '_untranslated_text_end': None})
 14:       self.deep_construct(CmdInterp, \
 15:                           <CURSOR>)

*** End of source buffer ***
Saying: ['brace', 'pair', 'single', 'quotes', 'on', 'application', 'jump', 'out', ':\\colon', 'on', 'application', 'comma']
Heard brace pair single quotes on application jump out colon on application comma
Associate 'on application' with symbol (Enter selection):

  '0': no association
  '1': on_app
  '2': on_application (*new*)
  '3': OnApplication (*new*)
  '4': onApplication (*new*)
  '5': ON_APPLICATION (*new*)
  '6': onapplication (*new*)
  '7': ONAPPLICATION (*new*)

> Associate 'on application' with symbol (Enter selection):

  '0': no association
  '1': on_app
  '2': on_application (*new*)
  '3': OnApplication (*new*)
  '4': onApplication (*new*)
  '5': ON_APPLICATION (*new*)
  '6': onapplication (*new*)
  '7': ONAPPLICATION (*new*)

>  12:    def __init__(self, on_app = None, symdict_pickle_file = None, **attrs):
 13:       self.decl_attrs({'_untranslated_text_start': None, '_untranslated_text_end': None})
 14:       self.deep_construct(CmdInterp, \
 15:                           {'on_app': on_app, <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'known', 'symbols', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'dot', 'symbol', 'dictionary', 'without', 'arguments', 'comma', 'continue', 'statement']
Heard single quotes known symbols jump out colon symbol dictionary dot symbol dictionary without arguments comma continue statement
 13:       self.decl_attrs({'_untranslated_text_start': None, '_untranslated_text_end': None})
 14:       self.deep_construct(CmdInterp, \
 15:                           {'on_app': on_app, 'known_symbols': SymDict.SymDict(), \
 16:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'language', 'specific', 'aliases', 'jump', 'out', ':\\colon', 'empty', 'dictionary', 'comma', 'continue', 'statement']
Heard single quotes language specific aliases jump out colon empty dictionary comma continue statement
 14:       self.deep_construct(CmdInterp, \
 15:                           {'on_app': on_app, 'known_symbols': SymDict.SymDict(), \
 16:                            'language_specific_aliases': {}, \
 17:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'last', 'loaded', 'language', 'jump', 'out', ':\\colon', 'none', 'comma', 'continue', 'statement']
Heard single quotes last loaded language jump out colon none comma continue statement
 15:                           {'on_app': on_app, 'known_symbols': SymDict.SymDict(), \
 16:                            'language_specific_aliases': {}, \
 17:                            'last_loaded_language': None, \
 18:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', 'comma', 'continue', 'statement']
Heard single quotes symbol dictionary pickle file jump out colon symbol dictionary pickle file jump out comma continue statement
Associate 'SymDict pickle file' with symbol (Enter selection):

  '0': no association
  '1': symdict_pickle_file
  '2': SymdictPickleFile (*new*)
  '3': symdictPickleFile (*new*)
  '4': SYMDICT_PICKLE_FILE (*new*)
  '5': symdictpicklefile (*new*)
  '6': SYMDICTPICKLEFILE (*new*)

> Associate 'SymDict pickle file' with symbol (Enter selection):

  '0': no association
  '1': symdict_pickle_file
  '2': SymdictPickleFile (*new*)
  '3': symdictPickleFile (*new*)
  '4': SYMDICT_PICKLE_FILE (*new*)
  '5': symdictpicklefile (*new*)
  '6': SYMDICTPICKLEFILE (*new*)

>  16:                            'language_specific_aliases': {}, \
 17:                            'last_loaded_language': None, \
 18:                            'symdict_pickle_file': symdict_pickle_file}, \
 19:                           <CURSOR>)

*** End of source buffer ***
Saying: ['attributes', 'new', 'statement', 'new', 'statement']
Heard attributes new statement new statement
 18:                            'symdict_pickle_file': symdict_pickle_file}, \
 19:                           attrs)
 20: 
 21:       <CURSOR>

*** End of source buffer ***
Saying: ['back indent', 'define', 'method', 'spoken', 'form', 'regular', 'expression', 'add', 'argument', 'spoken', 'form']
Heard back indent define method spoken form regular expression add argument spoken form
 18:                            'symdict_pickle_file': symdict_pickle_file}, \
 19:                           attrs)
 20: 
 21:    def spoken_form_regexp(self, spoken_form<CURSOR>):
 22:       

*** End of source buffer ***
Saying: ['method', 'body']
Heard method body
 19:                           attrs)
 20: 
 21:    def spoken_form_regexp(self, spoken_form):
 22:       <CURSOR>

*** End of source buffer ***
Saying: ['words', 'equals', 'R.', 'E.', 'dot', 'split', 'with', 'arguments']
Heard words equals R. E. dot split with arguments
Associate 'R. E.' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': Re (*new*)
  '3': RE (*new*)

>  19:                           attrs)
 20: 
 21:    def spoken_form_regexp(self, spoken_form):
 22:       words = re.split(<CURSOR>)

*** End of source buffer ***
Saying: ['single', 'quotes', '\\s\\back slash s.', 'plus', 'sign', 'jump', 'out', 'comma', 'spoken', 'form', 'new', 'statement']
Heard single quotes back slash s plus sign jump out comma spoken form new statement
 20: 
 21:    def spoken_form_regexp(self, spoken_form):
 22:       words = re.split('\s+', spoken_form)
 23:       <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'empty', 'single', 'quotes', 'new', 'statement']
Heard regular expression equals empty single quotes new statement
 21:    def spoken_form_regexp(self, spoken_form):
 22:       words = re.split('\s+', spoken_form)
 23:       regexp = ''
 24:       <CURSOR>

*** End of source buffer ***
Saying: ['for', 'loop', 'a', 'word', 'in', 'list', 'words', 'loop', 'body']
Heard for loop a word in list words loop body
 22:       words = re.split('\s+', spoken_form)
 23:       regexp = ''
 24:       for a_word in words:
 25:          <CURSOR>

*** End of source buffer ***
Saying: ['first', 'equals', 'a', 'word', 'at', 'index', '0', 'new', 'statement']
Heard first equals a word at index 0 new statement
 23:       regexp = ''
 24:       for a_word in words:
 25:          first = a_word[0]
 26:          <CURSOR>

*** End of source buffer ***
Saying: ['rest', 'equals', 'a', 'word', 'at', 'index', '1', ':\\colon', 'new', 'statement']
Heard rest equals a word at index 1 colon new statement
 24:       for a_word in words:
 25:          first = a_word[0]
 26:          rest = a_word[1: ]
 27:          <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'this', 'word', 'equals', 'single', 'quotes']
Heard regular expression this word equals single quotes
 24:       for a_word in words:
 25:          first = a_word[0]
 26:          rest = a_word[1: ]
 27:          regexp_this_word = '<CURSOR>'

*** End of source buffer ***
Saying: ['open', 'bracket', 'jump', 'out', 'plus', 'string', 'dot', 'lower', 'with', 'arguments', 'first']
Heard open bracket jump out plus string dot lower with arguments first
 24:       for a_word in words:
 25:          first = a_word[0]
 26:          rest = a_word[1: ]
 27:          regexp_this_word = '[' + string.lower(first<CURSOR>)

*** End of source buffer ***
Saying: ['jump', 'out', 'plus', 'string', 'dot', 'upper', 'with', 'arguments', 'first', 'new', 'statement']
Heard jump out plus string dot upper with arguments first new statement
 25:          first = a_word[0]
 26:          rest = a_word[1: ]
 27:          regexp_this_word = '[' + string.lower(first) + string.upper(first)
 28:          <CURSOR>

*** End of source buffer ***
Saying: ['if', 'statement', 'not', 'regular', 'expression', 'equal', 'to', 'empty', 'single', 'quotes', 'if', 'body']
Heard if statement not regular expression equal to empty single quotes if body
 26:          rest = a_word[1: ]
 27:          regexp_this_word = '[' + string.lower(first) + string.upper(first)
 28:          if not regexp == '':
 29:             <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'single', 'quotes', '\\s\\back slash s.', 'asterisk', 'new', 'statement']
Heard regular expression equals regular expression plus single quotes back slash s asterisk new statement
 27:          regexp_this_word = '[' + string.lower(first) + string.upper(first)
 28:          if not regexp == '':
 29:             regexp = regexp + '\s*'
 30:             <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'regular', 'expression', 'this', 'word', 'new', 'statement']
Heard regular expression equals regular expression plus regular expression this word new statement
 28:          if not regexp == '':
 29:             regexp = regexp + '\s*'
 30:             regexp = regexp + regexp_this_word
 31:             <CURSOR>

*** End of source buffer ***
Saying: ['return', 'regular', 'expression']
Heard return regular expression
 28:          if not regexp == '':
 29:             regexp = regexp + '\s*'
 30:             regexp = regexp + regexp_this_word
 31:             return regexp<CURSOR>

*** End of source buffer ***
Saying: ['back indent', 'new statement']
Heard back indent new statement
 29:             regexp = regexp + '\s*'
 30:             regexp = regexp + regexp_this_word
 31:          return regexp
 32:       <CURSOR>

*** End of source buffer ***
Saying: ['if', 'not', 'this', 'word', 'then', 'this', 'word', 'equals', 'single', 'quotes', 'hello']
Heard if not this word then this word equals single quotes hello
Associate 'this word' with symbol (Enter selection):

  '0': no association
  '1': this_word (*new*)
  '2': ThisWord (*new*)
  '3': thisWord (*new*)
  '4': THIS_WORD (*new*)
  '5': thisword (*new*)
  '6': THISWORD (*new*)

> Associate 'hello' with symbol (Enter selection):

  '0': no association
  '1': hello (*new*)
  '2': Hello (*new*)
  '3': HELLO (*new*)

>  30:             regexp = regexp + regexp_this_word
 31:          return regexp
 32:       if not this_word:
 33:          this_word = 'hello<CURSOR>'

*** End of source buffer ***
Saying: ['else', 'if', 'this', 'word', 'is', 'equal', 'to', 'hi', 'then']
Heard else if this word is equal to hi then
Associate 'hi' with symbol (Enter selection):

  '0': no association
  '1': hi (*new*)
  '2': Hi (*new*)
  '3': HI (*new*)

>  32:       if not this_word:
 33:          this_word = 'hello'
 34:       elif this_word == hi:
 35:          <CURSOR>

*** End of source buffer ***
Saying: ['this', 'word', 'equals', 'greetings', 'else']
Heard this word equals greetings else
Associate 'greetings' with symbol (Enter selection):

  '0': no association
  '1': greetings (*new*)
  '2': Greetings (*new*)
  '3': GREETINGS (*new*)

>  34:       elif this_word == hi:
 35:          this_word = greetings
 36:       else:
 37:          <CURSOR>

*** End of source buffer ***
Saying: ['this', 'word', 'equals', 'single', 'quotes', 'done', 'new', 'statement']
Heard this word equals single quotes done new statement
Associate 'done' with symbol (Enter selection):

  '0': no association
  '1': done (*new*)
  '2': Done (*new*)
  '3': DONE (*new*)

>  35:          this_word = greetings
 36:       else:
 37:          this_word = 'done'
 38:          <CURSOR>

*** End of source buffer ***
Saying: ['try', 'some', 'function', 'with', 'arguments']
Heard try some function with arguments
Associate 'some function' with symbol (Enter selection):

  '0': no association
  '1': some_function (*new*)
  '2': SomeFunction (*new*)
  '3': someFunction (*new*)
  '4': SOME_FUNCTION (*new*)
  '5': somefunction (*new*)
  '6': SOMEFUNCTION (*new*)

>  36:       else:
 37:          this_word = 'done'
 38:          try:
 39:             some_function(<CURSOR>)

*** End of source buffer ***
Saying: ['except', 'do', 'the', 'following', 'print', 'single', 'quotes', 'error']
Heard except do the following print single quotes error
Associate 'error' with symbol (Enter selection):

  '0': no association
  '1': error (*new*)
  '2': Error (*new*)
  '3': ERROR (*new*)

>  38:          try:
 39:             some_function()
 40:          except :
 41:             print 'error<CURSOR>'

*** End of source buffer ***
Saying: ['finally', 'do', 'print', 'single', 'quotes', 'all', 'right']
Heard finally do print single quotes all right
Associate 'all right' with symbol (Enter selection):

  '0': no association
  '1': all_right (*new*)
  '2': AllRight (*new*)
  '3': allRight (*new*)
  '4': ALL_RIGHT (*new*)
  '5': allright (*new*)
  '6': ALLRIGHT (*new*)

>  40:          except :
 41:             print 'error'
 42:          finally:
 43:             print 'all_right<CURSOR>'

*** End of source buffer ***

>>> Dictating Python when only standard symbols are known <<<

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
_cached_symbols_as_one_string is:
   
WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'O.', 'S.', ', \\comma', 'R.', 'E.', ', \\comma', 'string', ', \\comma', 'system', 'new', 'statement']
Heard import modules O. S. comma R. E. comma string comma system new statement
Associate 'O. S.' with symbol (Enter selection):

  '0': no association
  '1': os (*new*)
  '2': Os (*new*)
  '3': OS (*new*)

> Associate 'R. E.' with symbol (Enter selection):

  '0': no association
  '1': re (*new*)
  '2': Re (*new*)
  '3': RE (*new*)

> Associate 'string' with symbol (Enter selection):

  '0': no association
  '1': string (*new*)
  '2': String (*new*)
  '3': STRING (*new*)

> Associate 'system' with symbol (Enter selection):

  '0': no association
  '1': system (*new*)
  '2': System (*new*)
  '3': SYSTEM (*new*)

> *** Start of source buffer ***
  1: import os, re, string, system
  2: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'auto', 'test', ', \\comma', 'natural', 'link', ', \\comma', 'V.', 'C.', 'globals', 'new', 'statement']
Heard import modules auto test comma natural link comma V. C. globals new statement
Associate 'auto test' with symbol (Enter selection):

  '0': no association
  '1': auto_test (*new*)
  '2': AutoTest (*new*)
  '3': autoTest (*new*)
  '4': AUTO_TEST (*new*)
  '5': autotest (*new*)
  '6': AUTOTEST (*new*)

> Associate 'natural link' with symbol (Enter selection):

  '0': no association
  '1': natural_link (*new*)
  '2': NaturalLink (*new*)
  '3': naturalLink (*new*)
  '4': NATURAL_LINK (*new*)
  '5': naturallink (*new*)
  '6': NATURALLINK (*new*)

> Associate 'V. C. globals' with symbol (Enter selection):

  '0': no association
  '1': vc_globals (*new*)
  '2': VcGlobals (*new*)
  '3': vcGlobals (*new*)
  '4': VC_GLOBALS (*new*)
  '5': vcglobals (*new*)
  '6': VCGLOBALS (*new*)

> *** Start of source buffer ***
  1: import os, re, string, system
  2: import auto_test, natural_link, vc_globals
  3: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'actions', 'C.', 'C.', 'P.', 'P.', ' import all\\import all', 'new', 'statement']
Heard from module actions C. C. P. P. import all new statement
Associate 'actions C. C. P. P.' with symbol (Enter selection):

  '0': no association
  '1': actions_ccpp (*new*)
  '2': ActionsCcpp (*new*)
  '3': actionsCcpp (*new*)
  '4': ACTIONS_CCPP (*new*)
  '5': actionsccpp (*new*)
  '6': ACTIONSCCPP (*new*)

> *** Start of source buffer ***
  1: import os, re, string, system
  2: import auto_test, natural_link, vc_globals
  3: from actions_ccpp import all
  4: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'application', 'state', 'import', 'symbols', 'application', 'state', 'new', 'statement']
Heard from module application state import symbols application state new statement
Associate 'application state' with symbol (Enter selection):

  '0': no association
  '1': application_state (*new*)
  '2': ApplicationState (*new*)
  '3': applicationState (*new*)
  '4': APPLICATION_STATE (*new*)
  '5': applicationstate (*new*)
  '6': APPLICATIONSTATE (*new*)

>   2: import auto_test, natural_link, vc_globals
  3: from actions_ccpp import all
  4: from application_state import application_state
  5: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'context', 'generic', 'import', 'symbols', 'context', 'C.', 'comma', 'context', 'python', 'new', 'statement']
Heard from module context generic import symbols context C. comma context python new statement
Associate 'context generic' with symbol (Enter selection):

  '0': no association
  '1': context_generic (*new*)
  '2': ContextGeneric (*new*)
  '3': contextGeneric (*new*)
  '4': CONTEXT_GENERIC (*new*)
  '5': contextgeneric (*new*)
  '6': CONTEXTGENERIC (*new*)

> Associate 'context C.' with symbol (Enter selection):

  '0': no association
  '1': context_c (*new*)
  '2': ContextC (*new*)
  '3': contextC (*new*)
  '4': CONTEXT_C (*new*)
  '5': contextc (*new*)
  '6': CONTEXTC (*new*)

> Associate 'context python' with symbol (Enter selection):

  '0': no association
  '1': context_python (*new*)
  '2': ContextPython (*new*)
  '3': contextPython (*new*)
  '4': CONTEXT_PYTHON (*new*)
  '5': contextpython (*new*)
  '6': CONTEXTPYTHON (*new*)

>   3: from actions_ccpp import all
  4: from application_state import application_state
  5: from context_generic import context_c, context_python
  6: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'context', 'sensitive', 'command', 'import', 'symbols', 'context', 'sensitive', 'command', 'new', 'statement']
Heard from module context sensitive command import symbols context sensitive command new statement
Associate 'context sensitive command' with symbol (Enter selection):

  '0': no association
  '1': context_sensitive_command (*new*)
  '2': ContextSensitiveCommand (*new*)
  '3': contextSensitiveCommand (*new*)
  '4': CONTEXT_SENSITIVE_COMMAND (*new*)
  '5': contextsensitivecommand (*new*)
  '6': CONTEXTSENSITIVECOMMAND (*new*)

>   4: from application_state import application_state
  5: from context_generic import context_c, context_python
  6: from context_sensitive_command import context_sensitive_command
  7: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'Ed', 'simulator', 'import', 'symbol', 'Ed', 'simulator', 'new', 'statement']
Heard from module Ed simulator import symbol Ed simulator new statement
Associate 'Ed simulator' with symbol (Enter selection):

  '0': no association
  '1': ed_simulator (*new*)
  '2': EdSimulator (*new*)
  '3': edSimulator (*new*)
  '4': ED_SIMULATOR (*new*)
  '5': edsimulator (*new*)
  '6': EDSIMULATOR (*new*)

>   5: from context_generic import context_c, context_python
  6: from context_sensitive_command import context_sensitive_command
  7: from ed_simulator import ed_simulator
  8: <CURSOR>

*** End of source buffer ***
Saying: ['from', 'module', 'object', 'import', 'symbol', 'object', 'new', 'statement']
Heard from module object import symbol object new statement
Associate 'object' with symbol (Enter selection):

  '0': no association
  '1': object (*new*)
  '2': Object (*new*)
  '3': OBJECT (*new*)

>   6: from context_sensitive_command import context_sensitive_command
  7: from ed_simulator import ed_simulator
  8: from object import object
  9: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'modules', 'Ed', 'simulator', 'comma', 'symbol', 'dictionary', 'new', 'statement']
Heard import modules Ed simulator comma symbol dictionary new statement
Associate 'symbol dictionary' with symbol (Enter selection):

  '0': no association
  '1': symbol_dictionary (*new*)
  '2': SymbolDictionary (*new*)
  '3': symbolDictionary (*new*)
  '4': SYMBOL_DICTIONARY (*new*)
  '5': symboldictionary (*new*)
  '6': SYMBOLDICTIONARY (*new*)

>   7: from ed_simulator import ed_simulator
  8: from object import object
  9: import ed_simulator, symbol_dictionary
 10: <CURSOR>

*** End of source buffer ***
Saying: ['import', 'module', 'S.', 'R.', 'interface', 'new', 'statement']
Heard import module S. R. interface new statement
Associate 'S. R. interface' with symbol (Enter selection):

  '0': no association
  '1': sr_interface (*new*)
  '2': SrInterface (*new*)
  '3': srInterface (*new*)
  '4': SR_INTERFACE (*new*)
  '5': srinterface (*new*)
  '6': SRINTERFACE (*new*)

>   8: from object import object
  9: import ed_simulator, symbol_dictionary
 10: import sr_interface
 11: <CURSOR>

*** End of source buffer ***
Saying: ['define', 'class', 'command', 'interpreter', 'sub class\\sub class', 'of', 'object', 'class', 'body']
Heard define class command interpreter sub class of object class body
Associate 'command interpreter' with symbol (Enter selection):

  '0': no association
  '1': command_interpreter (*new*)
  '2': CommandInterpreter (*new*)
  '3': commandInterpreter (*new*)
  '4': COMMAND_INTERPRETER (*new*)
  '5': commandinterpreter (*new*)
  '6': COMMANDINTERPRETER (*new*)

>   9: import ed_simulator, symbol_dictionary
 10: import sr_interface
 11: class command_interpreter(object):
 12:    <CURSOR>

*** End of source buffer ***
Saying: ['define', 'method', 'initialize', 'add', 'argument', 'on', 'application', 'equals', 'none', 'comma']
Heard define method initialize add argument on application equals none comma
Associate 'initialize' with symbol (Enter selection):

  '0': no association
  '1': initialize (*new*)
  '2': Initialize (*new*)
  '3': INITIALIZE (*new*)

> Associate 'on application' with symbol (Enter selection):

  '0': no association
  '1': on_application (*new*)
  '2': OnApplication (*new*)
  '3': onApplication (*new*)
  '4': ON_APPLICATION (*new*)
  '5': onapplication (*new*)
  '6': ONAPPLICATION (*new*)

>   9: import ed_simulator, symbol_dictionary
 10: import sr_interface
 11: class command_interpreter(object):
 12:    def initialize(self, on_application = None, <CURSOR>):
 13:       

*** End of source buffer ***
Saying: ['symbol', 'dictionary', 'pickle', 'file', 'equals', 'none', 'comma', 'double', 'asterisk', 'attributes', 'method', 'body']
Heard symbol dictionary pickle file equals none comma double asterisk attributes method body
Associate 'symbol_dictionary pickle file' with symbol (Enter selection):

  '0': no association
  '1': symbol_dictionary_pickle_file (*new*)
  '2': SymbolDictionaryPickleFile (*new*)
  '3': symbolDictionaryPickleFile (*new*)
  '4': SYMBOL_DICTIONARY_PICKLE_FILE (*new*)
  '5': symboldictionarypicklefile (*new*)
  '6': SYMBOLDICTIONARYPICKLEFILE (*new*)

> Associate 'attributes' with symbol (Enter selection):

  '0': no association
  '1': attributes (*new*)
  '2': Attributes (*new*)
  '3': ATTRIBUTES (*new*)

>  10: import sr_interface
 11: class command_interpreter(object):
 12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       <CURSOR>

*** End of source buffer ***
Saying: ['self', 'dot', 'declare', 'attributes', 'with', 'arguments', 'brace', 'pair']
Heard self dot declare attributes with arguments brace pair
Associate 'declare attributes' with symbol (Enter selection):

  '0': no association
  '1': declare_attributes (*new*)
  '2': DeclareAttributes (*new*)
  '3': declareAttributes (*new*)
  '4': DECLARE_ATTRIBUTES (*new*)
  '5': declareattributes (*new*)
  '6': DECLAREATTRIBUTES (*new*)

>  10: import sr_interface
 11: class command_interpreter(object):
 12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       self.declare_attributes({<CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'un', 'translated', 'text', 'start', 'jump', 'out', ':\\colon', 'none', 'comma']
Heard single quotes un translated text start jump out colon none comma
Associate 'un translated text start' with symbol (Enter selection):

  '0': no association
  '1': un_translated_text_start (*new*)
  '2': UnTranslatedTextStart (*new*)
  '3': unTranslatedTextStart (*new*)
  '4': UN_TRANSLATED_TEXT_START (*new*)
  '5': untranslatedtextstart (*new*)
  '6': UNTRANSLATEDTEXTSTART (*new*)

>  10: import sr_interface
 11: class command_interpreter(object):
 12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       self.declare_attributes({'un_translated_text_start': None, <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'un', 'translated', 'text', 'end', 'jump', 'out', ':\\colon', 'none', 'new', 'statement']
Heard single quotes un translated text end jump out colon none new statement
Associate 'un translated text end' with symbol (Enter selection):

  '0': no association
  '1': un_translated_text_end (*new*)
  '2': UnTranslatedTextEnd (*new*)
  '3': unTranslatedTextEnd (*new*)
  '4': UN_TRANSLATED_TEXT_END (*new*)
  '5': untranslatedtextend (*new*)
  '6': UNTRANSLATEDTEXTEND (*new*)

>  11: class command_interpreter(object):
 12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       self.declare_attributes({'un_translated_text_start': None, 'un_translated_text_end': None})
 14:       <CURSOR>

*** End of source buffer ***
Saying: ['self', 'dot', 'deep', 'construct', 'with', 'arguments', 'command', 'interpreter', 'comma', 'continue', 'statement']
Heard self dot deep construct with arguments command interpreter comma continue statement
Associate 'deep construct' with symbol (Enter selection):

  '0': no association
  '1': deep_construct (*new*)
  '2': DeepConstruct (*new*)
  '3': deepConstruct (*new*)
  '4': DEEP_CONSTRUCT (*new*)
  '5': deepconstruct (*new*)
  '6': DEEPCONSTRUCT (*new*)

>  12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       self.declare_attributes({'un_translated_text_start': None, 'un_translated_text_end': None})
 14:       self.deep_construct(command_interpreter, \
 15:                           <CURSOR>)

*** End of source buffer ***
Saying: ['brace', 'pair', 'single', 'quotes', 'on', 'application', 'jump', 'out', ':\\colon', 'on', 'application', 'comma']
Heard brace pair single quotes on application jump out colon on application comma
 12:    def initialize(self, on_application = None, symbol_dictionary_pickle_file = None, **attributes):
 13:       self.declare_attributes({'un_translated_text_start': None, 'un_translated_text_end': None})
 14:       self.deep_construct(command_interpreter, \
 15:                           {'on_application': on_application, <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'known', 'symbols', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'dot', 'symbol', 'dictionary', 'without', 'arguments', 'comma', 'continue', 'statement']
Heard single quotes known symbols jump out colon symbol dictionary dot symbol dictionary without arguments comma continue statement
Associate 'known symbols' with symbol (Enter selection):

  '0': no association
  '1': known_symbols (*new*)
  '2': KnownSymbols (*new*)
  '3': knownSymbols (*new*)
  '4': KNOWN_SYMBOLS (*new*)
  '5': knownsymbols (*new*)
  '6': KNOWNSYMBOLS (*new*)

>  13:       self.declare_attributes({'un_translated_text_start': None, 'un_translated_text_end': None})
 14:       self.deep_construct(command_interpreter, \
 15:                           {'on_application': on_application, 'known_symbols': symbol_dictionary.symbol_dictionary(), \
 16:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'language', 'specific', 'aliases', 'jump', 'out', ':\\colon', 'empty', 'dictionary', 'comma', 'continue', 'statement']
Heard single quotes language specific aliases jump out colon empty dictionary comma continue statement
Associate 'language specific aliases' with symbol (Enter selection):

  '0': no association
  '1': language_specific_aliases (*new*)
  '2': LanguageSpecificAliases (*new*)
  '3': languageSpecificAliases (*new*)
  '4': LANGUAGE_SPECIFIC_ALIASES (*new*)
  '5': languagespecificaliases (*new*)
  '6': LANGUAGESPECIFICALIASES (*new*)

>  14:       self.deep_construct(command_interpreter, \
 15:                           {'on_application': on_application, 'known_symbols': symbol_dictionary.symbol_dictionary(), \
 16:                            'language_specific_aliases': {}, \
 17:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'last', 'loaded', 'language', 'jump', 'out', ':\\colon', 'none', 'comma', 'continue', 'statement']
Heard single quotes last loaded language jump out colon none comma continue statement
Associate 'last loaded language' with symbol (Enter selection):

  '0': no association
  '1': last_loaded_language (*new*)
  '2': LastLoadedLanguage (*new*)
  '3': lastLoadedLanguage (*new*)
  '4': LAST_LOADED_LANGUAGE (*new*)
  '5': lastloadedlanguage (*new*)
  '6': LASTLOADEDLANGUAGE (*new*)

>  15:                           {'on_application': on_application, 'known_symbols': symbol_dictionary.symbol_dictionary(), \
 16:                            'language_specific_aliases': {}, \
 17:                            'last_loaded_language': None, \
 18:                            <CURSOR>})

*** End of source buffer ***
Saying: ['single', 'quotes', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', ':\\colon', 'symbol', 'dictionary', 'pickle', 'file', 'jump', 'out', 'comma', 'continue', 'statement']
Heard single quotes symbol dictionary pickle file jump out colon symbol dictionary pickle file jump out comma continue statement
 16:                            'language_specific_aliases': {}, \
 17:                            'last_loaded_language': None, \
 18:                            'symbol_dictionary_pickle_file': symbol_dictionary_pickle_file}, \
 19:                           <CURSOR>)

*** End of source buffer ***
Saying: ['attributes', 'new', 'statement', 'new', 'statement']
Heard attributes new statement new statement
 18:                            'symbol_dictionary_pickle_file': symbol_dictionary_pickle_file}, \
 19:                           attributes)
 20: 
 21:       <CURSOR>

*** End of source buffer ***
Saying: ['back indent', 'define', 'method', 'spoken', 'form', 'regular', 'expression', 'add', 'argument', 'spoken', 'form']
Heard back indent define method spoken form regular expression add argument spoken form
Associate 'spoken form regular expression' with symbol (Enter selection):

  '0': no association
  '1': spoken_form_regular_expression (*new*)
  '2': SpokenFormRegularExpression (*new*)
  '3': spokenFormRegularExpression (*new*)
  '4': SPOKEN_FORM_REGULAR_EXPRESSION (*new*)
  '5': spokenformregularexpression (*new*)
  '6': SPOKENFORMREGULAREXPRESSION (*new*)

> Associate 'spoken form' with symbol (Enter selection):

  '0': no association
  '1': spoken_form (*new*)
  '2': SpokenForm (*new*)
  '3': spokenForm (*new*)
  '4': SPOKEN_FORM (*new*)
  '5': spokenform (*new*)
  '6': SPOKENFORM (*new*)

>  18:                            'symbol_dictionary_pickle_file': symbol_dictionary_pickle_file}, \
 19:                           attributes)
 20: 
 21:    def spoken_form_regular_expression(self, spoken_form<CURSOR>):
 22:       

*** End of source buffer ***
Saying: ['method', 'body']
Heard method body
 19:                           attributes)
 20: 
 21:    def spoken_form_regular_expression(self, spoken_form):
 22:       <CURSOR>

*** End of source buffer ***
Saying: ['words', 'equals', 'R.', 'E.', 'dot', 'split', 'with', 'arguments']
Heard words equals R. E. dot split with arguments
Associate 'words' with symbol (Enter selection):

  '0': no association
  '1': words (*new*)
  '2': Words (*new*)
  '3': WORDS (*new*)

> Associate 'R. E.' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': Re (*new*)
  '3': RE (*new*)

> Associate 'split' with symbol (Enter selection):

  '0': no association
  '1': split (*new*)
  '2': Split (*new*)
  '3': SPLIT (*new*)

>  19:                           attributes)
 20: 
 21:    def spoken_form_regular_expression(self, spoken_form):
 22:       words = re.split(<CURSOR>)

*** End of source buffer ***
Saying: ['single', 'quotes', '\\s\\back slash s.', 'plus', 'sign', 'jump', 'out', 'comma', 'spoken', 'form', 'new', 'statement']
Heard single quotes back slash s plus sign jump out comma spoken form new statement
 20: 
 21:    def spoken_form_regular_expression(self, spoken_form):
 22:       words = re.split('\s+', spoken_form)
 23:       <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'empty', 'single', 'quotes', 'new', 'statement']
Heard regular expression equals empty single quotes new statement
Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

>  21:    def spoken_form_regular_expression(self, spoken_form):
 22:       words = re.split('\s+', spoken_form)
 23:       re = ''
 24:       <CURSOR>

*** End of source buffer ***
Saying: ['for', 'loop', 'a', 'word', 'in', 'list', 'words', 'loop', 'body']
Heard for loop a word in list words loop body
Associate 'a word' with symbol (Enter selection):

  '0': no association
  '1': a_word (*new*)
  '2': AWord (*new*)
  '3': aWord (*new*)
  '4': A_WORD (*new*)
  '5': aword (*new*)
  '6': AWORD (*new*)

>  22:       words = re.split('\s+', spoken_form)
 23:       re = ''
 24:       for a_word in words:
 25:          <CURSOR>

*** End of source buffer ***
Saying: ['first', 'equals', 'a', 'word', 'at', 'index', '0', 'new', 'statement']
Heard first equals a word at index 0 new statement
Associate 'first' with symbol (Enter selection):

  '0': no association
  '1': first (*new*)
  '2': First (*new*)
  '3': FIRST (*new*)

>  23:       re = ''
 24:       for a_word in words:
 25:          first = a_word[0]
 26:          <CURSOR>

*** End of source buffer ***
Saying: ['rest', 'equals', 'a', 'word', 'at', 'index', '1', ':\\colon', 'new', 'statement']
Heard rest equals a word at index 1 colon new statement
Associate 'rest' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': rest (*new*)
  '3': Rest (*new*)
  '4': REST (*new*)

>  24:       for a_word in words:
 25:          first = a_word[0]
 26:          re = a_word[1: ]
 27:          <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'this', 'word', 'equals', 'single', 'quotes']
Heard regular expression this word equals single quotes
Associate 'regular expression this word' with symbol (Enter selection):

  '0': no association
  '1': regular_expression_this_word (*new*)
  '2': RegularExpressionThisWord (*new*)
  '3': regularExpressionThisWord (*new*)
  '4': REGULAR_EXPRESSION_THIS_WORD (*new*)
  '5': regularexpressionthisword (*new*)
  '6': REGULAREXPRESSIONTHISWORD (*new*)

>  24:       for a_word in words:
 25:          first = a_word[0]
 26:          re = a_word[1: ]
 27:          regular_expression_this_word = '<CURSOR>'

*** End of source buffer ***
Saying: ['open', 'bracket', 'jump', 'out', 'plus', 'string', 'dot', 'lower', 'with', 'arguments', 'first']
Heard open bracket jump out plus string dot lower with arguments first
Associate 'lower' with symbol (Enter selection):

  '0': no association
  '1': lower (*new*)
  '2': Lower (*new*)
  '3': LOWER (*new*)

>  24:       for a_word in words:
 25:          first = a_word[0]
 26:          re = a_word[1: ]
 27:          regular_expression_this_word = '[' + string.lower(first<CURSOR>)

*** End of source buffer ***
Saying: ['jump', 'out', 'plus', 'string', 'dot', 'upper', 'with', 'arguments', 'first', 'new', 'statement']
Heard jump out plus string dot upper with arguments first new statement
Associate 'upper' with symbol (Enter selection):

  '0': no association
  '1': upper (*new*)
  '2': Upper (*new*)
  '3': UPPER (*new*)

>  25:          first = a_word[0]
 26:          re = a_word[1: ]
 27:          regular_expression_this_word = '[' + string.lower(first) + string.upper(first)
 28:          <CURSOR>

*** End of source buffer ***
Saying: ['if', 'statement', 'not', 'regular', 'expression', 'equal', 'to', 'empty', 'single', 'quotes', 'if', 'body']
Heard if statement not regular expression equal to empty single quotes if body
Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

>  26:          re = a_word[1: ]
 27:          regular_expression_this_word = '[' + string.lower(first) + string.upper(first)
 28:          if not re == '':
 29:             <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'single', 'quotes', '\\s\\back slash s.', 'asterisk', 'new', 'statement']
Heard regular expression equals regular expression plus single quotes back slash s asterisk new statement
Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

> Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

>  27:          regular_expression_this_word = '[' + string.lower(first) + string.upper(first)
 28:          if not re == '':
 29:             re = re + '\s*'
 30:             <CURSOR>

*** End of source buffer ***
Saying: ['regular', 'expression', 'equals', 'regular', 'expression', 'plus', 'regular', 'expression', 'this', 'word', 'new', 'statement']
Heard regular expression equals regular expression plus regular expression this word new statement
Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

> Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

>  28:          if not re == '':
 29:             re = re + '\s*'
 30:             re = re + regular_expression_this_word
 31:             <CURSOR>

*** End of source buffer ***
Saying: ['return', 'regular', 'expression']
Heard return regular expression
Associate 'regular expression' with symbol (Enter selection):

  '0': no association
  '1': re
  '2': regular_expression (*new*)
  '3': RegularExpression (*new*)
  '4': regularExpression (*new*)
  '5': REGULAR_EXPRESSION (*new*)
  '6': regularexpression (*new*)
  '7': REGULAREXPRESSION (*new*)

>  28:          if not re == '':
 29:             re = re + '\s*'
 30:             re = re + regular_expression_this_word
 31:             return re<CURSOR>

*** End of source buffer ***
Saying: ['back indent', 'new statement']
Heard back indent new statement
 29:             re = re + '\s*'
 30:             re = re + regular_expression_this_word
 31:          return re
 32:       <CURSOR>

*** End of source buffer ***
Saying: ['if', 'not', 'this', 'word', 'then', 'this', 'word', 'equals', 'single', 'quotes', 'hello']
Heard if not this word then this word equals single quotes hello
Associate 'this word' with symbol (Enter selection):

  '0': no association
  '1': this_word (*new*)
  '2': ThisWord (*new*)
  '3': thisWord (*new*)
  '4': THIS_WORD (*new*)
  '5': thisword (*new*)
  '6': THISWORD (*new*)

> Associate 'hello' with symbol (Enter selection):

  '0': no association
  '1': hello (*new*)
  '2': Hello (*new*)
  '3': HELLO (*new*)

>  30:             re = re + regular_expression_this_word
 31:          return re
 32:       if not this_word:
 33:          this_word = 'hello<CURSOR>'

*** End of source buffer ***
Saying: ['else', 'if', 'this', 'word', 'is', 'equal', 'to', 'hi', 'then']
Heard else if this word is equal to hi then
Associate 'hi' with symbol (Enter selection):

  '0': no association
  '1': hi (*new*)
  '2': Hi (*new*)
  '3': HI (*new*)

>  32:       if not this_word:
 33:          this_word = 'hello'
 34:       elif this_word == hi:
 35:          <CURSOR>

*** End of source buffer ***
Saying: ['this', 'word', 'equals', 'greetings', 'else']
Heard this word equals greetings else
Associate 'greetings' with symbol (Enter selection):

  '0': no association
  '1': greetings (*new*)
  '2': Greetings (*new*)
  '3': GREETINGS (*new*)

>  34:       elif this_word == hi:
 35:          this_word = greetings
 36:       else:
 37:          <CURSOR>

*** End of source buffer ***
Saying: ['this', 'word', 'equals', 'single', 'quotes', 'done', 'new', 'statement']
Heard this word equals single quotes done new statement
Associate 'done' with symbol (Enter selection):

  '0': no association
  '1': done (*new*)
  '2': Done (*new*)
  '3': DONE (*new*)

>  35:          this_word = greetings
 36:       else:
 37:          this_word = 'done'
 38:          <CURSOR>

*** End of source buffer ***
Saying: ['try', 'some', 'function', 'with', 'arguments']
Heard try some function with arguments
Associate 'some function' with symbol (Enter selection):

  '0': no association
  '1': some_function (*new*)
  '2': SomeFunction (*new*)
  '3': someFunction (*new*)
  '4': SOME_FUNCTION (*new*)
  '5': somefunction (*new*)
  '6': SOMEFUNCTION (*new*)

>  36:       else:
 37:          this_word = 'done'
 38:          try:
 39:             some_function(<CURSOR>)

*** End of source buffer ***
Saying: ['except', 'do', 'the', 'following', 'print', 'single', 'quotes', 'error']
Heard except do the following print single quotes error
Associate 'error' with symbol (Enter selection):

  '0': no association
  '1': error (*new*)
  '2': Error (*new*)
  '3': ERROR (*new*)

>  38:          try:
 39:             some_function()
 40:          except :
 41:             print 'error<CURSOR>'

*** End of source buffer ***
Saying: ['finally', 'do', 'print', 'single', 'quotes', 'all', 'right']
Heard finally do print single quotes all right
Associate 'all right' with symbol (Enter selection):

  '0': no association
  '1': all_right (*new*)
  '2': AllRight (*new*)
  '3': allRight (*new*)
  '4': ALL_RIGHT (*new*)
  '5': allright (*new*)
  '6': ALLRIGHT (*new*)

>  40:          except :
 41:             print 'error'
 42:          finally:
 43:             print 'all_right<CURSOR>'

*** End of source buffer ***


*******************************************************************************
* Name        : python_editing
* Description : testing the various CSCs and LSAs for editing Python
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Data\TestData\edit_this_buff.py'
>>> Known symbols are: 
AClass: ['a class']
ASuper: ['a super']
SomeOtherClass: ['some other class']
a_method: ['a method']
a_method_with_no_arguments: ['a method with no arguments', 'a method with number arguments']
class: ['class']
def: ['def', 'definition', 'default', 'define', 'defined', 'deaf']
do_some_more: ['do some more']
do_some_stuff: ['do some stuff']
if: ['if']
pass: ['pass']
self: ['self']
some_argument: ['some argument']
some_array: ['some array']
some_other_method: ['some other method']
some_variable: ['some variable']
try: ['try']
yet_another_method: ['yet another method']
_cached_symbols_as_one_string is:
    class  AClass  ASuper  def  a_method  self  some_argument  some_variable  some_array  if  do_some_stuff  do_some_more  try  a_method_with_no_arguments  pass  SomeOtherClass  some_other_method  yet_another_method 

*********************
*** Executing edit test: insert an import statement in middle of a file ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
*** Start of source buffer ***
  1: # This is a small buffer for testing editing of Python code
  2: <CURSOR>
  3: 
  4: class AClass(ASuper):
  5:     """This is a dummy class"""
Heard import some module
Associate 'some module' with symbol (Enter selection):

  '0': no association
  '1': some_module (*new*)
  '2': SomeModule (*new*)
  '3': someModule (*new*)
  '4': SOME_MODULE (*new*)
  '5': somemodule (*new*)
  '6': SOMEMODULE (*new*)

> *** Start of source buffer ***
  1: # This is a small buffer for testing editing of Python code
  2: import some_module<CURSOR>
  3: 
  4: class AClass(ASuper):
  5:     """This is a dummy class"""

*********************
*** DONE with edit test: insert an import statement in middle of a file ***
*********************


*********************
*** Executing edit test: create new class ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
 17:         pass
 18:            
 19: 
 20: <CURSOR>
 21: 
 22: class SomeOtherClass():
 23: 
Heard there is a bug below
Associate 'there' with symbol (Enter selection):

  '0': no association
  '1': there (*new*)
  '2': There (*new*)
  '3': THERE (*new*)

> Associate 'a bug below' with symbol (Enter selection):

  '0': no association
  '1': a_bug_below (*new*)
  '2': ABugBelow (*new*)
  '3': aBugBelow (*new*)
  '4': A_BUG_BELOW (*new*)
  '5': abugbelow (*new*)
  '6': ABUGBELOW (*new*)

>  17:         pass
 18:            
 19: 
 20: there is a bug below<CURSOR>
 21: 
 22: class SomeOtherClass():
 23: 
Heard class new class class body
 19: 
 20: there is a bug belowclass class :
 21:    :
 22:    <CURSOR>
 23: 
 24: class SomeOtherClass():
 25: 
Heard define method new method method body pass
Associate 'new method' with symbol (Enter selection):

  '0': no association
  '1': new_method (*new*)
  '2': NewMethod (*new*)
  '3': newMethod (*new*)
  '4': NEW_METHOD (*new*)
  '5': newmethod (*new*)
  '6': NEWMETHOD (*new*)

>  21:    :
 22:    def new_method(self):
 23:       pass
 24:    <CURSOR>
 25: 
 26: class SomeOtherClass():
 27: 

*********************
*** DONE with edit test: create new class ***
*********************


*********************
*** Executing edit test: change subclass of existing class ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
*** Start of source buffer ***
  1: # This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: <CURSOR>class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, some_argument):
Heard select a super
*** Start of source buffer ***
  1: # This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(<SEL_START>ASuper<SEL_END>):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, some_argument):
Heard new super class
Associate 'new super' with symbol (Enter selection):

  '0': no association
  '1': new_super (*new*)
  '2': NewSuper (*new*)
  '3': newSuper (*new*)
  '4': NEW_SUPER (*new*)
  '5': newsuper (*new*)
  '6': NEWSUPER (*new*)

> *** Start of source buffer ***
  1: # This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(new_superclass <CURSOR>:
  5:              ):
  6:     """This is a dummy class"""
  7:     

*********************
*** DONE with edit test: change subclass of existing class ***
*********************


*********************
*** Executing edit test: add_method_to_existing_class_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
 16:     def a_method_with_no_arguments():
 17:         pass
 18:            
 19: <CURSOR>
 20: 
 21: 
 22: class SomeOtherClass():
Heard add method some method method body pass
Associate 'some method' with symbol (Enter selection):

  '0': no association
  '1': some_method (*new*)
  '2': SomeMethod (*new*)
  '3': someMethod (*new*)
  '4': SOME_METHOD (*new*)
  '5': somemethod (*new*)
  '6': SOMEMETHOD (*new*)

>  18:            
 19: def some_method(self):
 20:    pass
 21: <CURSOR>
 22: 
 23: 
 24: class SomeOtherClass():

*********************
*** DONE with edit test: add_method_to_existing_class_test ***
*********************


*********************
*** Executing edit test: add_argument_to_existing_method_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7: <CURSOR>    def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
Heard add argument extra argument
Associate 'extra argument' with symbol (Enter selection):

  '0': no association
  '1': extra_argument (*new*)
  '2': ExtraArgument (*new*)
  '3': extraArgument (*new*)
  '4': EXTRA_ARGUMENT (*new*)
  '5': extraargument (*new*)
  '6': EXTRAARGUMENT (*new*)

>   4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, some_argument, extra_argument<CURSOR>):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)

*********************
*** DONE with edit test: add_argument_to_existing_method_test ***
*********************


*********************
*** Executing edit test: change_existing_argument_of_a_method_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7: <CURSOR>    def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
Heard select some argument
  4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, <SEL_START>some_argument<SEL_END>):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
Heard new argument
Associate 'new argument' with symbol (Enter selection):

  '0': no association
  '1': new_argument (*new*)
  '2': NewArgument (*new*)
  '3': newArgument (*new*)
  '4': NEW_ARGUMENT (*new*)
  '5': newargument (*new*)
  '6': NEWARGUMENT (*new*)

>   4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, new_argument<CURSOR>):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)

*********************
*** DONE with edit test: change_existing_argument_of_a_method_test ***
*********************


*********************
*** Executing edit test: insert_line_of_code_in_method_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  5:     """This is a dummy class"""
  6:     
  7:     def a_method(self, some_argument):
  8: <CURSOR>        some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
 11:            do_some_more()
Heard new statement
  6:     
  7:     def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         <CURSOR>
 10:         if some_variable:
 11:            do_some_stuff(some_array)
 12:            do_some_more()
Heard some array equals none
  6:     
  7:     def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         some_array = None<CURSOR>
 10:         if some_variable:
 11:            do_some_stuff(some_array)
 12:            do_some_more()

*********************
*** DONE with edit test: insert_line_of_code_in_method_test ***
*********************


*********************
*** Executing edit test: change_arguments_in_method_call_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  7:     def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10: <CURSOR>           do_some_stuff(some_array)
 11:            do_some_more()
 12:            
 13:         try:
Heard select some array
  7:     def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(<SEL_START>some_array<SEL_END>)
 11:            do_some_more()
 12:            
 13:         try:
Heard none
  7:     def a_method(self, some_argument):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(None<CURSOR>)
 11:            do_some_more()
 12:            
 13:         try:
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(None)
 11: <CURSOR>           do_some_more()
 12:            
 13:         try:
 14:            do_some_stuff()
Heard after paren none
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(None)
 11:            do_some_more(None<CURSOR>)
 12:            
 13:         try:
 14:            do_some_stuff()

*********************
*** DONE with edit test: change_arguments_in_method_call_test ***
*********************


*********************
*** Executing edit test: nested_if_then_else_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
 11: <CURSOR>           do_some_more()
 12:            
 13:         try:
 14:            do_some_stuff()
Heard new statement if some flag then
Associate 'some flag' with symbol (Enter selection):

  '0': no association
  '1': some_flag (*new*)
  '2': SomeFlag (*new*)
  '3': someFlag (*new*)
  '4': SOME_FLAG (*new*)
  '5': someflag (*new*)
  '6': SOMEFLAG (*new*)

>  10:            do_some_stuff(some_array)
 11:            do_some_more()
 12:            if some_flag:
 13:               <CURSOR>
 14:            
 15:         try:
 16:            do_some_stuff()
Heard do some more stuff with arguments some argument
Associate 'do_some_more stuff' with symbol (Enter selection):

  '0': no association
  '1': do_some_stuff
  '2': do_some_more_stuff (*new*)
  '3': DoSomeMoreStuff (*new*)
  '4': doSomeMoreStuff (*new*)
  '5': DO_SOME_MORE_STUFF (*new*)
  '6': dosomemorestuff (*new*)
  '7': DOSOMEMORESTUFF (*new*)

>  10:            do_some_stuff(some_array)
 11:            do_some_more()
 12:            if some_flag:
 13:               do_some_stuff(some_argument<CURSOR>)
 14:            
 15:         try:
 16:            do_some_stuff()
Heard else do some stuff again with arguments some other argument
Associate 'do_some_stuff again' with symbol (Enter selection):

  '0': no association
  '1': do_some_stuff_again (*new*)
  '2': DoSomeStuffAgain (*new*)
  '3': doSomeStuffAgain (*new*)
  '4': DO_SOME_STUFF_AGAIN (*new*)
  '5': dosomestuffagain (*new*)
  '6': DOSOMESTUFFAGAIN (*new*)

> Associate 'some other argument' with symbol (Enter selection):

  '0': no association
  '1': some_other_argument (*new*)
  '2': SomeOtherArgument (*new*)
  '3': someOtherArgument (*new*)
  '4': SOME_OTHER_ARGUMENT (*new*)
  '5': someotherargument (*new*)
  '6': SOMEOTHERARGUMENT (*new*)

>  12:            if some_flag:
 13:               do_some_stuff(some_argument)
 14:            else:
 15:               do_some_stuff_again(some_other_argument<CURSOR>)
 16:            
 17:         try:
 18:            do_some_stuff()
Heard else do some stuff without arguments
 14:            else:
 15:               do_some_stuff_again(some_other_argument)
 16:            else:
 17:               do_some_stuff()<CURSOR>
 18:            
 19:         try:
 20:            do_some_stuff()

*********************
*** DONE with edit test: nested_if_then_else_test ***
*********************


*********************
*** Executing edit test: add_else_clause_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
  8:         some_variable = some_array[0]
  9:         if some_variable:
 10:            do_some_stuff(some_array)
 11: <CURSOR>           do_some_more()
 12:            
 13:         try:
 14:            do_some_stuff()
Heard else clause
 10:            do_some_stuff(some_array)
 11:            do_some_more()
 12:         else:
 13:            <CURSOR>
 14:            
 15:         try:
 16:            do_some_stuff()

*********************
*** DONE with edit test: add_else_clause_test ***
*********************


*********************
*** Executing edit test: add_except_clause_test ***
*********************

*** Start of source buffer ***
  1: <CURSOR># This is a small buffer for testing editing of Python code
  2: 
  3: 
  4: class AClass(ASuper):
 23: 
 24: 	def some_other_method(self):
 25: 	   try:
 26: <CURSOR>	      do_some_stuff()
 27: 	       
 28: 	def yet_another_method(self):
 29: 	   pass

*** End of source buffer ***
Heard catch exceptions
 24: 	def some_other_method(self):
 25: 	   try:
 26: 	      do_some_stuff()
 27: 	   except <CURSOR>:
 28: 	      
 29: 	       
 30: 	def yet_another_method(self):

*********************
*** DONE with edit test: add_except_clause_test ***
*********************



*******************************************************************************
* Name        : redundant_translation
* Description : testing redundant translation of LSAs and symbols at SR and Mediator level
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file('blah.c')

WARNING: source file 'blah.c' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***


>>> Testing console command: compile_symbols([r'H:\Projects\VoiceCode\VCode\Data\TestData\small_buff.c'])

Compiling symbols for file '%VCODE_HOME%\Data\TestData\small_buff.c'
>>> Known symbols are: 
API_function: ['api function']
f_name: ['f name']
f_name2: ['f name 2']
float: ['float']
horiz_pos: ['horiz pos', 'horiz position', 'horiz positioning', 'horizontal pos', 'horizontal position', 'horizontal positioning', 'horizontally pos', 'horizontally position', 'horizontally positioning']
move: ['move']
move_horiz: ['move horiz', 'move horizontal', 'move horizontally']
move_vert: ['move vert', 'move vertical', 'move vertically']
this_sym_has_an_other_abbrev: ['this sym has an other abbrev', 'this symbol has an other abbrev']
this_sym_is_unres: ['this sym is unres', 'this symbol is unres']
this_sym_is_unres_too: ['this sym is unres too', 'this symbol is unres too']
void: ['void']
x: ['x']
y: ['y']
_cached_symbols_as_one_string is:
    void  move  float  x  y  move_horiz  move_vert  horiz_pos  this_sym_is_unres  this_sym_is_unres_too  this_sym_has_an_other_abbrev  f_name  f_name2  API_function 


>>> Testing console command: say(['index', ' != \\not equal to', '0'], user_input='0
0
')
Heard index not equal to 0
Associate 'index' with symbol (Enter selection):

  '0': no association
  '1': index (*new*)
  '2': Index (*new*)
  '3': INDEX (*new*)

> *** Start of source buffer ***
  1: index != 0<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'not', 'equal', 'to', '0'], user_input='0
0
')
Heard index not equal to 0
Associate 'index' with symbol (Enter selection):

  '0': no association
  '1': index (*new*)
  '2': Index (*new*)
  '3': INDEX (*new*)

> *** Start of source buffer ***
  1: index != 0index != 0<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['move_horiz\\move horizontally'], user_input='0
0
')
Heard move horizontally
*** Start of source buffer ***
  1: index != 0index != 0move_horiz<CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['move', 'horizontally'], user_input='0
0
')
Heard move horizontally
*** Start of source buffer ***
  1: index != 0index != 0move_horizmove_horiz<CURSOR>

*** End of source buffer ***


>>> Testing console command: quit(save_speech_files=0, disconnect=0)



*******************************************************************************
* Name        : repeat_last
* Description : testing repetition of last command
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file(r'H:\Projects\VoiceCode\VCode\Data\TestData\large_buff.py')

*** Start of source buffer ***
  1: <CURSOR>
  2: # This symbol is here because it is homophonic with auto_test. Just checking
  3: # to make sure that symbol match works with homophonic symbols.
  4: autoTst = 0


>>> Testing console command: say(['after hyphen'])

Heard after hyphen
 11:     This class implements various useful behaviors for generic
 12:     objects, such as:
 13: 
 14:     - <CURSOR>safe attribute setting
 15:     - deep constructor
 16:     - pretty printing???
 17:     


>>> Testing console command: say(['again'])

Heard again
 12:     objects, such as:
 13: 
 14:     - safe attribute setting
 15:     - <CURSOR>deep constructor
 16:     - pretty printing???
 17:     
 18: 


>>> Testing console command: goto_line(1)

*** Start of source buffer ***
  1: <CURSOR>
  2: # This symbol is here because it is homophonic with auto_test. Just checking
  3: # to make sure that symbol match works with homophonic symbols.
  4: autoTst = 0


>>> Testing console command: say(['after hyphen'])

Heard after hyphen
 11:     This class implements various useful behaviors for generic
 12:     objects, such as:
 13: 
 14:     - <CURSOR>safe attribute setting
 15:     - deep constructor
 16:     - pretty printing???
 17:     


>>> Testing console command: say(['again 3 times'])

Heard again 3 times
 35: 
 36:     Profile tests on NT indicate that:
 37: 
 38:     - <CURSOR>the speed of constructors for Object and non-Object instances are the same
 39:     - the speed of attribute *gets* is the same for Object and non-Object instances
 40:     - when *$PY_DEBUG_OBJECT=0*, the performance of attribute *sets* is the same for Object and non-Object instances
 41:     - when *$PY_DEBUG_OBJECT=1*, attribute *sets* are slower by a factor of about 15 for Object instances than for non-Object instances


>>> Testing console command: goto_line(1)

*** Start of source buffer ***
  1: <CURSOR>
  2: # This symbol is here because it is homophonic with auto_test. Just checking
  3: # to make sure that symbol match works with homophonic symbols.
  4: autoTst = 0


>>> Testing console command: say(['after hyphen'])

Heard after hyphen
 11:     This class implements various useful behaviors for generic
 12:     objects, such as:
 13: 
 14:     - <CURSOR>safe attribute setting
 15:     - deep constructor
 16:     - pretty printing???
 17:     


>>> Testing console command: say(['3 times'])

Heard 3 times
 13: 
 14:     - safe attribute setting
 15:     - deep constructor
 16:     - <CURSOR>pretty printing???
 17:     
 18: 
 19:     **SAFE ATTRIBUTE SETTING***


*******************************************************************************
* Name        : rsm_algorithm
* Description : Testing RecogStartMgr algorithm.
*******************************************************************************

new instance in window 14
new instance of emacs 1
with window 14
SelectWinGramDummy for buffer None, window 14
init

instance emacs(0)
running in module emacs
windows:  [14]
window #14:
all instances for window:
emacs(0)

new window 20
new buffer fish.C for instance 1
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;

instance emacs(0)
running in module emacs
windows:  [14]
window #14:
all instances for window:
emacs(0)

starting recognition in  (20, 'emacs - (Yak 0) - fish.C', 'emacs')
SelectWinGramDummy for buffer None, window 20
init
DictWinGramDummy for buffer = 'fish.C', window 20
init
SelectWinGramDummy for buffer 'fish.C', window 20
activating:  20  
DictWinGramDummy for buffer = 'fish.C', window 20
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', window 20
activating:  20  

instance emacs(0)
running in module emacs
windows:  [14, 20]
window #14:
all instances for window:
emacs(0)
window #20:
all instances for window:
emacs(0)

starting recognition in  (50, 'D:\\Projects', 'browseui')

instance emacs(0)
running in module emacs
windows:  [14, 20]
window #14:
all instances for window:
emacs(0)
window #20:
all instances for window:
emacs(0)

new instance in telnet window 5
new instance of emacs 5
with window 5

instance emacs(1)
(unknown module)
windows:  []


state {
application:  emacs
instance:  emacs(0)
window 14
window 20
instance:  emacs(1)
known windows [14, 20]
} state

now specifying window
SelectWinGramDummy for buffer None, window 5
init
success

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

starting recognition in  (8, 'ttssh - acappella', 'telnet')

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

starting recognition in  (5, 'ttssh - acappella', 'telnet')
DictWinGramDummy for buffer = 'bug.c', window 5
init
SelectWinGramDummy for buffer 'bug.c', window 5
activating:  5  
DictWinGramDummy for buffer = 'bug.c', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'bug.c', window 5
activating:  5  

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

suspending  emacs(1)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

new instance of emacs 6

instance emacs(2)
(unknown module)
windows:  []


instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

now specifying window
SelectWinGramDummy for buffer None, window 5
init
success

instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

starting recognition in  (5, 'ttssh - acappella', 'telnet')
DictWinGramDummy for buffer = 'dog.q', window 5
init
SelectWinGramDummy for buffer 'dog.q', window 5
activating:  5  
DictWinGramDummy for buffer = 'dog.q', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'dog.q', window 5
activating:  5  
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

suspending  emacs(2)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'dog.q', window 5
deactivating
DictWinGramDummy for buffer = 'dog.q', window 5
deactivating
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

resuming  emacs(1)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'bug.c', window 5
activating:  5  
DictWinGramDummy for buffer = 'bug.c', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'bug.c', window 5
activating:  5  
SelectWinGramDummy for buffer 'dog.q', window 5
deactivating
DictWinGramDummy for buffer = 'dog.q', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)
emacs(2)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)
emacs(2)

new Vim instance in exceed window 15
new instance of Vim 10
with window 15
SelectWinGramDummy for buffer None, window 15
init
new buffer dog.pl for instance 10
 10:     $dirSep = "\";
 11:     $curDirCom = 'cd';
 12: } else {
 13:     $dirSep = <CURSOR>'/';
 14:     $curDirCom = 'pwd';
 15: };
 16: 

*** End of source buffer ***

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)


state {
application:  Vim
instance:  Vim(0)
window 15
application:  emacs
instance:  emacs(0)
window 14
window 20
instance:  emacs(1)
window 5
instance:  emacs(2)
window 5
known windows [15, 14, 5, 20]
} state

starting recognition in  (15, 'Vim - (Oldie 0) - dog.pl', 'exceed')
DictWinGramDummy for buffer = 'dog.pl', window 15
init
SelectWinGramDummy for buffer 'dog.pl', window 15
activating:  15  
DictWinGramDummy for buffer = 'dog.pl', window 15
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', window 15
activating:  15  

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)

suspending  Vim(0)
starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)

new emacs instance in exceed window 15
new instance of emacs 7
with window 15

instance emacs(3)
(unknown module)
windows:  []

starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
(unknown module)
windows:  []

now specifying window
SelectWinGramDummy for buffer None, window 15
init
success

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

starting recognition in  (15, 'xterm - acappella', 'exceed')
DictWinGramDummy for buffer = 'nothing.py', window 15
init
SelectWinGramDummy for buffer 'nothing.py', window 15
activating:  15  
DictWinGramDummy for buffer = 'nothing.py', window 15
setting context: before = [], after = []
DictWinGramDummy for buffer = 'nothing.py', window 15
activating:  15  
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

suspending  emacs(3)
starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'nothing.py', window 15
deactivating
DictWinGramDummy for buffer = 'nothing.py', window 15
deactivating
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

resuming  Vim(0)
starting recognition in  (15, 'Vim - (Oldie 0) - dog.pl', 'exceed')
SelectWinGramDummy for buffer 'dog.pl', window 15
activating:  15  
DictWinGramDummy for buffer = 'dog.pl', window 15
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', window 15
activating:  15  
SelectWinGramDummy for buffer 'nothing.py', window 15
deactivating
DictWinGramDummy for buffer = 'nothing.py', window 15
deactivating

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)
emacs(3)

new emacs instance in exceed window 25
new instance of emacs 9
with window 25
SelectWinGramDummy for buffer None, window 25
init

instance emacs(4)
running in module exceed
windows:  [25]
window #25:
all instances for window:
emacs(4)

starting recognition in  (25, 'emacs - (Yak 4) - .cshrc', 'exceed')
DictWinGramDummy for buffer = '.cshrc', window 25
init
SelectWinGramDummy for buffer '.cshrc', window 25
activating:  25  
DictWinGramDummy for buffer = '.cshrc', window 25
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 25
activating:  25  

instance emacs(4)
running in module exceed
windows:  [25]
window #25:
all instances for window:
emacs(4)

app reports new window (is current)
current is (26, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer None, window 26
init

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)

starting recognition in  (26, 'emacs - (Yak 4) - .cshrc', 'exceed')
DictWinGramDummy for buffer = '.cshrc', window 26
init
SelectWinGramDummy for buffer '.cshrc', window 26
activating:  26  
DictWinGramDummy for buffer = '.cshrc', window 26
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 26
activating:  26  

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)

app reports new window (is not current)
current is (15, 'xterm - acappella', 'exceed')

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)


instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)
emacs(3)

but now it is
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer None, window 27
init
DictWinGramDummy for buffer = '.cshrc', window 27
init
SelectWinGramDummy for buffer '.cshrc', window 27
activating:  27  
DictWinGramDummy for buffer = '.cshrc', window 27
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 27
activating:  27  

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)

new universal instance of WaxEdit 12
now it is on WaxEdit
starting recognition in  (99, 'WaxEdit - (Floor 0) - large_buff.py', 'python')
SelectWinGramDummy for buffer None, global
init
DictWinGramDummy for buffer = 'large_buff.py', global
init
SelectWinGramDummy for buffer 'large_buff.py', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'large_buff.py', global
setting context: before = [], after = []
DictWinGramDummy for buffer = 'large_buff.py', global
activating:  global  exclusive 


instance WaxEdit(0)
(unknown module)
windows:  []

but now it is
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer 'large_buff.py', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'large_buff.py', global
setting context: before = [], after = []
DictWinGramDummy for buffer = 'large_buff.py', global
activating:  global  exclusive 

SelectWinGramDummy for buffer '.cshrc', window 27
deactivating
DictWinGramDummy for buffer = '.cshrc', window 27
deactivating

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)


instance WaxEdit(0)
(unknown module)
windows:  []

SelectWinGramDummy for buffer 'large_buff.py', global
deactivating
DictWinGramDummy for buffer = 'large_buff.py', global
deactivating
SelectWinGramDummy for buffer 'large_buff.py', global
del
DictWinGramDummy for buffer = 'large_buff.py', global
del
and now the WaxEdit is gone
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer '.cshrc', window 27
activating:  27  
DictWinGramDummy for buffer = '.cshrc', window 27
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 27
activating:  27  

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)



*******************************************************************************
* Name        : rsm_algorithm_trust
* Description : Testing RecogStartMgr algorithm.
*******************************************************************************

new instance in window 14
new instance of emacs 1
with window 14
SelectWinGramDummy for buffer None, window 14
init

instance emacs(0)
running in module emacs
windows:  [14]
window #14:
all instances for window:
emacs(0)

new window 20
new buffer fish.C for instance 1
*** Start of source buffer ***
  1: /* This is a small test buffer for C */
  2: 
  3: void move(float x, y)
  4: <CURSOR>{
  5:   move_horiz(x);
  6:   move_vert(y)
  7:   horiz_pos = 0;

instance emacs(0)
running in module emacs
windows:  [14]
window #14:
all instances for window:
emacs(0)

starting recognition in  (20, 'emacs - (Yak 0) - fish.C', 'emacs')
SelectWinGramDummy for buffer None, window 20
init
DictWinGramDummy for buffer = 'fish.C', window 20
init
SelectWinGramDummy for buffer 'fish.C', window 20
activating:  20  
DictWinGramDummy for buffer = 'fish.C', window 20
setting context: before = [ x, y)
], after = [{
  move_horiz(x);
  ]
DictWinGramDummy for buffer = 'fish.C', window 20
activating:  20  

instance emacs(0)
running in module emacs
windows:  [14, 20]
window #14:
all instances for window:
emacs(0)
window #20:
all instances for window:
emacs(0)

starting recognition in  (50, 'D:\\Projects', 'browseui')

instance emacs(0)
running in module emacs
windows:  [14, 20]
window #14:
all instances for window:
emacs(0)
window #20:
all instances for window:
emacs(0)

new instance in telnet window 5
new instance of emacs 5
with window 5
SelectWinGramDummy for buffer None, window 5
init

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)


state {
application:  emacs
instance:  emacs(0)
window 14
window 20
instance:  emacs(1)
window 5
known windows [14, 5, 20]
} state

now specifying window
failed

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

starting recognition in  (8, 'ttssh - acappella', 'telnet')

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

starting recognition in  (5, 'ttssh - acappella', 'telnet')
DictWinGramDummy for buffer = 'bug.c', window 5
init
SelectWinGramDummy for buffer 'bug.c', window 5
activating:  5  
DictWinGramDummy for buffer = 'bug.c', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'bug.c', window 5
activating:  5  

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

suspending  emacs(1)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

new instance of emacs 6

instance emacs(2)
(unknown module)
windows:  []


instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)

now specifying window
SelectWinGramDummy for buffer None, window 5
init
success

instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

starting recognition in  (5, 'ttssh - acappella', 'telnet')
DictWinGramDummy for buffer = 'dog.q', window 5
init
SelectWinGramDummy for buffer 'dog.q', window 5
activating:  5  
DictWinGramDummy for buffer = 'dog.q', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'dog.q', window 5
activating:  5  
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

suspending  emacs(2)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'dog.q', window 5
deactivating
DictWinGramDummy for buffer = 'dog.q', window 5
deactivating
SelectWinGramDummy for buffer 'bug.c', window 5
deactivating
DictWinGramDummy for buffer = 'bug.c', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(2)
emacs(1)

resuming  emacs(1)
starting recognition in  (5, 'ttssh - acappella', 'telnet')
SelectWinGramDummy for buffer 'bug.c', window 5
activating:  5  
DictWinGramDummy for buffer = 'bug.c', window 5
setting context: before = [], after = []
DictWinGramDummy for buffer = 'bug.c', window 5
activating:  5  
SelectWinGramDummy for buffer 'dog.q', window 5
deactivating
DictWinGramDummy for buffer = 'dog.q', window 5
deactivating

instance emacs(1)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)
emacs(2)


instance emacs(2)
running in module telnet
windows:  [5]
window #5:
shared
all instances for window:
emacs(1)
emacs(2)

new Vim instance in exceed window 15
new instance of Vim 10
with window 15
SelectWinGramDummy for buffer None, window 15
init
new buffer dog.pl for instance 10
 10:     $dirSep = "\";
 11:     $curDirCom = 'cd';
 12: } else {
 13:     $dirSep = <CURSOR>'/';
 14:     $curDirCom = 'pwd';
 15: };
 16: 

*** End of source buffer ***

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)


state {
application:  Vim
instance:  Vim(0)
window 15
application:  emacs
instance:  emacs(0)
window 14
window 20
instance:  emacs(1)
window 5
instance:  emacs(2)
window 5
known windows [15, 14, 5, 20]
} state

starting recognition in  (15, 'Vim - (Oldie 0) - dog.pl', 'exceed')
DictWinGramDummy for buffer = 'dog.pl', window 15
init
SelectWinGramDummy for buffer 'dog.pl', window 15
activating:  15  
DictWinGramDummy for buffer = 'dog.pl', window 15
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', window 15
activating:  15  

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)

suspending  Vim(0)
starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)

new emacs instance in exceed window 15
new instance of emacs 7
with window 15
SelectWinGramDummy for buffer None, window 15
init

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

starting recognition in  (15, 'xterm - acappella', 'exceed')
DictWinGramDummy for buffer = 'nothing.py', window 15
init
SelectWinGramDummy for buffer 'nothing.py', window 15
activating:  15  
DictWinGramDummy for buffer = 'nothing.py', window 15
setting context: before = [], after = []
DictWinGramDummy for buffer = 'nothing.py', window 15
activating:  15  
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

now specifying window
failed

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'nothing.py', window 15
activating:  15  
DictWinGramDummy for buffer = 'nothing.py', window 15
setting context: before = [], after = []
DictWinGramDummy for buffer = 'nothing.py', window 15
activating:  15  
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

suspending  emacs(3)
starting recognition in  (15, 'xterm - acappella', 'exceed')
SelectWinGramDummy for buffer 'nothing.py', window 15
deactivating
DictWinGramDummy for buffer = 'nothing.py', window 15
deactivating
SelectWinGramDummy for buffer 'dog.pl', window 15
deactivating
DictWinGramDummy for buffer = 'dog.pl', window 15
deactivating

instance emacs(3)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
emacs(3)
Vim(0)

resuming  Vim(0)
starting recognition in  (15, 'Vim - (Oldie 0) - dog.pl', 'exceed')
SelectWinGramDummy for buffer 'dog.pl', window 15
activating:  15  
DictWinGramDummy for buffer = 'dog.pl', window 15
setting context: before = [
    $dirSep = ], after = ['/';
    $curDirCom ]
DictWinGramDummy for buffer = 'dog.pl', window 15
activating:  15  
SelectWinGramDummy for buffer 'nothing.py', window 15
deactivating
DictWinGramDummy for buffer = 'nothing.py', window 15
deactivating

instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)
emacs(3)

new emacs instance in exceed window 25
new instance of emacs 9
with window 25
SelectWinGramDummy for buffer None, window 25
init

instance emacs(4)
running in module exceed
windows:  [25]
window #25:
all instances for window:
emacs(4)

starting recognition in  (25, 'emacs - (Yak 4) - .cshrc', 'exceed')
DictWinGramDummy for buffer = '.cshrc', window 25
init
SelectWinGramDummy for buffer '.cshrc', window 25
activating:  25  
DictWinGramDummy for buffer = '.cshrc', window 25
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 25
activating:  25  

instance emacs(4)
running in module exceed
windows:  [25]
window #25:
all instances for window:
emacs(4)

app reports new window (is current)
current is (26, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer None, window 26
init

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)

starting recognition in  (26, 'emacs - (Yak 4) - .cshrc', 'exceed')
DictWinGramDummy for buffer = '.cshrc', window 26
init
SelectWinGramDummy for buffer '.cshrc', window 26
activating:  26  
DictWinGramDummy for buffer = '.cshrc', window 26
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 26
activating:  26  

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)

app reports new window (is not current)
current is (15, 'xterm - acappella', 'exceed')

instance emacs(4)
running in module exceed
windows:  [25, 26]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)


instance Vim(0)
running in module exceed
windows:  [15]
window #15:
shared
all instances for window:
Vim(0)
emacs(3)

but now it is
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer None, window 27
init
DictWinGramDummy for buffer = '.cshrc', window 27
init
SelectWinGramDummy for buffer '.cshrc', window 27
activating:  27  
DictWinGramDummy for buffer = '.cshrc', window 27
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 27
activating:  27  

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)

new universal instance of WaxEdit 12
now it is on WaxEdit
starting recognition in  (99, 'WaxEdit - (Floor 0) - large_buff.py', 'python')
SelectWinGramDummy for buffer None, global
init
DictWinGramDummy for buffer = 'large_buff.py', global
init
SelectWinGramDummy for buffer 'large_buff.py', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'large_buff.py', global
setting context: before = [], after = []
DictWinGramDummy for buffer = 'large_buff.py', global
activating:  global  exclusive 


instance WaxEdit(0)
(unknown module)
windows:  []

but now it is
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer 'large_buff.py', global
activating:  global  exclusive 

DictWinGramDummy for buffer = 'large_buff.py', global
setting context: before = [], after = []
DictWinGramDummy for buffer = 'large_buff.py', global
activating:  global  exclusive 

SelectWinGramDummy for buffer '.cshrc', window 27
deactivating
DictWinGramDummy for buffer = '.cshrc', window 27
deactivating

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)


instance WaxEdit(0)
(unknown module)
windows:  []

SelectWinGramDummy for buffer 'large_buff.py', global
deactivating
DictWinGramDummy for buffer = 'large_buff.py', global
deactivating
SelectWinGramDummy for buffer 'large_buff.py', global
del
DictWinGramDummy for buffer = 'large_buff.py', global
del
and now the WaxEdit is gone
current is (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
starting recognition in  (27, 'emacs - (Yak 4) - .cshrc', 'exceed')
SelectWinGramDummy for buffer '.cshrc', window 27
activating:  27  
DictWinGramDummy for buffer = '.cshrc', window 27
setting context: before = [], after = []
DictWinGramDummy for buffer = '.cshrc', window 27
activating:  27  

instance emacs(4)
running in module exceed
windows:  [25, 26, 27]
window #25:
all instances for window:
emacs(4)
window #26:
all instances for window:
emacs(4)
window #27:
all instances for window:
emacs(4)



*******************************************************************************
* Name        : select_pseudocode
* Description : testing select pseudocode commands
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'


>>> Testing console command: open_file('blah.py')

WARNING: source file 'blah.py' doesn't exist.
*** Start of source buffer ***
  1: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'equals', '0', 'new statement'], user_input='1\n')
Heard index equals 0 new statement
Associate 'index' with symbol (Enter selection):

  '0': no association
  '1': index (*new*)
  '2': Index (*new*)
  '3': INDEX (*new*)

> *** Start of source buffer ***
  1: index = 0
  2: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'equals', '1', 'new statement'], user_input='1\n')
Heard index equals 1 new statement
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'equals', '0', 'new statement'], user_input='1\n')
Heard index equals 0 new statement
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0
  4: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'equals', '1', 'new statement'], user_input='1\n')
Heard index equals 1 new statement
  2: index = 1
  3: index = 0
  4: index = 1
  5: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['index', 'equals', '0', 'new statement'], user_input='1\n')
Heard index equals 0 new statement
  3: index = 0
  4: index = 1
  5: index = 0
  6: <CURSOR>

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go', 'index', '=\\equals', '0'], user_input='None')
Heard go index equals 0
*** Start of source buffer ***
  1: index = 0<CURSOR>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go after next', 'index', '=\\equals', '0'], user_input='None')
Heard go after next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0<CURSOR>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go after previous', 'index', '=\\equals', '0'], user_input='None')
Heard go after previous index equals 0
*** Start of source buffer ***
  1: index = 0<CURSOR>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go before', 'index', '=\\equals', '0'], user_input='None')
Heard go before index equals 0
*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go before next', 'index', '=\\equals', '0'], user_input='None')
Heard go before next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <CURSOR>index = 0
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go before previous', 'index', '=\\equals', '0'], user_input='None')
Heard go before previous index equals 0
*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go next', 'index', '=\\equals', '0'], user_input='None')
Heard go next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0<CURSOR>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['go previous', 'index', '=\\equals', '0'], user_input='None')
Heard go previous index equals 0
*** Start of source buffer ***
  1: index = 0<CURSOR>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['after next', 'index', '=\\equals', '0'], user_input='None')
Heard after next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0<CURSOR>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['after previous', 'index', '=\\equals', '0'], user_input='None')
Heard after previous index equals 0
*** Start of source buffer ***
  1: index = 0<CURSOR>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['before', 'index', '=\\equals', '0'], user_input='None')
Heard before index equals 0
*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['before next', 'index', '=\\equals', '0'], user_input='None')
Heard before next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <CURSOR>index = 0
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['before previous', 'index', '=\\equals', '0'], user_input='None')
Heard before previous index equals 0
*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['next', 'index', '=\\equals', '0'], user_input='None')
Heard next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <SEL_START>index = 0<SEL_END>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['previous', 'index', '=\\equals', '0'], user_input='None')
Heard previous index equals 0
*** Start of source buffer ***
  1: <SEL_START>index = 0<SEL_END>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['select', 'index', '=\\equals', '0'], user_input='None')
Heard select index equals 0
*** Start of source buffer ***
  1: <SEL_START>index = 0<SEL_END>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['select next', 'index', '=\\equals', '0'], user_input='None')
Heard select next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <SEL_START>index = 0<SEL_END>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(2)

*** Start of source buffer ***
  1: index = 0
  2: <CURSOR>index = 1
  3: index = 0
  4: index = 1
  5: index = 0


>>> Testing console command: say(['select previous', 'index', '=\\equals', '0'], user_input='None')
Heard select previous index equals 0
*** Start of source buffer ***
  1: <SEL_START>index = 0<SEL_END>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: goto_line(1)

*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: say(['go next', 'index', '=\\equals', '0'], user_input='None')
Heard go next index equals 0
*** Start of source buffer ***
  1: index = 0<CURSOR>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: say(['go next', 'index', '=\\equals', '0'], user_input='None')
Heard go next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0<CURSOR>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(6)

  3: index = 0
  4: index = 1
  5: index = 0
  6: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['go previous', 'index', '=\\equals', '0'], user_input='None')
Heard go previous index equals 0
  2: index = 1
  3: index = 0
  4: index = 1
  5: index = 0<CURSOR>
  6: 

*** End of source buffer ***


>>> Testing console command: say(['go previous', 'index', '=\\equals', '0'], user_input='None')
Heard go previous index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: index = 0<CURSOR>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(1)

*** Start of source buffer ***
  1: <CURSOR>index = 0
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: say(['select next', 'index', '=\\equals', '0'], user_input='None')
Heard select next index equals 0
*** Start of source buffer ***
  1: <SEL_START>index = 0<SEL_END>
  2: index = 1
  3: index = 0
  4: index = 1


>>> Testing console command: say(['select next', 'index', '=\\equals', '0'], user_input='None')
Heard select next index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <SEL_START>index = 0<SEL_END>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: goto_line(6)

  3: index = 0
  4: index = 1
  5: index = 0
  6: <CURSOR>

*** End of source buffer ***


>>> Testing console command: say(['select previous', 'index', '=\\equals', '0'], user_input='None')
Heard select previous index equals 0
  2: index = 1
  3: index = 0
  4: index = 1
  5: <SEL_START>index = 0<SEL_END>
  6: 

*** End of source buffer ***


>>> Testing console command: say(['select previous', 'index', '=\\equals', '0'], user_input='None')
Heard select previous index equals 0
*** Start of source buffer ***
  1: index = 0
  2: index = 1
  3: <SEL_START>index = 0<SEL_END>
  4: index = 1
  5: index = 0
  6: 

*** End of source buffer ***


>>> Testing console command: quit(save_speech_files=0, disconnect=0)



*******************************************************************************
* Name        : set_text
* Description : Testing set_text.
*******************************************************************************

Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
*** Start of source buffer ***
  1: <CURSOR># This is a small test buffer for Python
  2: 
  3: 
  4: 
*** Start of source buffer ***
  1: nothing left<CURSOR>

*** End of source buffer ***



-----------------------------------------------
Test suite completed in:  1333.14999998 secs
-----------------------------------------------
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'
Compiling symbols for file '%VCODE_HOME%\Config\py_std_sym.py'