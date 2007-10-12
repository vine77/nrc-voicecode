a""" This test file has lots of pieces that can be selected by
select ABC through XYZ.

Test the possibilities of extending the range of found ranges by natlink/NatSpeak
with the voicecoder function extend_ranges

"""

# words to recognise: function one, function-one, function-1, function 1.


class Lots(object):
   def __init__(self, a, b):
      self.a = ((x, ), (x, b), (b, ))
      self.b = ((b, ), (b, x), (x, ))
   def function1(self):
      return self.x() + self.b()
   def function2(self):
      return self.x(x,b)  * self.b(x,b)

def _run(self, c, d):
   x = Lots(1, 2)
   y = Lots(1, 2)
   z = Lots(1, 2)
   calc1 = (x.function1(a, c, b) + y.function2()) /( z.function1() + z.function2())
   calc2 = (x.function1() + y.function2() /( z.function1() + z.function2())
   calc3 = (x.function1() + y.function2()) /( z.function1() + z.function2())
   calc4 = (x.function1() + y.function2()) /( z.function1() + z.function2())
   center = 1
   calc5 = (x.function1() + y.function2()) /(z.function1() + z.function2())
