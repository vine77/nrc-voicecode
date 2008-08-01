import VoiceCodeRootTest
import vc_globals
import os, os.path
import time

class AcceptanceTestHelpers(VoiceCodeRootTest.VoiceCodeRootTest):
    """Helper functions for the different language acceptance test files.

    """
     
    def __init__(self, name):
        VoiceCodeRootTest.VoiceCodeRootTest.__init__(self, name)

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
        os.chdir(demo_folder)

        filename = name.replace(' ', '_') + '.py'
        filename_fullpath = os.path.join(demo_folder, filename)
        language_file = name.replace(' ', '_') + self.file_extension
        if os.path.exists(filename):
            print "Warning, overwriting old demo file: %s\nRevert with SVN if this was not your intention!!"% filename_fullpath
        collect_data = ["# " + self.header_of_demo_file]
        collect_data.append("#")


        self._open_empty_test_file("acceptance_test_%s"% language_file)
        
        i = 0
        for line in source.split("\n"):
            utterance = self.extract_utterance(line)
            if not utterance: continue
            i += 1
            self._say(utterance)
            got_content = self._get_buffer_content_with_selection_position()
            utt_name = 'utt%s'% i
            collect_data.extend(self.make_utterance_contents_list(utt_name, utterance, got_content))
        open(filename_fullpath, 'w').write('\n'.join(collect_data))
        print "written acceptance_test_file: %s"% filename_fullpath

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
        test_info = 'acceptance test for "%s"\ntest: "%s"\nfile: "%s"'% (self.language_name, test_name,file_full_path)  
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


    def get_numbered_variables_from_module(self, module, prefix):
        """return, sorted by number a list of variables from a module

        Module must be imported before calling.

        As example when prefix = "utt" the result can be:
           ['utt1', 'utt2', 'utt3']
        """
        prefix_length = len(prefix)
        utterances = [(int(v[prefix_length:]), v) for v in dir(module) if v.startswith(prefix) and int(v[prefix_length:]) > 0]
        utterances.sort()
        return [v for (dummy, v) in utterances]
    
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
        """make a list of saying (utterance)  and result for acceptance test file"""
        collect_data = []
        quoted_utt = self.quote_string(utterance)
        collect_data.append("%s = %s"%  (utt_name, quoted_utt))  
        expected_name = utt_name.replace("utt", "exp")
        quoted_got_content = self.quote_string(got_content)
        collect_data.append("%s = \\\n%s"%  (expected_name, quoted_got_content))  
        return collect_data

    def quote_string(self, text):
        """place the text between fitting quotes, for printing in a file"""
        if text.find('\n') >= 0:
            triple = 1
        elif text.find('"') >= 0 and text.find("'") >= 0:
            triple = 1
        else:
            triple = 0

        if triple:
            if text.find('"""') >= 0:
                if text.find("'''") >= 0:
                    text = text.replace("'", "\\'")
                quote = "'''"
            else:
                quote = '"""'

        else:
            if text.find('"') >= 0:
                quote = "'"
            else:
                quote = '"'
        return quote + text + quote
                
    def assert_equal_test_modules(self, ref, to_test, test_info):
        """test contents of modules not tested yet, first try with compare files..."""
        ## self.assert_equal(dir(ref), dir(to_test))
        
        utt_ref = self.get_numbered_variables_from_module(ref, "utt")
        utt_to_test = self.get_numbered_variables_from_module(to_test, "utt")
        exp_ref = self.get_numbered_variables_from_module(ref, "exp")
        exp_to_test = self.get_numbered_variables_from_module(to_test, "exp")
        self.assert_equal(utt_ref, utt_to_test, 'utterance variables in reference and to_test file of test "%s" should be equal'% test_info)

        for u_ref, u_to_test, e_ref, e_to_test in zip(utt_ref, utt_to_test, exp_ref, exp_to_test):
            spoken_reference = getattr(ref, u_ref)
            spoken_to_test = getattr(to_test, u_ref)
            content_reference = getattr(ref, e_ref)
            content_to_test = getattr(to_test, e_ref)
            message = "utterances %s and %s should be equal in\ntest %s"% (u_ref, u_to_test, test_info)
            self.assert_equal(spoken_reference, spoken_to_test, message)
            message = 'buffer after saying "%s"\n(utterance %s) should be equal in\ntest %s'%  (spoken_reference, u_ref, test_info)
            self.assert_equal(content_reference, content_to_test,  message)
        max_items = max(map(len, [utt_ref, utt_to_test, exp_ref, exp_to_test]))
        min_items = min(map(len, [utt_ref, utt_to_test, exp_ref, exp_to_test]))
        self.assert_equal(max_items, min_items, "number of items not the same, min: %s, max: %s\ntest:%s"%
                          (max_items, min_items, test_info) )
        
    
            



        
