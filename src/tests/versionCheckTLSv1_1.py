
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "TLSv1.1 Check"
		self.weight = 100
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		if scanResult.tlsv1_1Enabled == True:
			return TestResult(self, True, "TLSv1.1 is enabled.")
		return TestResult(self, False, "TLSv1.1 should be enabled.")




