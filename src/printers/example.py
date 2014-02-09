# Import Parent
import printer

# Terminal printer.
class Printer(printer.Printer):
	
	# implemtation
	def doPrintResults(self, service, testResults):

			print "Host: " + service.getHostname()
			print "Port:"  + service.getPort()
			print

			for testResult in testResults:

				print "Test name: " + testResult.getTestName()
				print "Test result: " + testResult.getDescription()

				if testResult.getPositive:
					print "Test successful."
				else:
					print "Test failed."

				print
			print