import re

from Object import Object

file_language = {'c': 'C', 'h': 'C', 'py': 'python'}

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
    *INT selection_start=None* -- Start position (in number of chars) of the current selection
    *INT selection_end=None* -- End position (in number of chars) of the current selection
    *STR content=None* -- Content of the source buffer

    CLASS ATTRIBUTES**
    
    *{STR: STR}* file_language -- key is a standard file extension and
    value is the programming language associated with that extension
    """
    
    def __init__(self, file_name=None, language=None, cur_pos=0, visible_start=0, visible_end=0, selection_start=0, selection_end=0, content=None, **attrs):
        self.deep_construct(SourceBuff,
                            {'file_name': file_name, \
                             'language': language, \
                             'cur_pos': cur_pos, \
                             'visible_start': visible_start, \
                             'visible_end': visible_end, \
                             'selection_start': selection_start, \
                             'selection_end': selection_end, \
                             'content': content}, \
                            attrs \
                            )


        #
        # Set the language name if it hasn't been set already
        #
        if self.language == None and self.file_name != None:
            self.language = self.language_name(file_name)
            


    #
    # Note: this method can be called even if *self* is not an actual
    #       class.
    #
    def language_name(self, file_name):
        """Returns the name of the language a file is written in
        
        **INPUTS**
        
        *STR* file_name -- name of the file 
        

        **OUTPUTS**

        *STR* -- the name of the language
        """
        global file_language

        language = None
        if file_name != None:
            a_match = re.match('^.*?\.([^\.]*)$', file_name)
            extension = a_match.group(1)
            if file_language.has_key(extension):
                language =  file_language[extension]
        return language


    def is_language(self, lang):
        """Check if a source buffer is in a particular language.

        Outputs *true* if and only if *self* is displaying a file
        written in programming language *STR lang*.
        """
        return (self.language == lang)
