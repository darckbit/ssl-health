import thread
import time
import sys

class HealthAssessor():
	"""docstring for HealthAssessor"""
		
	def __init__(self, printer):
		self.services = []
		self.tests = []
		self.testresults = []
		self.threadFinished = []
		self.threadCounter = 0
		self.printer = printer

	def addService(self, service):
		self.services.append(service)

	def addTest(self, test):
		self.tests.append(test)

	def setPrinter(self, printer):
		self.printer = printer

	def threadBasedTestService(self):
		self.testresults = []
		count = 0
		for service in self.services:
			self.testresults.append(None)
			thread.start_new_thread( self.testService2, (count, service, self.tests, ) )
			count = count+1
		while count != self.threadCounter:
			time.sleep(1)
			sys.stdout.write("\rservices checked: (" + str(self.threadCounter) + "/" + str(count) + ")")
			sys.stdout.flush()
		sys.stdout.write("\r                              \r")
		sys.stdout.flush()
		count = 0
		for service in self.services:
			self.printResults(service,self.testresults[count])
			count = count +1

	def run(self):
		self.printer.printHeader()
		for service in self.services:
			self.printResults(service,self.testService(service,self.tests))
		self.printer.printFooter()
		#self.threadBasedTestService()

	def testService(self, service, tests):
		service.scan()
		testresults = []
		if service.getScanResult() != None:
			for test in tests:
				testresults.append(test.getResult(service.getScanResult()))
		return testresults

	def testService2(self, number, service, tests):
		service.scan()
		testresults = []
		for test in tests:
			testresults.append(test.getResult(service.getScanResult()))
		self.testresults[number] = testresults
		self.threadCounter = self.threadCounter +1
		return

	def printResults(self, service, testresults):
		if(len(testresults)>0):
			self.printer.printResults(service, testresults, self.calculateHealth(testresults))

	def calculateHealth(self, testResults):
		cntWeight = 0.0
		maxWeight = 0.0

		for testResult in testResults:
			if testResult.getRequiredPass() == False:
				cntWeight = 0.0
				maxWeight = 100.0
				break;
			if testResult.getPositive():
				cntWeight = cntWeight + testResult.getTestWeight()
			maxWeight = maxWeight + testResult.getTestWeight()

		return round((cntWeight / maxWeight)*100)
		