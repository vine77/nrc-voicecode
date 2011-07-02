# demo file generated with mediator test of PythonAcceptanceTest
#
utt1 = "define class some variable class body"
exp1 = \
"""class SomeVariable:
    <CURSOR>"""

utt2 = "define method some method add arguments"
exp2 = "<<1 line>>    def some_method(self, <CURSOR>):"

utt3 = "collect arguments positional arguments comma"
exp3 = "<<1 line>>    def some_method(self, *positional_arguments, <CURSOR>):"

utt4 = "collect keyword arguments keyword arguments"
exp4 = "<<1 line>>    def some_method(self, *positional_arguments, **keyword_arguments<CURSOR>):"

utt5 = "class body"
exp5 = \
"""<<1 line>>
    def some_method(self, *positional_arguments, **keyword_arguments):
        <CURSOR>"""

utt6 = "some array equals some other array sliced at one colon five new statement"
exp6 = \
"""<<2 lines>>
        some_array = some_other_array[1: 5]
        <CURSOR>"""

utt7 = "some dictionary item with key zero jump out equals one"
exp7 = "<<3 lines>>        some_dictionary[0] = 1<CURSOR>"

utt8 = "comment above"
exp8 = \
"""<<3 lines>>
        # <CURSOR>
        some_dictionary[0] = 1"""

utt9 = "this is a commented out"
exp9 = \
"""<<3 lines>>
        # this_is_a_commented_out<CURSOR>
        some_dictionary[0] = 1"""
