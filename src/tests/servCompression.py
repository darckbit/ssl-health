
# Import Parent
import test

from testresult import TestResult

import pytz
utc=pytz.UTC
from dateutil import parser
import datetime

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "Compression Disabled"
		self.weight = 50
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		# Perform a test.
		if True:
			# Testresults needs a test.
			return TestResult(self, True, "Compression is disabled.")
		return TestResult(self, False, "Compression is enabled.")


