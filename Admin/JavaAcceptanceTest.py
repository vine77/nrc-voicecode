import os
import AcceptanceTestHelpers
## For each programming language in voicecode a file like this should be present,
## for doing the acceptance tests.

## The tests are kept in the directory Data/Demo/java (for this one), in python files.
## These files are tested in "test_acceptance_tests" one by one,
## and the results are tested against the expected results.
#  Note: the first difference ends the testing!

## The test files are also going to be used for "what can I say" demonstration.

## When you want to make a new test follow the instructions in
## the function "test_make_new_acceptance_test" below.
## Do not forget to comment out your lines after you did so.

## When one of the tests does not pass any more,
## the results are kept in the file "demo_name__new.py" (test file was "demo_name.py").
## If you are sure the new result is correct,
## for example after improvements in the voicecode code or in the vc_config file,
## simply remove the previous file and rename the __new.py file.

class JavaAcceptanceTest(AcceptanceTestHelpers.AcceptanceTestHelpers):
     
    def __init__(self, name):
        AcceptanceTestHelpers.AcceptanceTestHelpers.__init__(self, name)
        language_name = self.__class__.__name__
        self.assert_(language_name.endswith("AcceptanceTest"), "Class name must end with 'AcceptanceTest'")
        self.language_name = language_name[:-len("AcceptanceTest")]
        self.file_extension = ".java"    
        self.header_of_demo_file = "demo file generated with mediator test of %s"% self.__class__.__name__
        
    def setUp(self):
        self._init_simulator_regression()
        # test can change the working directory, so save:
        self.old_dir = os.getcwd()
        
    def tearDown(self):

        if os.getcwd() != self.old_dir:
##            print ' working directory to: %s'% self.old_dir
            os.chdir(self.old_dir)

###############################################################
# Assertions.
# 
# Demo of statements, collect new test or test previous entered tests
###############################################################

    def test_make_new_acceptance_test(self):
        """define new statements for a java acceptance test
        """
## instructions:        
## --put in source:  a series of Heard strings from an interactive session or
##                   a series of self._say("...") commands or
##                   just a series of utterances
## --put in name: the name of the test

## In Data/Demo/java a python file "name.py" is created, which contains the phrases and
## window contents.

## put in the return as the top again if you are ready. Next time the test is taken with the other acceptance tests

## For each test an empty test file is taken...
## 
        return
        source =    \
"""        
        self._say("import hello world")
        self._say("new statement")
"""
        name = "demo import"                        
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
            
        for file_path in files:
            if not file_path.endswith(".py"):
                continue
            if file_path.endswith("__new.py"):
                continue
            self.do_test_acceptance_test_file(demo_folder, file_path)

    def do_test_acceptance_test_file(self, demo_folder, file_path):
        """ Do the acceptance test for one file in Data/Demo/language_name

        First all utterances are simulated, and the results are collected.
        The utterances are taken from an imported python file that is passed
        as input.

        These results are written to a new python file.  The two resulting files
        compared variable by variable.
        """
        file_full_path = os.path.join(demo_folder, file_path)
        file_trunc = file_path[:-3]
        test_name = file_trunc.replace('_', " ")
        try:
            _ref_mod = __import__(file_trunc)
        except ImportError:
            print "could not import %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
            return 
        test_info = 'acceptance test for "%s", test: "%s", file: "%s"'% (self.language_name, test_name,file_full_path)  
        utterances = self.get_numbered_variables_from_module(_ref_mod, 'utt')
        if not utterances:
            print "not a valid testfile: %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
            return 
        # doing the utterances and collecting the results:
        print 'starting with acceptance test (%s): %s'% (self.language_name, file_trunc)
        self._open_empty_test_file("acceptance_test_%s%s"% (file_trunc, self.file_extension))
        collect_data = ["# " + self.header_of_demo_file]
        collect_data.append("#")
        for utt in utterances:
            said = getattr(_ref_mod, utt)
            self._say(said)
            buffer_contents = self._get_buffer_content_with_selection_position()
            collect_data.extend(self.make_utterance_contents_list(utt, said, buffer_contents))

        # write the results to a __new.py testfile:
        test_trunc = file_trunc + "__new"
        test_file = os.path.join(demo_folder,test_trunc +  ".py")
        if os.path.isfile(test_file):
            os.remove(test_file)
        self.failIf(os.path.isfile(test_file), 'testfile %s should not be present at start of test, could not be removed'% test_file)
        open(test_file, 'w').write('\n'.join(collect_data))
        ## self.assert_equal_files(file_path, test_file, "of acceptance test %s"%test_name)
        ## # if ok, remove the __new.py file:
        ## os.remove(test_file)

        # and open the testfile as module, in order to compare the contents:
        try:
            _test = __import__(test_trunc)
        except ImportError:
            print "could not import %s, ERROR!! skip further testing of %s"% (test_trunc, test_info)
            return 
        self.assert_equal_test_modules(_ref_mod, _test, test_info)
        # test was ok, remove the testfile:
        os.remove(test_file)


