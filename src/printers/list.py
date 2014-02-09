# Import Parent
import printer

# Terminal colors
COLOR_ORIGINAL 	= "\033[0m"
COLOR_RED		= "\033[1;31m"
COLOR_GREEN		= "\033[1;32m"
COLOR_YELLOW	= "\033[1;33m"
COLOR_BLUE		= '\033[1;36m'


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
			cntWeight = 0.0
			maxWeight = 0.0
			errorLabel = ""
			for testResult in testResults:
				if testResult.getRequiredPass() == False:
					errorLabel = "-> Did not pass required "+ COLOR_BLUE + testResult.getTestName() + COLOR_ORIGINAL + " test"
					break;

			print "" + service.getHostname() + ":" + service.getPort() + " " + self.getGradeColored(healthScore) + " " + errorLabel

