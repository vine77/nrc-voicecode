"""interfaces for editor buffers with change notification"""

# (C)2000 David C. Fox


import debug
import find_difference
from Object import Object

class TextBuffer(Object):
    """abstract class defining basic text buffer interface.

    **INSTANCE ATTRIBUTES**

    *none*
    
    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
	"""abstract base class - no arguments
	
	**INPUTS**
	
	*none*
	"""
        self.deep_construct(TextBuffer,
                            {},
                            args)

    def set_text(self, text, start = None, end = None):
	"""changes a portion of the buffer

	**INPUTS**

	*STR text* is the new text.
	
	*INT start* is the offset into the buffer of the text to the
	replaced.  Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the text to be replaced (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*none*
	"""
	pass

    def get_text(self, start = None, end = None):
	"""retrieves a portion of the buffer

	**INPUTS**

	*INT start* is the start of the region returned.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""
	pass

    def get_selection(self):
	"""retrieves range of current selection

	**INPUTS**

	*none*
	
	**OUTPUTS**

	*INT* (start, end)

	start is the offset into the buffer of the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""
	pass

    def set_selection(self, start = None, end = None):
	"""changes range of current selection

	**INPUTS**

	*INT start* is the start of the region to be selected.
	Defaults to start of buffer.

	*INT end* is the offset into the buffer of the character following 
	the region to be selected (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

        *none*
	"""
	pass

class SpeechBuffer:
    """abstract base class describing additional interfaces for a
    (hidden) speech buffers, used to keep track of dictated text and
    context.

    Note: Generally, a concrete class will inherit from TextBuffer (or a
    subclass) and often, either VisibleBuffer or SpeechBuffer.  
    SpeechBuffer does not inherit from TextBuffer so as to simplify
    such mix-and-match multiple inheritance.

    **INSTANCE ATTRIBUTES**

    *none*
    
    **CLASS ATTRIBUTES**
    
    *none*
    """
    def __init__(self, **args):
        self.deep_construct(SpeechBuffer,
                            {},
			    args)

    def set_lock(self, state):
	"""locks/unlocks changes to the contents of a hidden speech 
	buffer, to ensure consistency between multiple get operations.
	When the buffer is
	locked, all speech-initiated changes to the buffer will be 
	deferred until it is unlocked.  No speech should be lost.
	
	**INPUTS**

	*INT* state

	**OUTPUTS**

	*none*
	"""
	pass
    
class VisibleBuffer:
    """abstract base class describing additional interfaces for visible
    text buffers.

    Note: Generally, a concrete class will inherit from TextBuffer (or a
    subclass) and often, either VisibleBuffer or SpeechBuffer.  
    VisibleBuffer does not inherit from TextBuffer so as to simplify
    such mix-and-match multiple inheritance.

    **INSTANCE ATTRIBUTES**

    *none*
    
    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, **args):
        self.deep_construct(VisibleBuffer,
                            {},
			    args)
	

    def get_visible(self):
	""" get start and end offsets of the currently visible region of
	the buffer.  End is the offset of the first character not
	visible (matching Python's slice convention)

	**INPUTS**

	*none*

	**OUTPUTS**

	*INT* (start, end)
	"""
	pass

    def make_position_visible(self, position = None):
	"""scroll buffer (if necessary) so that  the specified position
	is visible.  Position defaults to the current cursor position.
	Note: if a particular subclass of VisibleBuffer cannot support
	this method, it should just leave it as a no-op.

	**INPUTS**

	*INT* position

	**OUTPUTS**

	*none*
	"""
	pass

    def refresh(self):
	"""force a refresh of the buffer.
	Note: if a particular subclass of VisibleBuffer cannot support
	this method, it should just leave it as a no-op.

	**INPUTS**

	*none*

	**OUTPUTS**

	*none*
	"""
	pass

class TextBufferChangeNotify(TextBuffer):
    """abstract class wrapper for text buffers with change notification,
    but not change specification (tell you when something changed, but
    not what).  Both Windows CEdit controls and wxWindows TextCtrl's share
    this stupid characteristic.  However, we can convert such a buffer
    into a more civilized form by wrapping it in a TextBufferChangeNotify, 
    and then passing it to TextBufferSpecifyFromNotify.

    Note: TextBufferChangeNotify provides the infrastructure for change
    notification, but a concrete subclass of TextBufferChangeNotify is
    responsible for calling TextBufferChangeNotify._on_change with the
    proper value of the program_initiated flag to
    initiate the processing of the change event, for both user- and
    program-initiated changes.  See TextBufferWX for an example of Hal
    how to do this.

    **INSTANCE ATTRIBUTES**

    *FCT* notification_callback --
      notification_callback( *TextBufferChangeNotify* buffer,
    *BOOL* program_initiated).
    function to be called on change to
    the underlying buffer.   program_initiated will be true if the change
    came from the program (through set_text).
    The only other argument passed will be a reference to this buffer,
    so if the callback function wants to know what changed,
    it will have to call other methods of
    TextBufferChangeNotify (or its parent classes).
    Note that the notification callback will be called on ANY change
    to the buffer, whether initiated by the user or by a caller to a
    buffer method, so no changes should be made during the callback.

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, notification_callback=None, **args):
	"""

	**INPUTS**

	*FCT* notification_callback --
	  notification_callback( *TextBufferChangeNotify* buffer,
	*BOOL* user_initiated) 
	see TextBufferChangeNotify documentation for details.
	"""
    
        self.deep_construct(TextBufferChangeNotify,
                            {'notification_callback':notification_callback}, 
			    args)

    def set_change_notification_callback(self, notification_callback = None):
	"""changes the callback to a new function

	**INPUTS**

	*FCT* notification_callback --
	notification_callback( *TextBufferChangeNotify* buffer,
	*BOOL* program_initiated)
	function to be called on change to
	the underlying buffer.  
	see TextBufferChangeNotify documentation for details.

	**OUTPUTS**

	*none*
	"""
	self.notification_callback = notification_callback

    def _on_change(self, program_initiated):
	"""internal function which triggers the
	notification_callback.  Only the concrete subclass of
	TextBufferChangeNotify implementing the change notification 
	should call this function"""
	if self.notification_callback:
	    self.notification_callback(self, program_initiated)
	    # note: notification_callback is an attribute of 
	    # TextBufferChangeNotify, which is a function, not a method of
	    # TextBufferChangeNotify.  This looks a bit funny (like a
	    # method being called with a duplicate self argument) but it
	    # is actually correct.

class TextBufferChangeSpecify(TextBuffer):
    """abstract class defining an interface for text buffers with 
    change specification (i.e. they tell you what changed).
    VDct/CDgnDictCustom meet this criterion.
    TextBufferSpecifyFromNotify below will provide a TextBufferChangeSpecify 
    wrapper for a TextBufferChangeNotify class.

    **INSTANCE ATTRIBUTES**

    *FCT* change_callback --
      change_callback( *INT* start, *INT* end, *STR* text, 
      *INT* selection_start, *INT* selection_end, 
      *TextBufferChangeSpecify* buffer, *BOOL* program_initiated) 
    function to be called on change to
    the underlying buffer.  
    Note that the change callback will be called on ANY change
    to the buffer, whether initiated by the user or by a caller to a
    buffer method, so no changes should be made during the callback.

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, change_callback=None, **args):
	"""

	**INPUTS**

	*FCT* change_callback --
	change_callback( *INT* start, *INT* end, *STR* text, 
	*INT* selection_start,
	*INT* selection_end, TextBufferChangeSpecify buffer,
	*BOOL* program_initiated) 
	see TextBufferChangeSpecify documentation for details.
	"""
    
        self.deep_construct(TextBufferChangeSpecify,
                            {'change_callback':change_callback}, args)

    def set_change_callback(self, change_callback = None):
	"""changes the callback to a new function

	**INPUTS**
	*FCT* change_callback --
	change_callback( *INT* start, *INT* end, *STR* text, 
	*INT* selection_start, *INT* selection_end, 
	*TextBufferChangeSpecify* buffer, *BOOL* program_initiated) 
	see TextBufferChangeSpecify documentation for details.
	-- function to be called on change to
	the underlying buffer.  
	see TextBufferChangeSpecify documentation for details.

	**OUTPUTS**

	*none*
	"""
	self.change_callback = change_callback

    def _on_change_specification(self, start, end, text,
	selection_start, selection_end, program_initiated):
	"""internal function which triggers the
	change_callback.  Only the concrete subclass of 
	TextBufferChangeSpecify implementing change specification
	should call this function"""
#	print 'hi there'
#	print repr(self.change_callback)
	if self.change_callback:
	    self.change_callback(start, end, text, selection_start, 
		selection_end, self, program_initiated)
	    # note: change_callback is an attribute of 
	    # TextBufferChangeSpecify, which is a function, not a method of
	    # TextBufferChangeSpecify.  This looks a bit funny (like a
	    # method being called with a duplicate self argument) but it
	    # is actually correct.

class TextBufferSpecifyFromNotify(TextBufferChangeSpecify):
    """creates a TextBufferChangeSpecify given an underlying
    TextBufferChangeNotify

    note: TextBufferSpecifyFromNotify uses the __getattr__ method to
    delegate unknown attributes and methods to the underlying
    TextBufferChangeNotify.  Thus, if a specific subclass of
    TextBufferChangeNotify has additional attributes or methods, they
    will be visible through the containing TextBufferSpecifyFromNotify.
    However, since TextBufferChangeSpecify inherits from TextBuffer, any
    attributes added to TextBuffer will not be unknown, and will not be
    automatically delegated.  Like get_text, set_text, etc.,
    corresponding methods must be added manually to
    TextBufferSpecifyFromNotify to ensure that it will properly support
    these new attributes.

    TextBufferSpecifyFromNotify intercepts and disables the 
    set_change_notification_callback method, since it needs to receive
    the change notification callbacks itself.

    **INSTANCE ATTRIBUTES**

    *TextBufferChangeNotify* underlying - underlying change notification
    TextBuffer

    **CLASS ATTRIBUTES**
    
    *none*
    """

    def __init__(self, change_notification, **args):
	"""

	**INPUTS**

	*TextBufferChangeNotify* change_notification
	 - underlying buffer to provide change notification and rest of
	   services

	[Inherited from TextBufferChangeSpecify: 

	*FCT* change_callback --
	change_callback( *INT* start, *INT* end, *STR* text, 
	*INT* selection_start, *INT* selection_end, 
	*TextBufferChangeSpecify* buffer, *BOOL* program_initiated) 

	see TextBufferChangeSpecify documentation for details.]
	"""
    
        self.deep_construct(TextBufferSpecifyFromNotify,
                            {'change_notification':change_notification,
			    'contents': change_notification.get_text()},
			    args)

	self.change_notification.set_change_notification_callback(
	    self._on_change_translator)
    
    def _on_change_translator(self, internal, program_initiated):
	"""private method which handles change notification callbacks
	from the underlying TextBufferChangeNotify object and translates
	to change specification callbacks.  Should not be called
	manually."""

	contents = self.change_notification.get_text()
	if self.change_callback:
	    start, end, text = \
	        find_difference.find_string_difference(self.contents, contents)
#	    text = self.contents[start: end]
	    selection_start, selection_end = \
	        self.change_notification.get_selection()
#	    start, end, text = 0, 0, ""
	    self._on_change_specification(start, end, text,
		selection_start, selection_end, program_initiated)
	self.contents = contents

    def __getattr__(self, name):
	"""delegates unknown attributes (including methods) to the underlying
	TextBufferChangeNotify object"""
	return getattr(self.change_notification, name)

# no-op versions of these functions are defined in TextBuffer, so
# __getattr__ will not automatically delegate them to the underlying
# TextBufferChangeNotify

    def set_text(self, text, start = None, end = None):
	"""changes a portion of the buffer - see TextBuffer"""
	return self.change_notification.set_text(text, start, end)

    def get_text(self, start = None, end = None):
	"""retrieves a portion of the buffer
	- see TextBuffer"""
	return self.change_notification.get_text(start, end)

    def get_selection(self):
	"""retrieves range of current selection
	- see TextBuffer"""
	return self.change_notification.get_selection()

    def set_selection(self, start = None, end = None):
	"""changes range of current selection
	- see TextBuffer"""
	return self.change_notification.set_selection(start, end)

# this WOULD be delegated automatically, but we don't want it to.
# TextBufferSpecifyFromNotify is a TextBufferChangeSpecify object, not a
# TextBufferChangeNotify object, so it shouldn't have a
# set_change_notification_callback method.
    def set_change_notification_callback(self, callback):
	raise AttributeError("'%s' object has no attribute '%s'" % \
	(self.__class__.__name__, 'set_change_notification_callback'))
    
