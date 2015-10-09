import random
import string
from hashlib import md5
from lxml import etree, objectify

def md5hash(s):
    """MD5 hash a string, return hex"""
    return md5(s.encode('utf-8')).hexdigest()

def make_validated_parser(schemafile):
    """Create a validated XML parser from input schema file/URL"""
    xml_schema = etree.XMLSchema(file = schemafile)
    xml_parser = objectify.makeparser(schema = xml_schema)
    return xml_parser

def generate_nonce(size=21, chars=string.ascii_lowercase+string.digits):
    """Create an alphanumeric nonce"""
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
