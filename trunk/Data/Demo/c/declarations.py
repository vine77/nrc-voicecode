# demo file generated with mediator test of CAcceptanceTest
#
utt1 = "declare function test procedure"
exp1 = "test_procedure<CURSOR>();"

utt2 = "add argument integer count"
exp2 = "test_procedure(int count<CURSOR>);"

utt3 = "comma float divisor"
exp3 = "test_procedure(int count, float divisor<CURSOR>);"

utt4 = "returning void"
exp4 = "void <CURSOR>test_procedure(int count, float divisor);"

utt5 = "new statement"
exp5 = "void test_procedure(int count, float divisor);<CURSOR>;"

utt6 = "declare char hello"
exp6 = "void test_procedure(int count, float divisor);care_hello<CURSOR>;"

utt7 = "new statement"
exp7 = \
"""void test_procedure(int count, float divisor);care_hello;
<CURSOR>;"""

utt8 = "int count"
exp8 = "<<1 line>>int count<CURSOR>;"

utt9 = "new statement integer pointer testing pointers"
exp9 = \
"""<<1 line>>
int count;
int * testing_pointers<CURSOR>;"""

utt10 = "comma pointer testing other pointers"
exp10 = "<<2 lines>>int * testing_pointers, * testing_other_pointers<CURSOR>;"

utt11 = "new statement declare the value of type double"
exp11 = \
"""<<2 lines>>
int * testing_pointers, * testing_other_pointers;
double <CURSOR>the_value;"""

utt12 = "new statement declare some variable of type static int"
exp12 = \
"""<<3 lines>>
double the_value;
static int <CURSOR>some_variable;"""

utt13 = "new statement declare char star star string address"
exp13 = \
"""<<4 lines>>
static int some_variable;
char **string_address<CURSOR>;"""

utt14 = "after semi"
exp14 = "<<5 lines>>char **string_address;<CURSOR>"

utt15 = "new paragraph"
exp15 = \
"""<<5 lines>>
char **string_address;

<CURSOR>"""

utt16 = "declare function foo"
exp16 = "<<7 lines>>foo<CURSOR>();"

utt17 = "returning some pointer"
exp17 = "<<7 lines>>some* <CURSOR>foo();"

utt18 = "add argument integer counter comma sum of type int"
exp18 = "<<7 lines>>some* foo(int counter, int <CURSOR>sum);"

utt19 = "after semi"
exp19 = "<<7 lines>>some* foo(int counter, int sum);<CURSOR>"

utt20 = "new paragraph"
exp20 = \
"""<<7 lines>>
some* foo(int counter, int sum);

<CURSOR>"""

utt21 = "declare method bar scope operator fabulous method returning char star"
exp21 = "<<9 lines>>char *<CURSOR>bar::fabulous_method();"

utt22 = "add argument integer pointer another memory address"
exp22 = "<<9 lines>>char *bar::fabulous_method(int * another_memory_address<CURSOR>);"

utt23 = "after semi new paragraph"
exp23 = \
"""<<9 lines>>
char *bar::fabulous_method(int * another_memory_address);

<CURSOR>"""

utt24 = "define function foo returning some pointer"
exp24 = \
"""<<11 lines>>
some* <CURSOR>foo()
{

}"""

utt25 = "add argument integer counter comma sum of type int"
exp25 = \
"""<<11 lines>>
some* foo(int counter, int <CURSOR>sum)
{

}"""

utt26 = "jump out jump out new paragraph"
exp26 = \
"""<<11 lines>>
some* foo(int counter, int sum)
{

}

<CURSOR>"""

utt27 = "define method foo scope bar returning pointer to char"
exp27 = \
"""<<16 lines>>
char <CURSOR>*foo::bar()
{

}"""

utt28 = "method body"
exp28 = \
"""<<16 lines>>
char *foo::bar()
{

<CURSOR>}"""

utt29 = "for loop"
exp29 = \
"""<<19 lines>>
  for (<CURSOR>; ; )
    {

    }
}"""

utt30 = "integer index equals zero"
exp30 = \
"""<<19 lines>>
  for (int index=0<CURSOR>; ; )
    {

    }
}"""

utt31 = "after semi index"
exp31 = \
"""<<19 lines>>
  for (int index=0; index<CURSOR>; )
    {

    }
}"""

utt32 = "is less or equal to"
exp32 = \
"""<<19 lines>>
  for (int index=0; index <= <CURSOR>; )
    {

    }
}"""

utt33 = "platypus count"
exp33 = \
"""<<19 lines>>
  for (int index=0; index <= platypus_count<CURSOR>; )
    {

    }
}"""

utt34 = "after semi index increment"
exp34 = \
"""<<19 lines>>
  for (int index=0; index <= platypus_count; index++<CURSOR>)
    {

    }
}"""

utt35 = "loop body"
exp35 = \
"""<<19 lines>>
  for (int index=0; index <= platypus_count; index++)
    {
<CURSOR>
    }
}"""
