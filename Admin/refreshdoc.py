"""Script used to refresh the HTML documentation for the VoiceCode Python modules.
"""

import pythondoc.pythondoc
import glob, os, posixpath, sys

#
# Get names of py files to document
#
glob_pattern = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Mediator' + os.sep + '*.py')
modules = glob.glob(glob_pattern)
modules = map(pythondoc.pythondoc.path2module, modules)

#
# Set format to HTML4
#
formats = []
pythondoc.pythondoc.add_formatter('HTML4', formats)

#
# Set documentation directory to $VCODE_HOME/Doc
#
doc_dir = posixpath.expandvars('$VCODE_HOME' + os.sep + 'Doc')
pythondoc.pythondoc._options.add_value('main_directory', doc_dir)

sys.stdout.write("Creating documentation files under directory:\n   %s\n" % (doc_dir))
sys.stdout.write("For modules:\n")
for a_module in modules:
    sys.stdout.write("   %s\n" % a_module)

#
# Generate the HTML documentation
#
pythondoc.pythondoc.generate_pages(modules, formats)



