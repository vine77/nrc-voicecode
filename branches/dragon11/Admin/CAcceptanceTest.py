import os
import AcceptanceTestHelpers
## For each programming language in voicecode a file like this should be present,
## for doing the acceptance tests.
## See JavascriptAcceptanceTest.py for more detailed instructions...

class CAcceptanceTest(AcceptanceTestHelpers.AcceptanceTestHelpers):
     
    def __init__(self, name):
        AcceptanceTestHelpers.AcceptanceTestHelpers.__init__(self, name)
        language_name = self.__class__.__name__
        self.assert_(language_name.endswith("AcceptanceTest"), "Class name must end with 'AcceptanceTest'")
        self.language_name = language_name[:-len("AcceptanceTest")]
        self.file_extension = ".cpp"    
        self.header_of_demo_file = "demo file generated with mediator test of %s"% self.__class__.__name__
        
    def setUp(self):
        self._init_simulator_regression()
        # test can change the working directory, so save:
        self.old_dir = os.getcwd()
        
    def tearDown(self):

        if os.getcwd() != self.old_dir:
            print 'reset working directory to: %s'% self.old_dir
            os.chdir(self.old_dir)

###############################################################
# Assertions.
# 
# Demo of statements, collect new test or test previous entered tests
###############################################################

    def test_make_new_acceptance_test(self):
        """define new statements for a javascript acceptance test
        """
## instructions:        
## --put in source:  a series of Heard strings from an interactive session or
##                   a series of self._say("...") commands or
##                   a series of commands.say(['comment','line']) (as from the old style tests)
##                   just a series of utterances
## --put in name: the name of the test

## In Data/Demo/javascript a python file "name.py" is created, which contains the phrases and
## window contents.

## put in the return as the top again if you are ready. Next time the test is taken with the other acceptance tests

## For each test an empty test file is taken...
## 
        return

        name = "comments"                        

        source =    \
"""        
    commands.say(['comment','line'])
    commands.say(['test','comment'])
    commands.say(['new','paragraph'])
    commands.say(['begin','long','comment','this'])
    commands.say(['new','line'])
    commands.say(['is','an','important'])
    commands.say(['new','line'])
    commands.say(['bit','of','information','end','long','comment'])
    commands.say(['new','paragraph'])
"""
        self.make_acceptance_test_file(source, name)

        

    def test_acceptance_tests(self):
        """go through the previous setup demo tests


        see test_make_new_acceptance_test above, for making them
        """
        demo_folder = self.find_demo_directory()
        # needed for importlater:
        os.chdir(demo_folder)
        files = os.listdir(demo_folder)
##        print 'working dir: %s'% os.getcwd()
##        import sys
##        if "." not in sys.path:
##            sys.path.insert(0, ".")
        nFail = 0
        for file_path in files:
            if not file_path.endswith(".py"):
                continue
            if file_path.endswith("__new.py"):
                continue
            result = self.do_test_acceptance_test_file(demo_folder, file_path, no_stop=1)
            if result:
                self.print_acceptance_fail_result(result)
                nFail += 1
        if nFail:
            self.fail("%s of the acceptance tests of %s failed"% (nFail, self.language_name))
