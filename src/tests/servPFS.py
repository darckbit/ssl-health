
# Import Parent
import test

from testresult import TestResult

class Test(test.Test):
	def __init__(self):
		self.name = "PFS Availability"
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

		pfsav = False

		for cip in ciphers:
			s = cip.split('-')
			if "ECDHE" in s or "DHE" in s:
				pfsav = True
				break

		if pfsav:
			return TestResult(self, True, "Perfect Forward Secrecy is available.")
		return TestResult(self, False, "Perfect Forward Secrecy is not available.")


