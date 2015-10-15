from lxml import etree, objectify
from utils import make_validated_parser

TRIDASSCHEMA_URL = "http://www.tridas.org/1.2.2/tridas-1.2.2.xsd"

# Read tridas file.
# tridas_schema = etree.XMLSchema(file = TRIDASSCHEMA_URL)
# tridas_parser = objectify.makeparser(schema = tridas_schema)
tridas_parser = make_validated_parser(TRIDASSCHEMA_URL)

tree_ex = objectify.parse(SIMPLEEXAMPLE_PATH)
with open(SIMPLEEXAMPLE_PATH, "rb") as fl:
    schema_ex = objectify.fromstring(fl.read(), tridas_parser)
print(schema_ex.project.title)
# Seems to work very well.
# Line below doesn't seem to work. Produces etree.
# schema_ex = objectify.parse(SIMPLEEXAMPLE_PATH, tridas_parser)
