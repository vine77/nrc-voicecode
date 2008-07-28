import debug
import VoiceCodeRootTest
import vc_globals
import os, os.path
import time
## For each programming language in voicecode a file like this should be present,
## for doing the acceptance tests.

## The tests are kept in the directory Data/Demo/Javascript (for this one), in python files.
## These files are tested in "test_acceptance_tests" one by one,
## and the results are tested against the expected results.

## The test files are also going to be used for "what can I say" demonstration.

## When you want to make a new test follow the instructions in
## the function "test_make_new_acceptance_test" below.
## Do not forget to comment out your lines after you did so.

## When one of the tests does not pass any more,
## the results are kept in the file "demo_name__new.py" (test file was "demo_name.py").
## If you are sure the new result is correct,
## for example after improvements in the voicecode code or in the vc_config file,
## simply remove the previous file and rename the __new.py file.

class JavascriptAcceptanceTest(VoiceCodeRootTest.VoiceCodeRootTest):
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)
        language_name = self.__class__.__name__
        self.assert_(language_name.endswith("AcceptanceTest"), "Class name must end with 'AcceptanceTest'")
        self.language_name = language_name[:-len("AcceptanceTest")]
        self.file_extension = ".js"    
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
# Demo of statements, use collect_mode to set up...
###############################################################

    def test_make_new_acceptance_test(self):
        """define new statements for a javascript acceptance test
        """
## instructions:        
## --put in source:  a series of Heard strings from an interactive session or
##                   a series of self._say("...") commands or
##                   just a series of utterances
## --put in name: the name of the test

## In Data/Demo/javascript a python file "name.py" is created, which contains the phrases and
## window contents.

## put in the return as the top again if you are ready. Next time the test is taken with the other acceptance tests

## For each test an empty test file is taken...
## 
        return
        source =    \
"""        
        self._say("new statement")
        self._say("example equals one")
        self._say("new statement")
"""
        name = "demo statement"                        
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
            print 'file: %s' % file_path
            file_trunc = file_path[:-3]
            name = file_trunc.replace('_', " ")
            try:
                _imp = __import__(file_trunc)
            except ImportError:
                print "could not import %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
                continue
            utterances = [(int(v[3:]), v) for v in dir(_imp) if v.startswith('utt') and int(v[3:]) > 0]
            if not utterances:
                print "not a valid testfile: %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
                continue
            test_file = os.path.join(demo_folder, file_trunc + "__new.py")
            utterances.sort()
            utterances = [utt for (dummy, utt) in utterances]
            
            print 'starting with acceptance test (%s): %s'% (self.language_name, file_trunc)
            print 'utterances: %s'% utterances
            self._open_empty_test_file("acceptance_test_%s.js"% file_trunc)
            collect_data = ["# " + self.header_of_demo_file]
            collect_data.append("#")
            collect_data.append('name = "%s"'% name)
            for utt in utterances:
                said = getattr(_imp, utt)
                self._say(said)
                time.sleep(0.3)
                buffer_contents = self._get_buffer_content_with_selection_position()
                collect_data.extend(self.make_utterance_contents_list(utt, said, buffer_contents))

            
            open(test_file, 'w').write('\n'.join(collect_data))
            
            try:
                _imp = __import__(file_trunc)
            except ImportError:
                print "could not import %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
                continue
            utterances = [(int(v[3:]), v) for v in dir(_imp) if v.startswith('utt') and int(v[3:]) > 0]
            if not utterances:
                print "not a valid testfile: %s (%s, %s), skip testing"% (file_trunc, demo_folder, file_path)
                continue
            test_trunc = file_trunc + "__new"
            test_file  =os.path.join(demo_folder, test_trunc + ".p")
            utterances.sort()
            utterances = [utt for (dummy, utt) in utterances]
            
            print 'starting with acceptance test (%s): %s'% (self.language_name, file_trunc)
            print 'utterances: %s'% utterances
            self._open_empty_test_file("acceptance_test_%s.js"% file_trunc)
            collect_data = ["# " + self.header_of_demo_file]
            collect_data.append("#")
            collect_data.append('name = "%s"'% name)
            for utt in utterances:
                said = getattr(_imp, utt)
                buffer_contents = self._get_buffer_content_with_selection_position()
                collect_data.extend(self.make_utterance_contents_list(utt, said, buffer_contents))

            
            open(test_file, 'w').write('\n'.join(collect_data))
            try:
                _test = __import__(test_trunc)
            except ImportError:
                print "could not import %s (%s, %s), skip further testing"% (test_trunc, demo_folder, test_file)
                continue
            time.sleep(1)
            self.assert_equal_test_modules(_imp, _test)
                

    def find_demo_directory(self):
        """Return the correct language directory in Data/Demo"""
        demo_folder = vc_globals.demo_data
        self.assert_(os.path.isdir(demo_folder), "not a directory: %s"% demo_folder)
        demo_folder = os.path.join(demo_folder, self.language_name)
        self.assert_(os.path.isdir(demo_folder), "Please make a new demo directory for %s: %s"% (self.language_name, demo_folder))
        return demo_folder
        
    def make_acceptance_test_file(self, source, name, first=1):
        """make in Data/Demo/<language> a demo file, for What can I say or later acceptance test use

        """
        demo_folder = self.find_demo_directory()
        filename = name.replace(' ', '_') + '.py'
        filename_fullpath = os.path.join(demo_folder, filename)
        if os.path.exists(filename_fullpath):
            print "Warning, overwriting old demo file: %s\nRevert with SVN if this was not your intention!!"% filename_fullpath
        collect_data = ["# " + self.header_of_demo_file]
        collect_data.append("#")
        collect_data.append('name = "%s"'% name)
        
        i = 0
        for line in source.split("\n"):
            utterance = self.extract_utterance(line)
            if not utterance: continue
            i += 1
            self._say(utterance)
            time.sleep(0.5)
            got_content = self._get_buffer_content_with_selection_position()
            utt_name = 'utt%s'% i
            collect_data.extend(self.make_utterance_contents_list(utt_name, utterance, got_content))
        open(filename_fullpath, 'w').write('\n'.join(collect_data))
        print "written acceptance_test_file: %s"% filename_fullpath

    def extract_utterance(self, line):
        """extract the "said part" of a line"""

        line = line.strip()
        if not line: return
        if line.startswith('self._say("'):
            quote = '"'
            parts = line.split(quote)
            utterance = parts[1]
        elif line.startswith("self._say('"):
            quote = "'"
            parts = line.split(quote)
            utterance = parts[1]
        elif line.startswith("Heard "):
            utterance = line[6:].strip()
            print 'Heard: %s'% utterance
        else:
            utterance = line
        return utterance


    def make_utterance_contents_list(self, utt_name, utterance, got_content):
            """make a list of saying and result for acceptance test file"""
            collect_data = []
            if utterance.find('"') == -1:
                quote = '"'
            else:
                self.assert_(utterance.find("'")== -1, \
                            "utterance contains single AND double quotes: %s\nplease change your test"% utterance)
                quote = "'"
            if quote == "'":
                collect_data.append("%s = '%s'"%  (utt_name, utterance))  
            else:
                collect_data.append('%s = "%s"'%  (utt_name, utterance)) 

            if not got_content.find('"""'):
                quote = '"""'
            else:
                self.assert_(got_content.find("'''") ==  - 1,
                             "Contents have both double and single triple quotes. Please find another test\n%s"% got_content)
                quote = "'''"
            expected_name = utt_name.replace("utt", "exp")
            
            if quote == "'''":
                collect_data.append("%s = \\\n'''%s'''"%  (expected_name, got_content))  
            else:
                collect_data.append('%s = \\\n"""%s"""'%  (expected_name, got_content)) 
            return collect_data

                
    def assert_equal_test_modules(self, ref, to_test):
        """test contents of modules"""
        self.assert_equal(dir(ref), dir(to_test)) 
