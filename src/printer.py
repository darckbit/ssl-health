
# Abstract class
from abc import ABCMeta, abstractmethod

#Printer class, abstract.
class Printer:

	# Abstract class
	__metaclass__ = ABCMeta
 
	# Function  to be implemented by subclasses.
	def printResults(self, Service, TestResults, healthScore): 
		return self.doPrintResults(Service, TestResults, healthScore)

	@abstractmethod
	def doPrintResults(self, Service, TestResults, healthScore): 
		raise NotImplementedError()

	def printHeader(self):
		pass

	def printFooter(self):
		pass