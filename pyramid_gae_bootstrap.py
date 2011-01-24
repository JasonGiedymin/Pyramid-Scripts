#!/usr/bin/env python

"""
Directions

	This script is ugly (but it works) and is a stop gap until Pyramid has:
		- specific app monkey scripts sucked into Pyramid
		  (for GAE purposes only)
		- a proper GAE paster template is included
		- less janky directions for GAE

	This script:
		- does not check the return of commands which are executed
		  (no sudo checking, no net connx checking, etc...)
		- has very liberal use of print here...
		- bunch of other garbage which 'could' be refactored but why?
		  Instead work on the two points above.

	How to use this script:
		- Change the bang to the location of your Python binary 
		  (tip: "which python") if env python is not native.
		- Change _GAE_PATH to the location of the GAE SDK 
		  (tip: "which dev_appserver.py |xargs ls -l").
		- Change _APP_MONKEY to the location of where you downloaded the App 
		  Monkey scripts.
		* Run this script like so: "pyramid_gae_bootstrap.py MyApp"
		  Where "MyApp" is the name of your new application.

License

    A copyright notice accompanies this license document that identifies
    the copyright holders.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    1.  Redistributions in source code must retain the accompanying
	copyright notice, this list of conditions, and the following
	disclaimer.

    2.  Redistributions in binary form must reproduce the accompanying
	copyright notice, this list of conditions, and the following
	disclaimer in the documentation and/or other materials provided
	with the distribution.

    3.  Names of the copyright holders must not be used to endorse or
	promote products derived from this software without prior
	written permission from the copyright holders.

    4.  If any files are modified, you must cause the modified files to
	carry prominent notices stating that you changed the files and
	the date of any change.

    Disclaimer

      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND
      ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
      TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
      PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
      HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
      EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
      TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
      DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
      ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
      TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
      THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
      SUCH DAMAGE.

"""

import os
import sys
import commands

## Globals

# Locations
_APP_NAME = None

#DIRECTORY OF THE SDK ONLY!
_GAE_PATH = "/usr/local/google_appengine"

_APP_MONKEY = "/Users/jason/Programming/python/lib-src/appengine-monkey"

def createVirtualEnv():
	if _APP_NAME is not None:
		print("Constructing first command...")
		veCommand = ("python %s/appengine-homedir.py --gae %s %s" % (_APP_MONKEY, _GAE_PATH, _APP_NAME) )


		print("Executing app monkey script...")
		print("Command: [%s]" % veCommand)
		commands.getstatusoutput( veCommand )

		print("Changing to %s..." % _APP_NAME)

		os.chdir("%s" % _APP_NAME)

		print("Installing pyramid via easy_install...")
		print("Command: [bin/easy_install pyramid]")
		commands.getstatusoutput("bin/easy_install pyramid")

		print("Changing to app...")
		os.chdir("app")

		print("Deleting %s..." % _APP_NAME )
		print("rm -rf %s" % _APP_NAME)
		commands.getstatusoutput("rm -rf %s" % _APP_NAME)

		print("Running paster template pyramid_starter on %s..." % _APP_NAME)
		print("bin/paster create -t pyramid_starter %s" % _APP_NAME)
		commands.getstatusoutput("bin/paster create -t pyramid_starter %s" % _APP_NAME)

		print("Moving directories around and cleaning up...")
		commands.getstatusoutput("mv %s aside" % _APP_NAME)
		commands.getstatusoutput("mv aside/%s ." % _APP_NAME)
		commands.getstatusoutput("rm -rf aside")

		print("Creation of virtual environment complete.")

		furtherInstructions()

	else:
		print ("App name not specified.")

def furtherInstructions():
	print("""
	Edit the following files like so:

	config.py		(add the following changes)
		APP_NAME = "pyramidapp:main"
		APP_ARGS = ({},)

	runner.py		(add the os.mkdir line)
		import os
		os.mkdir = None

	runner.py		(add the sys.path line)
		import sys
		sys.path = [path for path in sys.path if 'site-packages' not in path]
		import site
		
	runner.py		(comment out the following)
		# comment the sys.path assertion out
		# assert sys.path[:len(cur_sys_path)] == cur_sys_path, (
		#   "addsitedir() caused entries to be prepended to sys.path")
	
	----------------------------------------------------------------------
	""")
	
	print("To run the server via command-line:")
	print("		dev_appserver.py %s/app/" % _APP_NAME)

	print("""

	""")

	print("To list compressed files run: (also gives a file list count)")
	print("		%s/bin/pip2.5 zip -l" % _APP_NAME)

	print("To compressed files run:")
	print("		%s/bin/pip2.5 zip <a_python.egg>" % _APP_NAME)

	print("Good candidates to compress are:")
	print("Chameleon, zope.i18n, ...")

	print("""
	
	""")

	print("To use PyDev, add all the egg folders from %s/app/lib/python/ to the Python runtime profile." % _APP_NAME)
	print("Do not append them to the PyDev PYTHONPATH.")
	print("PyDev will also need '$GAE_PATH/lib/' to be added to the environment variables for simplejson and the like.")


def main(argv):
	if len(sys.argv) > 1:
		global _APP_NAME
		_APP_NAME = sys.argv[1]

		if not os.path.exists(_APP_NAME):
			print("Creating app %s" % _APP_NAME)

			createVirtualEnv()
		else:
			print("App [%s] already exists, try another name." % _APP_NAME)

	else:
		print("App name not supplied.")
		print("Usage:")
		print("		python %s ExampleApp" % sys.argv[0])

	print("Script Done.")

if __name__ == "__main__":
		main(sys.argv[1:])

