import urllib.parse
import urllib.request
import http.cookiejar
from lxml import etree, objectify
from exception import RequestError
from utils import generate_nonce, md5hash


def build_basic_element(tag, attributes={}, subelements=[]):
    nsmap = {'c': 'http://www.tellervo.org/schema/1.0',
             'gml': 'http://www.opengis.net/gml',
             'tridas': 'http://www.tridas.org/1.2.2',
             'xlink': 'http://www.w3.org/1999/xlink'}
    tag_string = '{%s}%s' % (nsmap['c'], tag)
    root = objectify.Element(tag_string, nsmap = nsmap, **attributes)
    for se in subelements:
        root.append(se)
    return root

def build_xmlrequest(request_attributes={}, subelements=[]):
    """Build an XML request string
    """
    request_element = build_basic_element('request', request_attributes, subelements)
    root = build_basic_element('tellervo', subelements = [request_element])
    objectify.deannotate(root, xsi_nil = True)
    etree.cleanup_namespaces(root)
    return etree.tostring(root)

def build_loginrequest(username, client_nonce, server_nonce, bighash, sequence):
    login_attributes = {'username': username,
                        'cnonce': client_nonce,
                        'snonce': server_nonce,
                        'hash': bighash,
                        'seq': sequence}
    auth_element = build_basic_element("authenticate", login_attributes)
    request = build_xmlrequest({'type': 'securelogin'}, [auth_element])
    return request

class Response(object):
    def __init__(self, http_response):
        self.content = None
        self.status = None
        self.message = None
        self.messagecode = None
        self.content = objectify.fromstring(http_response.read())
        self.status = self.content.find('.//{http://www.tellervo.org/schema/1.0}status').text
        if self.status != "OK":
            message_element = self.content.find('.//{http://www.tellervo.org/schema/1.0}message')
            message_text = message_element.text
            message_code = message_element.attrib["code"]
            raise RequestError(message_text, message_code)


class Connection(object):
    def __init__(self, server_url, username, password):
        self._serverurl = server_url
        self._username = username
        self._password = md5hash(password)
        self._cookiejar = http.cookiejar.CookieJar()
        cookieprocessor = urllib.request.HTTPCookieProcessor(self._cookiejar)
        self._urlopener = urllib.request.build_opener(cookieprocessor)
        self.login()

    def read_record(id, record_type, format="standard"):


    def execute(self, xmlrequest):
        """Package a string XML request and submit it to the server"""
        request_data = {'xmlrequest': xmlrequest}
        payload = urllib.parse.urlencode(request_data).encode('utf-8')
        response = Response(self._urlopener.open(self._serverurl, payload))
        return response

    def logout(self):
        return self.execute(build_xmlrequest("logout"))

    def login(self):
        server_nonce, nonce_seq = self._request_nonce()
        client_nonce = generate_nonce(21)
        to_hash = ":".join([self._username, self._password, server_nonce, client_nonce])
        out_hash = md5hash(to_hash)
        login_request = build_loginrequest(self._username,
            client_nonce, server_nonce, out_hash, nonce_seq)
        self.execute(login_request)

    def _request_nonce(self):
        nonce_response = self.execute(build_xmlrequest({'type': 'nonce'})).content
        nonce_element = nonce_response.find('.//{http://www.tellervo.org/schema/1.0}nonce')
        server_nonce = nonce_element.text
        nonce_seq = nonce_element.attrib['seq']
        return (server_nonce, nonce_seq)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # See https://docs.python.org/3.5/library/stdtypes.html#typecontextmanager
        self.logout()