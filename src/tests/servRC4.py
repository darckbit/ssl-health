
# Import Parent
import test

from testresult import TestResult

class Test(test.Test):
	def __init__(self):
		self.name = "RC4 Usage"
		self.weight = 80
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

		rc4usage = False

		for cip in ciphers:
			if "RC4" in cip.split('-'):
				rc4usage = True
				break

		if rc4usage:
			return TestResult(self, False, "RC4 cipher is available.")
		return TestResult(self, True, "RC4 cipher is disabled.")


