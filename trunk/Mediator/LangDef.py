from Object import Object


class LangDef(Object):
    """Specifications for a given programming language.
    
    **INSTANCE ATTRIBUTES**
    
    *ANY name=None* -- name of the programming language
    
    *ANY regexp_symbol=None* -- a regepx that matches a valid symbol
    
    *ANY regexp_no_symbols=None* -- a regexp that matches portions of
     code that don't contain symbols (e.g. quoted strings, comments)
    

    CLASS ATTRIBUTES**
    
    *none* -- 
    """
    
    def __init__(self, name=None, regexp_symbol=None, regexp_no_symbols=None, **attrs):
        self.deep_construct(LangDef, \
                            {'name': name, \
                             'regexp_symbol': regexp_symbol, \
                             'regexp_no_symbols': regexp_no_symbols}, \
                            attrs, \
                            {})
