"""Script used to refresh the HTML documentation for the VoiceCode Python modules.

Usage: python make_doc.py files

files: names of .py files for which to refresh the documentation. If files is not specified, then documentation for all .py files is refreshed.

Example: python make_doc.py Object.py
"""

import pythondoc.pythondoc
import glob, os, posixpath, re, sys
import util

regs_file_name = None

def fix_references(doc_dir):
   """For some reason, internal references must be specified as:

   \.\. [anchor] file:///./this_file.html#internal_ID (for internal refs)
   or
   \.\. [anchor] file:///some_file.html#ID (for external refs)
   

   instead of

   \.\. [anchor] #internal_ID or \.\. [anchor] some_file.html#ID

   The later causes pythondoc to choke on the definition (note that
   the syntax "anchor":#internal_ID doesn't work either, because
   pythondoc inserts it as is).

   The problem is that while pythondoc works with
   file:///./this_file#internal_ID, neither Netscape nor IE will find
   the file unless they are started from the Doc directory.

   To deal with this problem, *fix_internal_references* substitutes
   file:///./ and file:/// for a null string in all the Doc/*.html files.   
   """

   files = glob.glob(doc_dir + os.sep + '*.html')
   for a_file_name in files:

      #
      # Read the file
      #
      a_file = open(a_file_name, 'r')
      a_file_content = a_file.read()
      a_file.close()

      #
      # Substitute 'file:///./' -> ''
      #
      reg_internal_ref = 'file:\\/\\/\\/.\\/'
      reg_external_ref = 'file:\\/\\/\\/'
      (a_file_content, num_subst1) = re.subn(reg_internal_ref, '', a_file_content)
      (a_file_content, num_subst2) = re.subn(reg_external_ref, '', a_file_content)

      #
      # Don't resave the file if hasn't change, in order to preserve its date.
      #
      if num_subst1 + num_subst2:
         a_file = open(a_file_name, 'w')
         a_file.write(a_file_content)
         a_file.close()




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
   # Remove files that don't match name patter
   #
   if sys.argv: regs_file_name = sys.argv[1:]
   if regs_file_name:
      orig_files = files
      files = []
      for a_file in orig_files:
         for a_reg in regs_file_name:
            a_reg = '[\s\S]*\\' + os.sep + a_reg + '$'
            if re.match(a_reg, a_file):
               files = files + [a_file]
               break

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
       html_file = doc_dir + os.sep + module_name + '.html'

       if (util.last_mod(html_file) < util.last_mod(a_file)):
           print "   Updating documentation for module '%s'...\n" % module_name
           os.system(cmd_line + a_file)

   #
   # Fix problem with references
   #
   fix_references(doc_dir)












