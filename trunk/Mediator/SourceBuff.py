from Object import Object

class SourceBuff(Object):
    """Class representing a source buffer.

    This class implements methods for manipulating buffer containing
    source code in some programming language.
    
    **INSTANCE ATTRIBUTES**
    
    *STR file_name=None* -- Name of the source file loaded into buffer
    *STR language=None* -- Name of language of the source file
    *INT cur_pos=0* -- Cursor position (in number of chars) in the buffer
    *INT visible_start=None* -- Start position (in number of chars) of the visible portion of the source buffer
    *INT visible_end=None* -- End position (in number of chars) of the visible portion of the source buffer
    *STR content=None* -- Content of the source buffer

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, file_name=None, language=None, cur_pos=0, visible_start=None, visible_end=None, content=None, **attrs):
        Object.__init__(self)
        self.def_attrs({'file_name': None, 'language': None, 'cur_pos': 0, 'visible_start': None, 'visible_end': None, 'content': None})
        self.init_attrs(attrs)



    def is_language(self, lang):
        """Check if a source buffer is in a particular language.

        Outputs *true* if and only if *self* is displaying a file
        written in programming language *STR lang*.
        """
        return (self.language == lang)
