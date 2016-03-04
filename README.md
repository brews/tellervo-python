#tellervo-python

[![Travis-CI Build Status](https://travis-ci.org/brews/tellervo-python.svg?branch=master
)](https://travis-ci.org/brews/tellervo-python)

Python client to the [Tellervo dendrochronology suite](http://tellervo.org/).

Note that this software is under development. It may eat your pet hamster.

## Installation

Releases are in the [Python Package Index](https://pypi.python.org/pypi?:action=display&name=tellervo-python). You can install the package with `pip install tellervo-python`. This package requires a copy of Python 3.3 or more recent, so on some linux distros you might need to use `pip3`.

Bleeding-edge development can be found on [Github](https://github.com/brews/tellervo-python), if you like being in the danger zone.

##Example
Here is a quick example that queries a Tellervo server with a search request. The server replies with [TRiDaS XML](http://www.tridas.org/). We gather the fields we want from the XML reply and stick the information into a list of dictionaries.

```python
import tellervo as tel

USERNAME = 'username'
SERVER_URL = "https://tellervo.example.edu/ourserver/"
# Password is entered when we setup the connection below.

# Build a search query.
# Here we're looking for a comprehensive sample form any sample with a
# sampling date is after 2015-01-01.
search_query = tel.build_searchrequest(return_object = 'sample', 
                                       search_name = 'samplingdate',
                                       search_operator = '>',
                                       search_value = '2015-01-01',
                                       results_format = 'comprehensive')

# Open connection to Tellervo server, throw our query at it, close connection.
# Note that using the `with as` statement will close the connection to the
# server, even if something goes wrong.
with tel.Connection(SERVER_URL, USERNAME, 'MyPassword!') as con:
    reply = con.execute(search_query)

# Parse TRiDaS XML from server.
select_data = []
for site in reply.body.content.iterchildren():
    sample_dict = {'site_name': site.title.text,
                   'tree_name': site.element.title.text,
                   'tree_taxon': site.element.taxon.get('normal'),
                   'sample_name': site.element.sample.title.text}
    select_data.append(sample_dict)
```

For more on parsing the XML replies, see [lxml](http://lxml.de/).

If you want to refine things further, we can easily take our `select_data` list and turn it into a [pandas](http://pandas.pydata.org/) DataFrame. We then sort the data.

```python
import pandas as pd

d = pd.DataFrame(select_data, dtype = 'str')
d = d.sort_values(by = ['site_name', 'tree_name', 'sample_name'])
```
