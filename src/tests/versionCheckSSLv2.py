
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "SSLv2 Check"
		self.weight = 100
		self.required = False
		
	# Test
	def performTest(self, scanResult): 

		if scanResult.sslv2Enabled == True:
			# Testresults needs a test.
			return TestResult(self, False, "SSLv2 should be disabled.")
		return TestResult(self, True, "SSLv2 is disabled.")




