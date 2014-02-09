import sys
import os
import platform

class Environment:
	tempFolder = ""
	osLib = ""
	fileName = "F2536P9PEPfgRjNZF2KU2dcC"
	trustedCAFile = "" 

	def __init__(self, config):
		self.tempFolder = config.tmp
		self.trustedCAFile = config.trustedCAFile

		if sys.platform == "darwin" :
			self.osLib = os.path.dirname(os.path.realpath( __file__ )) + "/lib/osx64/sslyze.py"
		elif "linux" in sys.platform :
			if platform.architecture()[0] == "64bit":
				self.osLib = os.path.dirname(os.path.realpath( __file__ )) + "/lib/linux64/sslyze.py"
			else:
				self.osLib = os.path.dirname(os.path.realpath( __file__ )) + "/lib/linux32/sslyze.py"
		else:
			print "Operating system not supported!"
			exit(42)
