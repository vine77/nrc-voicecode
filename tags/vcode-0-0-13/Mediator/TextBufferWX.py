"""interfaces for editor buffers with change notification"""

# (C)2000 David C. Fox


import debug
from Object import Object
from TextBuffer import *
from wxPython.wx import *

class TextBufferWX(TextBufferChangeSpecify, VisibleBuffer):
    """TextBufferChangeSpecify wrapper for wxTextCtrl
    
    **INSTANCE ATTRIBUTES**

    *wxTextCtrl* underlying -- underlying text control - a wxPython
    text control object

    *BOOL* program_initiated -- flag used internally to indicate to the
    whether the text changed event was due to a program-initiated change
    or to a user-initiated change.

    *BOOL* carriage_return_bug -- flag specifying whether the current
    version of wxPython requires a workaround for the carriage return
    bug.  (see comments below)

    *STR* crnl -- rep of CR-NL pair in underlying buffer
    *STR* nl -- rep of new line externally and in contents
    *INT* delta_width -- difference in lengths of crnl and nl
    *STR* contents_internal -- copy of contents of the buffer, with CR-LF
    *STR* contents_external -- copy of contents of the buffer, with only NL



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
        self.deep_construct(TextBufferWX,
                            {'underlying':underlying_control,
			    'program_initiated':0,
			    'contents_external': underlying_control.GetValue(),
			    'contents_internal': '',
			    'carriage_return_bug':1,
			    'nl': '\n',
			    'crnl': '\015\n',
			    'delta_width': 0},
                            args)

	if not self.carriage_return_bug:
	    self.crnl = self.nl
	self.delta_width = len(self.crnl) - len(self.nl)
	self.contents_internal = string.replace(self.contents_external,
	    self.nl, self.crnl)
	parent = self.underlying.GetParent()
	ID = self.underlying.GetId()
	EVT_TEXT(parent, ID, self._on_evt_text)
      
    def _on_evt_text(self, event):
	"""handler for wxEVT_COMMAND_TEXT_UPDATED.
	
	"""
# program initiated calls originate from set_text, which handles
# updating self.contents_external and internal, and calling
# _on_change_specification
#	print '_on_evt_text', self.program_initiated
	if not self.program_initiated:
	    contents = self.underlying.GetValue()
	    start, end, text = \
	        find_difference.find_string_difference(self.contents_external, 
		contents)
	    self.contents_external = contents
	    self.contents_internal = \
	        string.replace(contents, self.nl, self.crnl)
	    selection_start, selection_end = self.get_selection()
	    self._on_change_specification(start, end, text,
		selection_start, selection_end, self.program_initiated)


    def range_defaults(self, start = None, end = None):
	"""translates from TextBuffer defaults for specifying start and
	end of a range to the appropriate values for wxTextCtrl (except
	that we use external offsets here)
	
	**INPUTS**
	
	*INT* start -- external offset of start of range, or None to
	default to the beginning of the buffer

	*INT* end -- external offset of character following end of 
	range, or None to default to the end of the buffer

	**OUTPUTS**

	*(INT, INT)* -- external offsets
	
	"""

# note: this uses internal positions
	if (start == None):
	  s = 0
	else:
	  s = start
	if (end == None):
	  e = len(self.contents_external)
	else:
	  e = end
	return s, e

    def line_range_internal(self, start, end):
	"""find line numbers of a range of internal positions within
	contents_internal

	**INPUTS**

	*INT* start -- character offset into contents_internal of start of range
	*INT* end  -- character offset into contents_internal of end of range

	**OUTPUTS**

	*(INT, INT)* -- corresponding range of line numbers
	"""
	before = string.split(self.contents_internal[0:start], self.crnl)
#	print before
	first = len(before) - 1
	range = self.contents_internal[start:end]
	n = len(string.split(range, self.crnl)) -1
	second = first + n
#	print first, second
	return first, second

    
    def line_range_external(self, start, end):
	"""find line numbers of a range of external positions within
	contents_external

	**INPUTS**

	*INT* start -- character offset into contents_external of start of range
	*INT* end  -- character offset into contents_external of end of range

	**OUTPUTS**

	*(INT, INT)* -- corresponding range of line numbers
	"""
	first = len(string.split(self.contents_external[0:start], self.nl)) -1
	range = self.contents_external[start:end]
	n = len(string.split(range, self.nl)) -1
	second = first + n
	return first, second

    def external_to_internal(self, start, end):
	"""converts a range of external positions (NL only) to
	internal positions (in the underlying
	buffer which uses CR-LF)

	**INPUTS**

	*INT* start -- start of range (external)
	*INT* end -- end of range (external)

	**OUTPUTS**

	*(INT, INT)* -- corresponding character range 
	internally, using CR-LF
	"""
	lines = self.line_range_external(start, end)
	s = start +lines[0]*self.delta_width
	e = end +lines[1]*self.delta_width
	return s, e

    def internal_to_external(self, start, end):
	"""converts a range of internal positions (in the underlying
	buffer which uses CR-LF) to external positions (NL only)

	**INPUTS**

	*INT* start -- start of range (internal)
	*INT* end -- end of range (internal)

	**OUTPUTS**

	*(INT, INT)* -- corresponding character range 
	externally, assuming only newlines
	"""
	lines = self.line_range_internal(start, end)
	s = start -lines[0]*self.delta_width
	e = end -lines[1]*self.delta_width
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
# store initial value of flag
	program_initiated = self.program_initiated
	s, e = self.range_defaults(start, end)
	before = self.contents_external[0:s]
	after = self.contents_external[e:]
	st, en = self.external_to_internal(s, e)
	self.contents_external = before + text + after
#	print 'TBNwx.set_text ', s, e, text
	before_internal = self.contents_internal[0:st]
	after_internal = self.contents_internal[en:]
	t = string.replace(text, self.nl, self.crnl)
	self.contents_internal = before_internal + t + after_internal
	self.program_initiated = 1
	self.set_selection(s, e)
	self.underlying.WriteText(text)
	selection_start, selection_end = self.get_selection()
	self._on_change_specification(s, e, text, selection_start,
	    selection_end, self.program_initiated)
# restore flag to initial value	
	self.program_initiated = program_initiated
#	if self.carriage_return_bug:
#	    s, e = self._internal_range(s, e)
#	self.program_initiated = 1
# this tries to use clipboard, for some unknown reason, and fails
#	self.underlying.Replace(s, e, text)

    def get_length(self):
	return len(self.contents_external)

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
	s, e = self.range_defaults(start, end)
	return self.contents_external[s:e]

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
#	print s, e
	if self.carriage_return_bug:
	    s, e = self.internal_to_external(s, e)
#	print 'external ',s,e
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
	program_initiated = self.program_initiated
	s, e = self.range_defaults(start, end)
#	print 'TBNwx.set_selection', s, e
	if self.carriage_return_bug:
	    s, e = self.external_to_internal(s, e)
	self.program_initiated = 1
	self.underlying.SetSelection(s, e)
	self.program_initiated = program_initiated

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
	start = self.underlying.XYToPosition(0, starting_line)
	lines = self.underlying.GetNumberOfLines()
#	print 'heights', height, char_height
	ending_line = starting_line + height/char_height - 1
# if ending line of window goes beyond end of buffer, retrace steps
#	print 'visible'
	while self.underlying.XYToPosition(0, ending_line) == -1:
	    ending_line = ending_line -1
#	print 'line: ', ending_line, lines - 1
	if ending_line + 1 <= lines - 1:
	    end = self.underlying.XYToPosition(-1, ending_line+1)
	else:
	    end = self.underlying.GetLastPosition()
#	print end
	ending_x, ending_y = self.underlying.PositionToXY(end)
#	print starting_line, ending_line, ending_x
	if self.carriage_return_bug:
	    start, end = self.internal_to_external(start, end)
#	print start, end
	return start, end
	