"""find a single changed region in a pair of strings
"""

# (C)2000 David C. Fox

def find_difference(old, new):
    """Finds the difference between old and new sequences, assuming that there
    is only one contiguous changed region.

    **INPUTS**

    *SEQ ANY* old -- old sequence

    *SEQ ANY* new -- new sequence
    
    **OUTPUTS**

    (start, end, change)
    
    *INT* start -- the offset into old of the range replaced or deleted

    *INT* end -- the offset into old of the item following 
    the range modified (or deleted) (this matches Python's slice convention).

    *ANY* change -- the replacement range from new
    """
#     print repr(old), repr(new)
    shorter = min(len(old), len(new))
    longer = max(len(old), len(new))
    for i in range(shorter):
	if old[i] != new[i]: break
    else:
# we reached the end of the shorter sequence
#  	print 'extra ', shorter, longer, repr(new[shorter:])
	return shorter, longer, new[shorter:]
# otherwise
#    print 'difference at ', i
    rest = shorter - i
    for j in range(rest):
	if old[-1-j] != new[-1-j]: break
#    print 'full', i, len(old) - j - 1, repr(new[i:-j-1])
    return i, len(old)-j-1, new[i:-j-1]
    
def find_string_difference(old, new):
    """Finds the difference between old and new strings, assuming that there
    is only one contiguous changed region.

    **INPUTS**

    *STR* old -- old string

    *STR* new -- new string
    
    **OUTPUTS**

    (start, end, change)
    
    *INT* start -- the offset into old of the range replaced or deleted

    *INT* end -- the offset into old of the character following 
    the range modified (or deleted) (this matches Python's slice convention).

    *STR* change -- the replacement string from new
    """
# note, this function is probably terribly slow for long strings.
# We may want to rewrite find_difference as an extension module in C
    return find_difference(old, new)
    
