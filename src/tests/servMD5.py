
# Import Parent
import test

from testresult import TestResult

class Test(test.Test):
	def __init__(self):
		self.name = "MD5 Usage"
		self.weight = 50
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		ciphers = []

		for cip in scanResult.sslv2CipherSuites:
			ciphers.append(cip)
		for cip in scanResult.sslv3CipherSuites:
			ciphers.append(cip)
		for cip in scanResult.tlsv1_0CipherSuites:
			ciphers.append(cip)
		for cip in scanResult.tlsv1_1CipherSuites:
			ciphers.append(cip)
		for cip in scanResult.tlsv1_2CipherSuites:
			ciphers.append(cip)

		MD5usage = False

		for cip in ciphers:
			if "MD5" in cip.split('-'):
				MD5usage = True
				break

		if MD5usage:
			return TestResult(self, False, "MD5 cipher is available.")
		return TestResult(self, True, "MD5 cipher is disabled.")


