"""Script used to refresh the HTML documentation for the VoiceCode Python modules.
"""


import pythondoc.pythondoc
import glob, os, posixpath, re, sys
import util


if (__name__ == '__main__'):
    #
    # Path of the pythondoc or pydoc.py script
    #
   pydoc_path = 'D:\Util\Python\pydoc.py'

   #
   # Get names of py files to document
   #
   #    glob_pattern = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Mediator' + os.sep + '*.py')
   glob_pattern = posixpath.expandvars('$VCODE_HOME' + os.sep + '*' + os.sep + '*.py')
   files = glob.glob(glob_pattern)

   #
   # Remove make_doc.py from files list
   #
#     this_file_name = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Admin' + os.sep + 'make_doc.py')
#     this_file_ind = files.index(this_file_name)
#     files = files[:this_file_ind - 1] + files[this_file_ind + 1:]
   
   
   
   # Not needed anymore
   # modules = map(pythondoc.pythondoc.path2module, files)
   
   #
   # Set format to HTML4
   #
   #  formats = []
   #  pythondoc.pythondoc.add_formatter('HTML4', formats)
   
   #
   # Set documentation directory to $VCODE_HOME/Doc
   #
   doc_dir = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Doc')
   
   #  pythondoc.pythondoc._options.add_value('main_directory', doc_dir)
   #  pythondoc.pythondoc._options.add_value('main_index', 1)
   
   # for a_module in modules:
   #     sys.stdout.write("   %s\n" % a_module)
   #     pythondoc.pythondoc.generate_pages(modules, formats)
   
   
   
   #
   # Generate the HTML doc for each module
   #
   cmd_line = 'python ' + pydoc_path + ' -i -f HTML4 -d ' + doc_dir + ' '
   for a_file in files:
       
       #
       # Check to see if HTML doc needs to be refreshed
       #
       a_match = re.match('.*?([^\\' + os.sep + ']*)\.py$', a_file)
       module_name = a_match.groups()[0]
#       print "groups()=%s" % str(a_match.groups())
       html_file = doc_dir + os.sep + module_name + '.html'
#       print "html_file='%s'" % html_file
#       print "   %s\n" % a_file

       if (util.last_mod(html_file) < util.last_mod(a_file)):
           print "   Updating documentation for module '%s'...\n" % module_name
           os.system(cmd_line + a_file)
