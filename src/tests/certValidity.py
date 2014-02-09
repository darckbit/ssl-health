
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
		self.name = "ValidityTest"
		self.weight = 0
		self.required= True
		
	# Test
	def performTest(self, scanResult): 


		if (scanResult.validAfter > utc.localize(datetime.datetime.now())):
			return TestResult(self, False, "Certificate is not valid yet.")
		elif (scanResult.validUntil < utc.localize(datetime.datetime.now())):
			return TestResult(self, False, "Certificate is expired.")
		return TestResult(self, True, "Certificate is valid.")


