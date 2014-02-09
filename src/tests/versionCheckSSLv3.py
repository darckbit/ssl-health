
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "SSLv3 Check"
		self.weight = 30
		self.required = False
		
	# Test
	def performTest(self, scanResult): 

		if scanResult.sslv3Enabled == True:
			# Testresults needs a test.
			return TestResult(self, False, "SSLv3 should be disabled.")
		return TestResult(self, True, "SSLv3 is disabled.")




