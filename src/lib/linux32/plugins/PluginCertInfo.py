#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         PluginCertInfo.py
# Purpose:      Verifies the target server's certificate validity against
#               Mozilla's trusted root store, and prints relevant fields of the
#               certificate.
#
# Author:       aaron, alban
#
# Copyright:    2012 SSLyze developers
#
#   SSLyze is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   SSLyze is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with SSLyze.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from os.path import join, dirname
import imp
from xml.etree.ElementTree import Element

from plugins import PluginBase
from utils.ThreadPool import ThreadPool
from utils.SSLyzeSSLConnection import create_sslyze_connection
from nassl import X509_NAME_MISMATCH, X509_NAME_MATCHES_SAN, X509_NAME_MATCHES_CN
from nassl.SslClient import ClientCertificateRequested


TRUST_STORES_PATH = join(join(dirname(PluginBase.__file__), 'data'), 'trust_stores')

# We use the Mozilla store for additional things: OCSP and EV validation
MOZILLA_STORE_PATH = join(TRUST_STORES_PATH, 'mozilla.pem')

AVAILABLE_TRUST_STORES = \
    { MOZILLA_STORE_PATH :                       'Mozilla NSS - 09/2013',
      join(TRUST_STORES_PATH, 'microsoft.pem') : 'Microsoft - 11/2013',
      join(TRUST_STORES_PATH, 'apple.pem') :     'Apple - OS X 10.9.0',
      join(TRUST_STORES_PATH, 'java.pem') :      'Java 7 - Update 25'}


# Import Mozilla EV OIDs
MOZILLA_EV_OIDS = imp.load_source('mozilla_ev_oids',
                                  join(TRUST_STORES_PATH,  'mozilla_ev_oids.py')).MOZILLA_EV_OIDS



class PluginCertInfo(PluginBase.PluginBase):

    interface = PluginBase.PluginInterface(title="PluginCertInfo", description=(''))
    interface.add_command(
        command="certinfo",
        help= "Verifies the target server's certificate validity against "
            "various trust stores, checks for support for OCSP stapling, and "
            "prints relevant fields of "
            "the certificate. CERTINFO should be 'basic' or 'full'.",
        dest="certinfo")

    FIELD_FORMAT = '      {0:<35}{1}'.format
    TRUST_FORMAT = '\"{0}\" CA Store:'.format


    def process_task(self, target, command, arg):

        if arg == 'basic':
            textFunction  = self._get_basic_text
        elif arg == 'full':
            textFunction = self._get_full_text
        else:
            raise Exception("PluginCertInfo: Unknown command.")

        (host, _, _, _) = target
        threadPool = ThreadPool()

        for (storePath, _) in AVAILABLE_TRUST_STORES.iteritems():
            # Try to connect with each trust store
            threadPool.add_job((self._get_cert, (target, storePath)))

        # Start processing the jobs
        threadPool.start(len(AVAILABLE_TRUST_STORES))

        # Store the results as they come
        (verifyDict, verifyDictErr, x509Cert, ocspResp)  = ({}, {}, None, None)

        for (job, result) in threadPool.get_result():
            (_, (_, storePath)) = job
            (x509Cert, verifyStr, ocspResp) = result
            # Store the returned verify string for each trust store
            storeName = AVAILABLE_TRUST_STORES[storePath]
            verifyDict[storeName] = verifyStr

        if x509Cert == None:
            # This means none of the connections were successful. Get out
            for (job, exception) in threadPool.get_error():
                raise exception

        # Store thread pool errors
        for (job, exception) in threadPool.get_error():
            (_, (_, storePath)) = job
            errorMsg = str(exception.__class__.__name__) + ' - ' \
                        + str(exception)

            storeName = AVAILABLE_TRUST_STORES[storePath]
            verifyDictErr[storeName] = errorMsg

        threadPool.join()


        # Results formatting
        # Text output - certificate info
        outputTxt = [self.PLUGIN_TITLE_FORMAT('Certificate - Content')]
        outputTxt.extend(textFunction(x509Cert))


        # Text output - trust validation
        outputTxt.extend(['', self.PLUGIN_TITLE_FORMAT('Certificate - Trust')])

        # Hostname validation
        if self._shared_settings['sni']:
            outputTxt.append(self.FIELD_FORMAT("SNI enabled with virtual domain:",
                                               self._shared_settings['sni']))
        # TODO: Use SNI name for validation when --sni was used
        hostValDict = {
            X509_NAME_MATCHES_SAN : 'OK - Subject Alternative Name matches',
            X509_NAME_MATCHES_CN :  'OK - Common Name matches',
            X509_NAME_MISMATCH :    'FAILED - Certificate does NOT match ' + host
        }
        outputTxt.append(self.FIELD_FORMAT("Hostname Validation:",
                                            hostValDict[x509Cert.matches_hostname(host)]))

        # Path validation that was successful
        for (storeName, verifyStr) in verifyDict.iteritems():
            verifyTxt = 'OK - Certificate is trusted' if (verifyStr in 'ok') else 'FAILED - Certificate is NOT Trusted: ' + verifyStr

            # EV certs - Only Mozilla supported for now
            if (verifyStr in 'ok') and ('Mozilla' in storeName):
                if (self._is_ev_certificate(x509Cert)):
                    verifyTxt += ', Extended Validation'
            outputTxt.append(self.FIELD_FORMAT(self.TRUST_FORMAT(storeName), verifyTxt))


        # Path validation that ran into errors
        for (storeName, errorMsg) in verifyDictErr.iteritems():
            verifyTxt = 'ERROR: ' + errorMsg
            outputTxt.append(self.FIELD_FORMAT(self.TRUST_FORMAT(storeName), verifyTxt))


        # Text output - OCSP stapling
        outputTxt.extend(['', self.PLUGIN_TITLE_FORMAT('Certificate - OCSP Stapling')])
        outputTxt.extend(self._get_ocsp_text(ocspResp))


        # XML output
        outputXml = Element(command, argument = arg, title = 'Certificate Information')

        # XML output - certificate info:  always return the full certificate
        certAttrib = { 'sha1Fingerprint' : x509Cert.get_SHA1_fingerprint() }
        if self._shared_settings['sni']:
            certAttrib['suppliedServerNameIndication'] = self._shared_settings['sni']

        certXml = Element('certificate', attrib = certAttrib)

        # Add certificate in PEM format
        PEMcertXml = Element('asPEM')
        PEMcertXml.text = x509Cert.as_pem().strip()
        certXml.append(PEMcertXml)

        for (key, value) in x509Cert.as_dict().items():
            certXml.append(_keyvalue_pair_to_xml(key, value))

        outputXml.append(certXml)


        # XML output - trust
        trustXml = Element('certificateValidation')

        # Hostname validation
        hostValBool = 'False' if (x509Cert.matches_hostname(host) == X509_NAME_MISMATCH) \
                              else 'True'
        hostXml = Element('hostnameValidation', serverHostname = host,
                           certificateMatchesServerHostname = hostValBool)
        trustXml.append(hostXml)

        # Path validation - OK
        for (storeName, verifyStr) in verifyDict.iteritems():
            pathXmlAttrib = { 'usingTrustStore' : storeName,
                              'validationResult' : verifyStr}

            # EV certs - Only Mozilla supported for now
            if (verifyStr in 'ok') and ('Mozilla' in storeName):
                    pathXmlAttrib['isExtendedValidationCertificate'] = str(self._is_ev_certificate(x509Cert))

            trustXml.append(Element('pathValidation', attrib = pathXmlAttrib))

        # Path validation - Errors
        for (storeName, errorMsg) in verifyDictErr.iteritems():
            pathXmlAttrib = { 'usingTrustStore' : storeName,
                              'error' : errorMsg}

            trustXml.append(Element('pathValidation', attrib = pathXmlAttrib))


        outputXml.append(trustXml)


        # XML output - OCSP Stapling
        if ocspResp is None:
            oscpAttr =  {'error' : 'Server did not send back an OCSP response'}
            ocspXml = Element('ocspStapling', attrib = oscpAttr)
        else:
            oscpAttr =  {'isTrustedByMozillaCAStore' : str(ocspResp.verify(MOZILLA_STORE_PATH))}
            ocspXml = Element('ocspResponse', attrib = oscpAttr)

            for (key, value) in ocspResp.as_dict().items():
                ocspXml.append(_keyvalue_pair_to_xml(key,value))

        outputXml.append(ocspXml)

        return PluginBase.PluginResult(outputTxt, outputXml)


# FORMATTING FUNCTIONS

    def _get_ocsp_text(self, ocspResp):

        if ocspResp is None:
            return [self.FIELD_FORMAT('Server did not send back an OCSP response.', '')]

        ocspRespDict = ocspResp.as_dict()
        ocspRespTrustTxt = 'Response is Trusted' if ocspResp.verify(MOZILLA_STORE_PATH) \
            else 'Response is NOT Trusted'

        ocspRespTxt = [ \
            self.FIELD_FORMAT('OCSP Response Status:', ocspRespDict['responseStatus']),
            self.FIELD_FORMAT('Validation w/ Mozilla\'s CA Store:', ocspRespTrustTxt),
            self.FIELD_FORMAT('Responder Id:', ocspRespDict['responderID'])]

        if 'successful' not in ocspRespDict['responseStatus']:
            return ocspRespTxt

        ocspRespTxt.extend( [ \
            self.FIELD_FORMAT('Cert Status:', ocspRespDict['responses'][0]['certStatus']),
            self.FIELD_FORMAT('Cert Serial Number:', ocspRespDict['responses'][0]['certID']['serialNumber']),
            self.FIELD_FORMAT('This Update:', ocspRespDict['responses'][0]['thisUpdate']),
            self.FIELD_FORMAT('Next Update:', ocspRespDict['responses'][0]['nextUpdate'])])

        return ocspRespTxt


    @staticmethod
    def _is_ev_certificate(cert):
        certDict = cert.as_dict()
        try:
            policy = certDict['extensions']['X509v3 Certificate Policies']['Policy']
            if policy[0] in MOZILLA_EV_OIDS:
                return True
        except:
            return False
        return False


    def _get_full_text(self, cert):
        return [cert.as_text()]


    def _get_basic_text(self, cert):
        certDict = cert.as_dict()

        try: # Extract the CN if there's one
            commonName = certDict['subject']['commonName']
        except KeyError:
            commonName = 'None'

        basicTxt = [ \
            self.FIELD_FORMAT("SHA1 Fingerprint:", cert.get_SHA1_fingerprint()),
            self.FIELD_FORMAT("Common Name:", commonName),
            self.FIELD_FORMAT("Issuer:", certDict['issuer']),
            self.FIELD_FORMAT("Serial Number:", certDict['serialNumber']),
            self.FIELD_FORMAT("Not Before:", certDict['validity']['notBefore']),
            self.FIELD_FORMAT("Not After:", certDict['validity']['notAfter']),
            self.FIELD_FORMAT("Signature Algorithm:", certDict['signatureAlgorithm']),
            self.FIELD_FORMAT("Key Size:", certDict['subjectPublicKeyInfo']['publicKeySize'])]

        try: # Print the SAN extension if there's one
            basicTxt.append(self.FIELD_FORMAT('X509v3 Subject Alternative Name:',
                                              certDict['extensions']['X509v3 Subject Alternative Name']))
        except KeyError:
            pass

        return basicTxt


    def _get_cert(self, target, storePath):
        """
        Connects to the target server and uses the supplied trust store to
        validate the server's certificate. Returns the server's certificate and
        OCSP response.
        """
        (_, _, _, sslVersion) = target
        sslConn = create_sslyze_connection(target, self._shared_settings,
                                           sslVersion,
                                           sslVerifyLocations=storePath)

        # Enable OCSP stapling
        sslConn.set_tlsext_status_ocsp()

        try: # Perform the SSL handshake
            sslConn.connect()

            ocspResp = sslConn.get_tlsext_status_ocsp_resp()
            x509Cert = sslConn.get_peer_certificate()
            (_, verifyStr) = sslConn.get_certificate_chain_verify_result()

        except ClientCertificateRequested: # The server asked for a client cert
            # We can get the server cert anyway
            ocspResp = sslConn.get_tlsext_status_ocsp_resp()
            x509Cert = sslConn.get_peer_certificate()
            (_, verifyStr) = sslConn.get_certificate_chain_verify_result()

        finally:
            sslConn.close()

        return (x509Cert, verifyStr, ocspResp)


# XML generation
def _create_xml_node(key, value=''):
    key = key.replace(' ', '').strip() # Remove spaces
    key = key.replace('/', '').strip() # Remove slashes (S/MIME Capabilities)

    # Things that would generate invalid XML
    if key[0].isdigit(): # Tags cannot start with a digit
            key = 'oid-' + key

    xml_node = Element(key)
    xml_node.text = value.decode( "utf-8" ).strip()
    return xml_node


def _keyvalue_pair_to_xml(key, value=''):

    if type(value) is str: # value is a string
        key_xml = _create_xml_node(key, value)

    elif type(value) is int:
        key_xml = _create_xml_node(key, str(value))

    elif value is None: # no value
        key_xml = _create_xml_node(key)

    elif type(value) is list:
        key_xml = _create_xml_node(key)
        for val in value:
            key_xml.append(_keyvalue_pair_to_xml('listEntry', val))

    elif type(value) is dict: # value is a list of subnodes
        key_xml = _create_xml_node(key)
        for subkey in value.keys():
            key_xml.append(_keyvalue_pair_to_xml(subkey, value[subkey]))
    else:
        raise Exception()

    return key_xml

