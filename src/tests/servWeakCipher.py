
# Import Parent
import test

from testresult import TestResult

class Test(test.Test):
	def __init__(self):
		self.name = "Weak ciphers"
		self.weight = 250
		self.required = False
		
	# Test
	def performTest(self, scanResult): 
		lowest = 204800
		
		for cip in scanResult.sslv2CipherSuites:
			if scanResult.sslv2CipherSuites[cip] < lowest:
				lowest = scanResult.sslv2CipherSuites[cip]
		for cip in scanResult.sslv3CipherSuites:
			if scanResult.sslv3CipherSuites[cip] < lowest:
				lowest = scanResult.sslv3CipherSuites[cip]
		for cip in scanResult.tlsv1_0CipherSuites:
			if scanResult.tlsv1_0CipherSuites[cip] < lowest:
				lowest = scanResult.tlsv1_0CipherSuites[cip]
		for cip in scanResult.tlsv1_1CipherSuites:
			if scanResult.tlsv1_1CipherSuites[cip] < lowest:
				lowest = scanResult.tlsv1_1CipherSuites[cip]
		for cip in scanResult.tlsv1_2CipherSuites:
			if scanResult.tlsv1_2CipherSuites[cip] < lowest:
				lowest = scanResult.tlsv1_2CipherSuites[cip]
		if lowest < 128:
			return TestResult(self, False, "Low bit ("+ str(lowest) +") security.")
		return TestResult(self, True, "Secure number of bits.("+ str(lowest)+")")


