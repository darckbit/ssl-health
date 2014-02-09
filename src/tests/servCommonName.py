
# Import Parent
import test

from testresult import TestResult

import pytz

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "Subject name"
		self.weight = 0
		self.required = True
		
	# Test
	def performTest(self, scanResult): 
		if scanResult.hostnameMatch == True:
			return TestResult(self, True, "Domain name found in certificate.")
		return TestResult(self, False, "Domain name not found in certificate.")


