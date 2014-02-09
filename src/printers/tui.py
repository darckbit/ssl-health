
# Import Parent
import printer

# Terminal colors
COLOR_ORIGINAL 	= "\033[0m"
COLOR_RED		= "\033[1;31m"
COLOR_GREEN		= "\033[1;32m"
COLOR_YELLOW	= "\033[1;33m"

# Terminal printer.
class Printer(printer.Printer):
	def getGradeColored(self, grade):
		if grade < 55:
			return COLOR_RED + "" + str(grade) + "%" + COLOR_ORIGINAL
		elif grade < 70:
			return COLOR_YELLOW + "" + str(grade) + "%" + COLOR_ORIGINAL
		return COLOR_GREEN + "" + str(grade) + "%" + COLOR_ORIGINAL
	# implemtation
	def doPrintResults(self, service, testResults, healthScore):

			print "Host: " + service.getHostname() + ":" + service.getPort() + "\tScore: " + self.getGradeColored(healthScore)
			print "-" * 80

			for testResult in testResults:

				firstspace = 20 - len(testResult.getTestName())
				secondspace = 50 - len(testResult.getDescription())

				print " " + testResult.getTestName() + " " * firstspace + " - " + testResult.getDescription() + " " * secondspace + self.getCheckBox(testResult.getPositive())
			print "-" * 80

	# Generate checkbox
	def getCheckBox(self, positive):
		if positive: 
			return COLOR_ORIGINAL + '[ ' + COLOR_GREEN + 'ok' + COLOR_ORIGINAL + ' ]'
		return COLOR_ORIGINAL + '[' + COLOR_RED + 'fail' + COLOR_ORIGINAL + ']'
