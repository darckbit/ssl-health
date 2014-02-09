
# Abstract class
from abc import ABCMeta, abstractmethod

from scanresult import ScanResult

# Test class, abstract.
class Test:
	"""docstring for ClassName"""

	def __init__(self, name, weight):
		self.name = name
		self.weight = weight
		self.required = False

	def getName(self):
		if self.name == None:
			raise Error("Test has no name.")
		return self.name

	def getWeight(self):
		if self.weight == None:
			raise Error("Weight not given")
		return self.weight

	def getResult(self, scanResult):
		if isinstance(scanResult, ScanResult):
			return self.performTest(scanResult)
		raise NotImplementedError()
	
	@abstractmethod
	def performTest(self, scanResult):
	    raise NotImplementedError()