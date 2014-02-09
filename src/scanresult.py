from dateutil import parser
import datetime
from xml.dom import minidom
import pytz
utc=pytz.UTC

class ScanResult:
	"""ScanResult has the resultset of the scanner"""

	certificate_fingerprint = ""
	certificate_pem = ""
	publicKeyModulus = ""
	publicKeyExponent = ""
	publicKeyAlgorithm = ""
	publicKeySize = ""
	caIssueUrl = ""
	alternativeNames = []
	authKeyIdentifier = ""
	signatureValue = ""
	signatureAlgorithm = ""
	subjectOrginizationName = ""
	subjectSerialNumber = ""
	subjectCommonName = ""
	validUntil = utc.localize(datetime.datetime.now())
	validAfter = utc.localize(datetime.datetime.now())
	issuerCommonName = ""
	validTrustStore = []
	trustStoreName = []
	ocspResult = ""
	compressionEnabled = ""
	sessionRenogotiation = ""
	sessionResumption = ""
	sslv2CipherSuites = {}
	sslv2Enabled = 0
	sslv3CipherSuites = {}
	sslv3Enabled = 0
	tlsv1_0CipherSuites = {}
	tlsv1_0Enabled = 0
	tlsv1_1CipherSuites = {}
	tlsv1_1Enabled = 0	
	tlsv1_2CipherSuites = {}
	tlsv1_2Enabled = 0
	service = None
	hostnameMatch = False

	def __init__(self, service):
		self.service = service

	def getElement(self,document,name):
		if len(document.getElementsByTagName(name))> 0:
			if len(document.getElementsByTagName(name)[0].childNodes) >0:
				return document.getElementsByTagName(name)[0].childNodes[0].wholeText
		return ""

	def parseFromFile(self, filename):
		self.certificate_fingerprint = ""
		self.certificate_pem = ""
		self.publicKeyModulus = ""
		self.publicKeyExponent = ""
		self.publicKeyAlgorithm = ""
		self.publicKeySize = ""
		self.caIssueUrl = ""
		self.alternativeNames = []
		self.authKeyIdentifier = ""
		self.signatureValue = ""
		self.signatureAlgorithm = ""
		self.subjectOrginizationName = ""
		self.subjectSerialNumber = ""
		self.subjectCommonName = ""
		self.validUntil = utc.localize(datetime.datetime.now())
		self.validAfter = utc.localize(datetime.datetime.now())
		self.issuerCommonName = ""
		self.validTrustStore = []
		self.trustStoreName = []
		self.ocspResult = ""
		self.compressionEnabled = ""
		self.sessionRenogotiation = ""
		self.sessionResumption = ""
		self.sslv2CipherSuites = {}
		self.sslv2Enabled = False
		self.sslv3CipherSuites = {}
		self.sslv3Enabled = False
		self.tlsv1_0CipherSuites = {}
		self.tlsv1_0Enabled = False
		self.tlsv1_1CipherSuites = {}
		self.tlsv1_1Enabled = False
		self.tlsv1_2CipherSuites = {}
		self.tlsv1_2Enabled = False
		self.domainnameMatch = False
		if(len(minidom.parse(filename).getElementsByTagName('target'))==0):
			return False
		xmldoc = minidom.parse(filename).getElementsByTagName('target')[0]
		if(len(xmldoc.getElementsByTagName('certificate')) >0 ):
			self.certificate_fingerprint = xmldoc.getElementsByTagName('certificate')[0].getAttribute('sha1Fingerprint')
		else:
			return False
		self.signatureAlgorithm = self.getElement(xmldoc, 'signatureAlgorithm')
		self.certificate_pem = self.getElement(xmldoc, 'asPEM')
		self.publicKeyModulus = self.getElement(xmldoc,'modulus')
		self.publicKeyExponent = self.getElement(xmldoc, 'exponent')
		self.publicKeyAlgorithm = self.getElement(xmldoc, 'publicKeyAlgorithm')
		self.publicKeySize = self.getElement(xmldoc, 'publicKeySize')

		# Bug with mailzim.hostnet.nl:443
		if len(xmldoc.getElementsByTagName('CAIssuers')) > 0:
			self.caIssueUrl = self.getElement(xmldoc.getElementsByTagName('CAIssuers')[0],'listEntry');

		if len(xmldoc.getElementsByTagName('DNS')) > 0:
			for dm in xmldoc.getElementsByTagName('DNS')[0].getElementsByTagName('listEntry'):
				self.alternativeNames.append(dm.childNodes[0].wholeText)
		self.authKeyIdentifier = self.getElement(xmldoc, 'X509v3AuthorityKeyIdentifier')
		self.signatureValue = self.getElement(xmldoc, 'signatureValue')
		self.signatureAlgorithm = self.getElement(xmldoc, 'signatureAlgorithm')
		self.subjectOrginizationName = self.getElement(xmldoc, 'organizationName')
		self.subjectCommonName = self.getElement(xmldoc, 'commonName')
		self.subjectSerialNumber = self.getElement(xmldoc, 'serialNumber')
		self.validUntil = parser.parse(self.getElement(xmldoc, 'notAfter'))
		self.validAfter = parser.parse(self.getElement(xmldoc, 'notBefore'))
		self.issuerCommonName = self.getElement(xmldoc.getElementsByTagName('issuer')[0], 'commonName')
		for dm in xmldoc.getElementsByTagName('pathValidation'):
			self.validTrustStore.append(dm.getAttribute('validationResult'))
			self.trustStoreName.append(dm.getAttribute('usingTrustStore'))
			if len(xmldoc.getElementsByTagName('ocspStapling')) > 0:
				self.ocspResult = False
			else:
				self.ocspResult = True
		self.hostnameMatch = xmldoc.getElementsByTagName('hostnameValidation')[0].getAttribute('certificateMatchesServerHostname')
		if self.hostnameMatch == "True":
			self.hostnameMatch = True
		else:
			self.hostnameMatch = False
			
		self.compressionEnabled = len(xmldoc.getElementsByTagName('compression')[0].childNodes)
		if self.compressionEnabled > 1 :
			self.compressionEnabled = True
		else:
			self.compression = False

		# Bug with imap.hostnet.nl:993
		#self.sessionRenogotiation = xmldoc.getElementsByTagName('sessionRenegotiation')[0].getAttribute('canBeClientInitiated')
		self.sessionResumption = xmldoc.getElementsByTagName('sessionResumptionWithSessionIDs')[0].getAttribute('isSupported')
		if len(xmldoc.getElementsByTagName('sslv2')) > 0:
			if len(xmldoc.getElementsByTagName('sslv2')[0].getElementsByTagName('acceptedCipherSuites')) > 0:
				if(len(xmldoc.getElementsByTagName('sslv2')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite')) > 0):
					self.sslv2Enabled = True
					for suite in xmldoc.getElementsByTagName('sslv2')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite'):
						self.sslv2CipherSuites[suite.getAttribute('name')] = 0
						if(suite.getAttribute('keySize') != 'Anon'):
							self.sslv2CipherSuites[suite.getAttribute('name')] = int(suite.getAttribute('keySize').split()[0])
		if(len(xmldoc.getElementsByTagName('sslv3')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite')) > 0):
			self.sslv3Enabled = True
			for suite in xmldoc.getElementsByTagName('sslv3')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite'):
				self.sslv3CipherSuites[suite.getAttribute('name')] = 0
				if(suite.getAttribute('keySize') != 'Anon'):
					self.sslv3CipherSuites[suite.getAttribute('name')] = int(suite.getAttribute('keySize').split()[0])
		if(len(xmldoc.getElementsByTagName('tlsv1')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite')) > 0):
			self.tlsv1_0Enabled = True
			for suite in xmldoc.getElementsByTagName('tlsv1')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite'):
				self.tlsv1_0CipherSuites[suite.getAttribute('name')] = 0
				if(suite.getAttribute('keySize') != 'Anon'):
					self.tlsv1_0CipherSuites[suite.getAttribute('name')] = int(suite.getAttribute('keySize').split()[0])
		if(len(xmldoc.getElementsByTagName('tlsv1_1')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite')) > 0):
			self.tlsv1_1Enabled = True
			for suite in xmldoc.getElementsByTagName('tlsv1_1')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite'):
				if(suite.getAttribute('keySize').split()[0] == 'Anon'):
					self.tlsv1_1CipherSuites[suite.getAttribute('name')] = 0
				else:
					self.tlsv1_1CipherSuites[suite.getAttribute('name')] = int(suite.getAttribute('keySize').split()[0])
		if(len(xmldoc.getElementsByTagName('tlsv1_2')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite')) > 0):
			self.tlsv1_2Enabled = True
			for suite in xmldoc.getElementsByTagName('tlsv1_2')[0].getElementsByTagName('acceptedCipherSuites')[0].getElementsByTagName('cipherSuite'):
				self.tlsv1_2CipherSuites[suite.getAttribute('name')] = 0
				if(suite.getAttribute('keySize') != 'Anon'):
					self.tlsv1_2CipherSuites[suite.getAttribute('name')] = int(suite.getAttribute('keySize').split()[0])
		return True
