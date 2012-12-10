#!/usr/bin/env python3
#
# Copyright (c) 2011 David Johansen <david@makewhatis.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# <http://www.opensource.org/licenses/mit-license.php>
"""
Python wrapper for the dnsmadeeasy RESTful api
"""

import httplib2
import json
from time import strftime, gmtime
import hashlib
import hmac


class dme:
    """
    Create dnsmadeeasy object
    """
    def __init__(self, apikey, secret):
        self.api = apikey
        self.secret = secret
        # self.baseurl = "http://api.sandbox.dnsmadeeasy.com/V1.2/"
        # use below url for real api access. above is sandbox.
        self.baseurl = "http://api.dnsmadeeasy.com/V1.2/"
    def _headers(self):
        rightnow = self._get_date()
        hashstring = self._create_hash(rightnow)
        headers = {'x-dnsme-apiKey' : self.api, 'x-dnsme-hmac' : hashstring, 'x-dnsme-requestDate' : rightnow, 'content-type' : 'application/json' , 'accept' : 'application/json' }
        return headers
    
    def _get_date(self):
        return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    def _create_hash(self, rightnow):
        return hmac.new(self.secret.encode(), rightnow.encode(), hashlib.sha1).hexdigest()
    
    def _rest_connect(self, resource, method, data=""):
        http = httplib2.Http()
        print(data)
        response, content = http.request(self.baseurl + resource, method, body=data, headers=self._headers())
        if (response['status'] == "200" or  response['status'] == "201" ):
            if content:
                jsonresponse = json.loads(content.decode('utf-8'))
                return jsonresponse
            else:
                return response
        else:
            print(content)
            raise Exception("Error talking to dnsmadeeasy: " + response['status'])               

    ########################################################################
    #  /domains
    ########################################################################

    def list_domains(self):
        domains = []
        jsonresponse = self._rest_connect('domains', 'GET')
        for domain in jsonresponse['list']:
            domains.append(domain)
        return domains
    
    #!!!!! Following function deletes all of your domains. Use that with caution. Why anybody would need this, who knows.!!!!!!!
    
    def delete_domains(self):
        jsonresponse = self._rest_connect('domains', 'DELETE')
        return jsonresponse
 
    ########################################################################
    #  /domains/{domainName}
    ########################################################################

    def get_domain(self, domain):
        domain_info = []
        jsonresponse = self._rest_connect('domains/' + domain, 'GET' )
        for info in jsonresponse.items():
            domain_info.append(info)
        return domain_info
    
    def delete_domain(self, domain):
        jsonresponse = self._rest_connect('domains/' + domain, 'DELETE')
        return jsonresponse
    
    def add_domain(self, domain):
        jsonresponse = self._rest_connect('domains/' + domain, 'PUT')
        return jsonresponse
 
    ########################################################################
    #  /domains/{domainName}/records
    ########################################################################

  
    def get_records(self, domain):
        records = []
        jsonresponse = self._rest_connect('domains/' + domain + '/records', 'GET')
        for record in jsonresponse:
            records.append(record)
        return records
        
    def add_record(self, domain, **kwargs):
        data = {'name': None,
                'data': None,
                'type': 'A',
                'gtdLocation': None,
                'ttl': 1800}
        data.update(kwargs)
        jsonresponse = self._rest_connect('domains/' + domain + '/records', 'POST', json.dumps(data))
        return jsonresponse

    ########################################################################
    #  /domains/{domainName}/records/{recordId}
    ########################################################################
    
    def get_record_byid(self, domain, id):
        jsonresponse = self._rest_connect('domains/' + domain + '/records/' + id, 'GET')
        return jsonresponse
        
    def delete_record_byid(self, domain, id):
        response = self._rest_connect('domains/' + domain + '/records/' + id, 'DELETE')
        return response
        
    
    def update_record_byid(self, domain, id, **kwargs):
        data = self.get_record_byid(domain, id)
        data.update(kwargs)
        response = self._rest_connect('domains/' + domain + '/records/' + id, 'PUT', json.dumps(data))
        return response
       

