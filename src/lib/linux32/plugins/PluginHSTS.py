#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         PluginHSTS.py
# Purpose:      Checks if the server supports RFC 6797 HTTP Strict Transport
#               Security by checking if the server responds with the
#               Strict-Transport-Security field in the header.
#
#               Note: There is currently no support for hsts pinning.
#
#               This plugin is based on the plugin written by Tom Samstag
#               (tecknicaltom) and reworked, integrated and adapted to the
#               new sslyze plugin API by Joachim Strömbergson.
#
# Author:       tecknicaltom, joachims, alban
#
# Copyright:    2013 SSLyze developers
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

from xml.etree.ElementTree import Element
from utils.HTTPResponseParser import parse_http_response
from utils.SSLyzeSSLConnection import create_sslyze_connection
from plugins import PluginBase


class PluginHSTS(PluginBase.PluginBase):

    interface = PluginBase.PluginInterface(title="PluginHSTS", description=(''))
    interface.add_command(
        command="hsts",
        help="Checks support for HTTP Strict Transport Security "
             "(HSTS) by collecting any Strict-Transport-Security field present in "
             "the HTTP response sent back by the server.",
        dest=None)


    def process_task(self, target, command, args):


        if self._shared_settings['starttls']:
            raise Exception('Cannot use --hsts with --starttls.')

        FIELD_FORMAT = '      {0:<35}{1}'.format

        hsts_supported = self._get_hsts_header(target)
        if hsts_supported:
            hsts_timeout = hsts_supported
            hsts_supported = True

        # Text output
        cmd_title = 'HTTP Strict Transport Security'
        txt_result = [self.PLUGIN_TITLE_FORMAT(cmd_title)]
        if hsts_supported:
            txt_result.append(FIELD_FORMAT("Supported:", hsts_timeout))
        else:
            txt_result.append(FIELD_FORMAT("Not supported.", ""))

        # XML output
        xml_hsts_attr = {'hsts_header_found': str(hsts_supported)}
        if hsts_supported:
            xml_hsts_attr['hsts_header'] = hsts_timeout
        xml_hsts = Element('hsts', attrib = xml_hsts_attr)

        xml_result = Element(self.__class__.__name__, command = command,
                             title = cmd_title)
        xml_result.append(xml_hsts)

        return PluginBase.PluginResult(txt_result, xml_result)



    def _get_hsts_header(self, target):

        hstsHeader = None
        HTTP_GET_REQ = 'GET / HTTP/1.0\r\nHost: {0}\r\nConnection: close\r\n\r\n'.format(target[0])
        sslConn = create_sslyze_connection(target, self._shared_settings)

        # Perform the SSL handshake
        sslConn.connect()

        sslConn.write(HTTP_GET_REQ)
        httpResp = parse_http_response(sslConn.read(2048))
        sslConn.close()
        if httpResp.version == 9 :
            # HTTP 0.9 => Probably not an HTTP response
            raise Exception('Server did not return an HTTP response')
        else:
            hstsHeader = httpResp.getheader('strict-transport-security', None)
        return hstsHeader


