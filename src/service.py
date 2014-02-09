
# Load scanresult class.
from scanresult import ScanResult
import os

class Service():
	"""docstring for Service"""
	hostname = ""
	port = ""
	scanResult = None
	env = None

	def __init__(self, hostname, port, environment):
		self.hostname = hostname
		self.port = port
		self.environment = environment

	def getHostname(self):
		return self.hostname	

	def getPort(self):
		return self.port

	def getScanResult(self):
		return self.scanResult

	def scan(self):
		# to be implemented.
		fullFilePath = self.environment.tempFolder + "ssl-health-tool-" + self.hostname + "" + self.environment.fileName
		os.system("python " + self.environment.osLib + " " + self.hostname + ":" + self.port + " --regular --xml_out=" + fullFilePath + " > /dev/null")
		self.scanResult = ScanResult(self);
		if self.scanResult.parseFromFile(fullFilePath) == False:
			self.scanResult = None
		#os.unlink(fullFilePath)
		
