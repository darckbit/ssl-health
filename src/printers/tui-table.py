
# Import Parent
import printer

# Terminal colors
COLOR_ORIGINAL 	= "\033[0m"
COLOR_BOLD 		= "\033[0m"
COLOR_RED		= "\033[1;31m"
COLOR_GREEN		= "\033[1;32m"
COLOR_YELLOW	= "\033[1;33m"

# Terminal printer.
class Printer(printer.Printer):
	
	hasPrintedFirstLine = False

	hostLength = 40

	# implemtation
	def doPrintResults(self, service, testResults, healthScore):
		if not self.hasPrintedFirstLine:
			self.hasPrintedFirstLine = True
			self._printHeader(testResults)

		testStr = ""
		for testResult in testResults:
			testStr += " " + self.getCheckBox(testResult.getPositive()) + " |"


		hostname = self.formatStringToLen("hostname", 40)
		resStr = "| " + self.formatStringToLen(service.getHostname(), 40) + " | " + self.formatStringToLen(service.getPort(), 4) + " | " + self.formatStringToLen(str(healthScore), 5) + " |" + testStr

		print resStr
			

	# header
	def _printHeader(self, testResults):

		testNr = 0
		testStr = ""
		testLegend = "Tests: \n"

		for testResult in testResults:
			testNr += 1
			testStr += " " + str(testNr) + " " * (2-len(str(testNr))) + "|"
			testLegend += "\n[" + str(testNr) + "] " + testResult.getTestName()

		hostname = self.formatStringToLen("hostname", 40)
		header = "| " + hostname + " | port | score |" + testStr

		print testLegend
		print "-" * len(header)
		print header
		print "-" * len(header)

	# Generate checkbox
	def getCheckBox(self, positive):
		if positive: 
			return COLOR_GREEN + 'V' + COLOR_ORIGINAL
		return COLOR_RED + 'X' + COLOR_ORIGINAL

	def formatStringToLen(self, name, length):
		return name + " " * (length-len(name))