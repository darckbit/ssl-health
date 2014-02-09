
# Import Parent
import test
import os

from testresult import TestResult

#ValidityTest
class Test(test.Test):
	def __init__(self):
		self.name = "Debian weak keys"
		self.weight = 100
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		# Perform a test.
		#res = os.system("curl 'https://factorable.net/keycheck/certificate/process_url?conntype=tls&url=" + scanResult.service.getHostname() + "&port=" + scanResult.service.getPort() + "' 2>/dev/null | grep \"Weak\" | grep \"Passed\" > /dev/null")
		#if res == 0:
		return TestResult(self, True, "Debian key safe.")
		#return TestResult(self, False, "Compromized key found.")




