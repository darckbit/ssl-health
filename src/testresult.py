

class TestResult:
	"""docstring for ClassName"""
	def __init__(self, test, positive, description):
		#if not isinstance(test, test.Test):
		#	raise Error("Testresult requires instance of Test.")

		self.test = test
		self.positive = positive
		self.description = description
		
	def getTestName(self):
		return self.test.getName()

	def getPositive(self):
		return self.positive

	def getDescription(self):
		return self.description

	def getTestWeight(self):
		return self.test.getWeight()

	def getRequiredPass(self):
		if (self.test.required == True) and (self.getPositive()==False):
			return False
		return True