
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "TLSv1.0 Check"
		self.weight = 75
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		if scanResult.tlsv1_0Enabled == True:
			return TestResult(self, True, "TLSv1 is enabled.")
		return TestResult(self, False, "TLSv1 should be enabled.")




