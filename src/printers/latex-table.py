
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
	
	# init
	def __init__(self):
		self.hasPrintedFirstLine = False
		self.hostLength = 60

	# implemtation
	def doPrintResults(self, service, testResults, healthScore):
		if not self.hasPrintedFirstLine:
			self.hasPrintedFirstLine = True
			self._printHeader(testResults)

		print "% ----------------------------------------------------------------- " + service.getHostname()
		print r"% Host \\"
		print service.getHostname() + " & "
		print r"% Port \\"
		print service.getPort() + " & "
		print r"% Health \\"
		print str(healthScore) + "\% & "

		testStr = ""
		testNr = 0
		tests = len(testResults)
		for testResult in testResults:
			testNr += 1
			print "% " + str(testNr) + " - " + testResult.getTestName()

			if testNr == tests:
				end = 0
			else:
				end = 1

			if testResult.getPositive():
				print r"\tbtrue " + "&" * end
			else:
				print r"\tbfalse " + "&" * end


		  	
		print r"\\ \hline "
		print


			

	# header
	def _printHeader(self, testResults):

		testNr = 0
		testStr = ""
		print r"\begin{table}[th]"
		print r"\centering"
		print r"\label{table:appedix-examined-hosts-legend}"
		print r"\begin{tabular}{|c|l|}"
		print r"\hline"
		print r"Tag & Description \\"
		print r"\hline"
		for testResult in testResults:
			testNr += 1
			print str(unichr(testNr+64))  + r" & " + testResult.getTestName() + r" \\"
			print r"\hline"
			testStr += " & " + str(unichr(testNr+64)) + " " * (2-len(str(testNr))) + ""
		
		print r"\end{tabular}"
		print r"\caption{Common mistakes service legend}"
		print r"\end{table}"

		print r"\begin{table}[th]"
		print r"\centering"
		print
		print r"\label{table:appedix-examined-hosts}"
		print r"\begin{tiny}"
		print
		print r"\begin{tabular}{|c|c|c|" + "c|" * testNr +"}"
		print r"\hline"
		print r"Host & Port & Score" + testStr  + r"\\"
		print



	def printFooter(self):
		print r"\hline"
		print r"\end{tabular}"
		print r"\end{tiny}"
		print r"\caption{Common mistakes service scope. ($\surd$ = in order, $\times$ is not in order.)}"
		print r"\end{table}"

	# Generate checkbox
	def getCheckBox(self, positive):
		if positive: 
			return COLOR_GREEN + 'V' + COLOR_ORIGINAL
		return COLOR_RED + 'X' + COLOR_ORIGINAL

	def formatStringToLen(self, name, length):
		return name + " " * (length-len(name))