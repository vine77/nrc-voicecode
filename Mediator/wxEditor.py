"""interfaces for editor buffers with change notification"""

# (C)2000 David C. Fox


import debug
from Object import Object
from TextBuffer import *
from wxPython.wx import *

class TextBufferNotifyWX(TextBufferChangeNotify, VisibleBuffer):
    """TextBufferChangeNotify wrapper for wxTextCtrl
    
    **INSTANCE ATTRIBUTES**

    *wxTextCtrl* underlying -- underlying text control - a wxPython
    text control object

    *BOOL* program_initiated -- flag used internally to indicate to the
    whether the text changed event was due to a program-initiated change
    or to a user-initiated change.

    *BOOL* carriage_return_bug -- flag specifying whether the current
    version of wxPython requires a workaround for the carriage return
    bug.  (see comments below)

    **CLASS ATTRIBUTES**
    
    *none* --
    """
    def __init__(self, underlying_control, **args):
	"""wraps underlying wxPython wxTextCtrl

	**INPUTS**

	*wxTextCtrl* underlying_control -- underlying text control - a wxPython
	text control object
    
	**OUTPUTS**

	*none*
	"""
        self.deep_construct(TextBufferNotifyWX,
                            {'underlying':underlying_control,
			    'program_initiated':0,
			    'carriage_return_bug':1},
                            args)

	parent = self.underlying.GetParent()
	ID = self.underlying.GetId()
	EVT_TEXT(parent, ID, self._on_evt_text)
      
    def _on_evt_text(self, event):
	"""handler for wxEVT_COMMAND_TEXT_UPDATED.
	
	calls  TextBufferChangeNotify's _on_change
	"""
	self._on_change(self.program_initiated)
	
    def _external_position(self, internal):
	"""conversion from internal offset to external

	part of the workaround for the
	carriage return bug: text is returned with
	Windows carriage return/new line pairs replaced with simple new
	lines, but calls into wxTextCtrl which specify a character position
	offset use the actual internal buffer contents with \r\n.  Currently
	wxPython 2.2.1 on Windows has the bug.

	**INPUTS**

	*INT* internal -- offset into internal buffer with \r\n

	**OUTPUTS**

	*INT* --  corresponding offset into external buffer (as returned
	by get_text)
	"""

	if (internal == None): 
	    return None
	return internal -self.underlying.PositionToXY(internal)[1]
    def _internal_line(self, external):
	"""conversion from external offset to internal line number
	(first is 0)

	part of the workaround for the
	carriage return bug: text is returned with
	Windows carriage return/new line pairs replaced with simple new
	lines, but calls into wxTextCtrl which specify a character position
	offset use the actual internal buffer contents with \r\n.  Currently
	wxPython 2.2.1 on Windows has the bug.

	**INPUTS**

	*INT* external -- offset into external buffer, where \n ends
	lines.

	**OUTPUTS**

	*INT* --  line index into internal buffer
	"""

	lower_line = self.underlying.PositionToXY(external)[1]
	lines = self.underlying.GetNumberOfLines()
	upper_line = self.underlying.PositionToXY(external + lines - 1)[1]
	while upper_line -lower_line > 1:
	    middle = (lower_line + upper_line)/2
	    internal_trial = self.underlying.XYToPosition(0, middle)
	    external_trial = internal_trial - middle
	    if (external_trial > external):
		upper_line = middle
	    elif (external_trial < external):
		lower_line = middle
	    else:
		return middle
	if upper_line != lower_line:
	    internal_trial = self.underlying.XYToPosition(0, upper_line)
	    external_trial = internal_trial - upper_line
	    if (external_trial <= external):
		return upper_line
	return lower_line
    def _internal_position(self, external):
	"""conversion from external offset to internal

	part of the workaround for the
	carriage return bug: text is returned with
	Windows carriage return/new line pairs replaced with simple new
	lines, but calls into wxTextCtrl which specify a character position
	offset use the actual internal buffer contents with \r\n.  Currently
	wxPython 2.2.1 on Windows has the bug.

	**INPUTS**

	*INT* external -- offset into external buffer 
	(as returned by get_text) with \n indicating new line.

	**OUTPUTS**

	*INT* --  corresponding offset into internal buffer, where new
	lines end with \r\n
	"""
	if ( external == None):
	    return None
	line = self._internal_line(external)
	return external + line
    def range_defaults(self, start = None, end = None):
	"""translates from TextBuffer defaults for specifying start and
	end of a range to the appropriate values for wxTextCtrl
	
	**INPUTS**
	
	*INT* start -- internal offset of start of range, or None to
	default to the beginning of the buffer

	*INT* end -- internal offset of character following end of 
	range, or None to default to the end of the buffer

	**OUTPUTS**

	*(INT, INT)* -- internal offsets
	
	"""

# note: this uses internal positions
	if (start == None):
	  s = 0
	else:
	  s = start
	if (end == None):
	  e = self.underlying.GetLastPosition()
	else:
	  e = end
	return s, e

    def set_text(self, text, start = None, end = None):
	"""changes a portion of the buffer

	**INPUTS**

	*STR* text -- the new text.
	
	*INT* start -- the offset into the buffer of the text to the
	replaced.  Defaults to start of buffer.

	*INT* end -- the offset into the buffer of the character following 
	the text to be replaced (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*none* --
	"""
	if self.carriage_return_bug:
	    start = self._internal_position(start)
	    end = self._internal_position(end)
	s, e = self.range_defaults(start, end)
	self.program_initiated = 1
# this tries to use clipboard, for some unknown reason, and fails
#	self.underlying.Replace(s, e, text)
	if self.carriage_return_bug:
	    s = self._external_position(s)
	    e = self._external_position(e)
	self.set_selection(s, e)
	self.underlying.WriteText(text)
	self.program_initiated = 0


    def get_text(self, start = None, end = None):
	"""retrieves a portion of the buffer

	**INPUTS**

	*INT* start -- the start of the region returned.
	Defaults to start of buffer.

	*INT* end -- the offset into the buffer of the character following 
	the region to be returned (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

	*STR* -- contents of specified range of the buffer
	"""
	if self.carriage_return_bug:
	    start = self._external_position(start)
	    end = self._external_position(end)
	s, e = self.range_defaults(start, end)
	return self.underlying.GetValue()[s:e]

    def get_selection(self):
	"""retrieves range of current selection

	**INPUTS**

	*none* --
	
	**OUTPUTS**

	*INT* (start, end) -- start is the offset into the buffer of 
	the start of the current
	selection.  end is the offset into the buffer of the character 
	following the selection (this matches Python's slice convention).
	"""
	s, e = self.underlying.GetSelection()
	if self.carriage_return_bug:
	    s = self._external_position(s)
	    e = self._external_position(e)
	return s, e

    def set_selection(self, start = None, end = None):
	"""changes range of current selection

	**INPUTS**

	*INT* start -- the start of the region to be selected.
	Defaults to start of buffer.

	*INT* end -- the offset into the buffer of the character following 
	the region to be selected (this matches Python's slice convention).
	Defaults to end of buffer.

	**OUTPUTS**

        *none* --
	"""
	# wxTextCtrl doesn't actually trigger a change notification (EVT_TEXT)
	# on selection changes, but just in case we switch to a
	# different underlying buffer which does,
	# we should set program_initiated before setting the
	# selection, and clear it afterwards
	if self.carriage_return_bug:
	    start = self._internal_position(start)
	    end = self._internal_position(end)
	s, e = self.range_defaults(start, end)
	self.program_initiated = 1
	self.underlying.SetSelection(s, e)
	self.program_initiated = 0

    def get_visible(self):
	""" get start and end offsets of the currently visible region of
	the buffer.  End is the offset of the first character not
	visible (matching Python's slice convention)

	**INPUTS**

	*none* --

	**OUTPUTS**

	*INT* (start, end) -- visible range
	"""
# check this
	width, height = self.underlying.GetClientSizeTuple()
	char_height = self.underlying.GetCharHeight()
	starting_line = self.underlying.GetScrollPos(wxVERTICAL)
	lines = self.underlying.GetNumberOfLines()
	ending_line = min(starting_line + height/char_height, lines)
	ending_x = self.underlying.GetLineLength(ending_line)
	start = self.underlying.PositionToXY(starting_line,0)
	end = self.underlying.PositionToXY(ending_line, ending_x)
	if self.carriage_return_bug:
	    start = self._external_position(start)
	    end = self._external_position(end)
	return start, end
	

class TextBufferSpecifyWX(TextBufferSpecifyFromNotify):
    """TextBufferChangeSpecify wrapper for wxTextCtrl
    **INSTANCE ATTRIBUTES**

    *none*

    **CLASS ATTRIBUTES**
    
    *none* --
    """
    def __init__(self, underlying_control, **args):
	"""wraps underlying wxPython wxTextCtrl

	**INPUTS**

	*TextBufferNotifyWX* underlying_control -- underlying text control
    
	**OUTPUTS**

	*none*
	"""
        self.deep_construct(TextBufferSpecifyWX, {},
                            args, 
                            new_default = \
			    {'change_notification':underlying_control})
#	print self.change_notification


