
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "ExampleTest"
		self.weight = 0
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		# Perform a test.
		if scanResult.compressionEnabled == True:
			# Testresults needs a test.
			return TestResult(self, True, "Test successful")
		return TestResult(self, False, "Test not successful")




