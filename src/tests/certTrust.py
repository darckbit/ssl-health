
# Import Parent
import test
import os

from testresult import TestResult

import pytz
utc=pytz.UTC
from dateutil import parser
import datetime

#ValidityTest
class Test(test.Test):
	"""docstring for ClassName"""
	def __init__(self):
		self.name = "Trust Test"
		self.weight = 0
		self.required = True
		
	# Test
	def performTest(self, scanResult): 
		res = os.system("echo -n | openssl s_client -prexit -CAfile " + scanResult.service.environment.trustedCAFile + " -showcerts -status -connect " + scanResult.service.getHostname() + ":" + scanResult.service.getPort() + " 2>&1 >/dev/null | grep verify\ error > /dev/null")
		
		if res == 0:
			return TestResult(self, False, "Certificate (Chain) not trused.")
		return TestResult(self, True, "Certificate (Chain) trused.")
