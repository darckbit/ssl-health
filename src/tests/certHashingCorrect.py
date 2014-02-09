
# Import Parent
import test

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "Hashing signature"
		self.weight = 80
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		# Perform a test.
		if scanResult.signatureAlgorithm == "md5WithRSAEncryption":
			# Testresults needs a test.
			return TestResult(self, False, "Hashing considerate insecure")
		return TestResult(self, True, "Hashing considerate secure")



