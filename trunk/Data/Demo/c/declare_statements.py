# demo file generated with mediator test of CAcceptanceTest
#
utt1 = "['declare','function','test','procedure']"
exp1 = "test_procedure<CURSOR>();"

utt2 = "['add','argument','integer','count']"
exp2 = "test_procedure(int count<CURSOR>);"

utt3 = "[',\comma','float','divisor']"
exp3 = "test_procedure(int count, float divisor<CURSOR>);"

utt4 = "['returning','void']"
exp4 = "void <CURSOR>test_procedure(int count, float divisor);"

utt5 = "['new','statement']"
exp5 = "void test_procedure(int count, float divisor);<CURSOR>;"

utt6 = "['declare','char','hello']"
exp6 = "void test_procedure(int count, float divisor);char hello<CURSOR>;"

utt7 = "['new','statement']"
exp7 = \
"""void test_procedure(int count, float divisor);char hello;
<CURSOR>;"""

utt8 = "['int\int','count']"
exp8 = "<<1 line>>int count<CURSOR>;"

utt9 = "['new','statement','integer','pointer','testing','pointers']"
exp9 = \
"""<<1 line>>
int count;
int * testing_pointers<CURSOR>;"""

utt10 = "['comma','pointer','testing','other','pointers']"
exp10 = "<<2 lines>>int * testing_pointers, * testing_other_pointers<CURSOR>;"

utt11 = "['new','statement','declare','the','value','of','type','double']"
exp11 = \
"""<<2 lines>>
int * testing_pointers, * testing_other_pointers;
double <CURSOR>the_value;"""

utt12 = "['new','statement','declare','some','variable','of','type','static','int\int']"
exp12 = "<<3 lines>>double int <CURSOR>the_value;"

utt13 = "['new','statement','declare','char','star','star','string','address']"
exp13 = \
"""<<3 lines>>
double int the_value;
char **string_address<CURSOR>;"""

utt14 = "['after','semi']"
exp14 = "<<4 lines>>char **string_address;<CURSOR>"

utt15 = "['new','paragraph']"
exp15 = \
"""<<4 lines>>
char **string_address;

<CURSOR>"""

utt16 = "['declare','function','foo', 'two']"
exp16 = "<<6 lines>>foo2<CURSOR>();"

utt17 = "['returning','some','pointer']"
exp17 = "<<6 lines>>some* <CURSOR>foo2();"

utt18 = "['add','argument','integer','counter','comma','sum','of','type','int\int']"
exp18 = "<<6 lines>>some* int <CURSOR>foo2();"

utt19 = "['after','semi']"
exp19 = "<<6 lines>>some* int foo2();<CURSOR>"

utt20 = "['new','paragraph']"
exp20 = \
"""<<6 lines>>
some* int foo2();

<CURSOR>"""

utt21 = "['declare','method','bar','scope','operator','fabulous','method','returning','char','star']"
exp21 = "<<8 lines>>char *<CURSOR>bar::fabulous_method();"

utt22 = "['add','argument','integer','pointer','another','memory','address']"
exp22 = "<<8 lines>>char *bar::fabulous_method(int * another_memory_address<CURSOR>);"

utt23 = "['after','semi','new','paragraph']"
exp23 = \
"""<<8 lines>>
char *bar::fabulous_method(int * another_memory_address);

<CURSOR>"""

utt24 = "['define','function','foo','returning','some','pointer']"
exp24 = \
"""<<10 lines>>
some* <CURSOR>foo()
{

}"""

utt25 = "['add','argument','integer','counter','comma','sum','of','type','int\int']"
exp25 = \
"""<<10 lines>>
some* int <CURSOR>foo()
{

}"""

utt26 = "['jump','out','jump','out','new','paragraph']"
exp26 = \
"""<<10 lines>>
some* int foo()
{

}

<CURSOR>"""

utt27 = "['define','method','foo','scope','bar','returning','pointer','to','char']"
exp27 = \
"""<<15 lines>>
char <CURSOR>*foo::bar()
{

}"""

utt28 = "['method','body']"
exp28 = \
"""<<15 lines>>
char *foo::bar()
{

<CURSOR>}"""

utt29 = "['for','loop']"
exp29 = \
"""<<18 lines>>
  for (<CURSOR>; ; )
    {

    }
}"""

utt30 = "['integer','index','equals','0\zero']"
exp30 = \
"""<<18 lines>>
  for (0<CURSOR>; ; )
    {

    }
}"""

utt31 = "['after','semi','index']"
exp31 = \
"""<<18 lines>>
  for (0; index<CURSOR>; )
    {

    }
}"""

utt32 = "['is','less','or','equal','to']"
exp32 = \
"""<<18 lines>>
  for (0; index <= <CURSOR>; )
    {

    }
}"""

utt33 = "['platypus','count']"
exp33 = \
"""<<18 lines>>
  for (0; index <= platypus_count<CURSOR>; )
    {

    }
}"""

utt34 = "['after','semi','index','increment']"
exp34 = \
"""<<18 lines>>
  for (0; index <= platypus_count; index++<CURSOR>)
    {

    }
}"""

utt35 = "['loop','body']"
exp35 = \
"""<<18 lines>>
  for (0; index <= platypus_count; index++)
    {
<CURSOR>
    }
}"""
