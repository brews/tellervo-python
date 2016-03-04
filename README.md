#tellervo-python

[![Travis-CI Build Status](https://travis-ci.org/brews/tellervo-python.svg?branch=master
)](https://travis-ci.org/brews/tellervo-python)

Python client to the Tellervo dendrochronology suite.

Note that this software is under development and may eat your pet hamster.

##Example
Here is a quick example that queries a Tellervo server for all samples that were sampled after 2015-01-01. The server replies with TRiDaS XML. We gather the fields that we want from the XML reply and stick the information into a list of dictionaries. nice Pandas DataFrame. To top things off, 

```python
import tellervo as tel

USERNAME = 'username'
TARGET_URL = "https://tellervo.example.edu/ourserver/"
# Password is entered when we setup the connection below.

# Build a search query.
# Here we're looking for a comprehensive sample form any sample with a
# sampling date is after 2015-01-01.
search_query = tel.build_searchrequest(return_object = 'sample', 
                                       search_name = 'samplingdate',
                                       search_operator = '>',
                                       search_value = '2015-01-01',
                                       results_format = 'comprehensive')

# Open connection to Tellervo server, throw it our query, close connection.
with tel.Connection(TARGET_URL, USERNAME, 'MyPassword!') as con:
    reply = con.execute(search_query)

# Parse TRiDaS XML from server. See `lxml` for details.
select_data = []
for site in reply.body.content.iterchildren():
    sample_dict = {'site_name': site.title.text,
                   'tree_name': site.element.title.text,
                   'tree_taxon': site.element.taxon.get('normal'),
                   'sample_name': site.element.sample.title.text}
    select_data.append(sample_dict)
```

Now we can take our `select_data` list and turn it into a Pandas DataFrame. To top things off, we sort the data by site name, tree name, and sample name.

```python
import pandas as pd

d = pd.DataFrame(select_data, dtype = 'str')
d = d.sort_values(by = ['site_name', 'tree_name', 'sample_name'])
```
