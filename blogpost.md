# Visualizing City Name Distribution with Python
When looking at a map, it's easy to take for granted the names of the cities and towns that dot the landscape. However, these names can provide valuable insight into the history, culture, and languages of a region. In this post, we'll explore how to use Python and data from Wikidata to visualize the distribution of settlements names in the Netherlands.

## Prerequisites
To follow this tutorial, you will need the following:

- Python 3.8 or higher
- The geopandas, pandas, matplotlib, SPARQLWrapper, and mapclassify Python packages
- Access to the internet to access the Wikidata API

All code use here can be found at my [github](https://github.com/jellevankerk/city_name_distribution_viewer)

## Getting Started
To get started, create a new Python script and import the required packages:

```
import pandas as pd
```

Next, define the Wikidata queries that we will use to extract the data. We will use two queries: one to get all settlements in the Netherlands, and another to get the provinces of the Netherlands.

```python
# Gets all cities/villages and settlements from the Netherlands (Q55) (municipality of the Netherlands (Q2039348))
settlement_query = """SELECT ?settlement ?settlementLabel ?municipality ?municipalityLabel ?province ?provinceLabel ?country ?countryLabel ?coordinates WHERE {

    ?municipality wdt:P31 wd:Q2039348 . # sovereign state
    ?settlement wdt:P625 ?coordinates.
    ?municipality wdt:P1383 ?settlement.
    ?municipality wdt:P17 ?country.
    ?municipality wdt:P131 ?province.
  

    SERVICE wikibase:label {
       bd:serviceParam wikibase:language "nl" 
    }
}"""

# Get all the provinces of the Netherlands
provinces_query =  """SELECT ?province ?provinceLabel WHERE {

    ?province wdt:P31 wd:Q134390 . # sovereign state


    SERVICE wikibase:label {
       bd:serviceParam wikibase:language "nl"
    }
}"""

```

## Extracting Data from Wikidata
We will use the WikiDataQueryResults class to extract the data from Wikidata. The WikiDataQueryResults class is a convenient way to query the Wikidata API and load the results into a Pandas DataFrame. We will also filter the results to only include settlements in the Netherlands and their associated provinces.

```python
import sys
import pandas as pd
from typing import List, Dict
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON

class WikiDataQueryResults:
    """
    A class that can be used to query data from Wikidata using SPARQL and return the results as a Pandas DataFrame or a list
    of values for a specific key.
    """
    def __init__(self, query: str):
        """
        Initializes the WikiDataQueryResults object with a SPARQL query string.

        :param query: A SPARQL query string.
        """
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

    def __transform2dicts(self, results: List[Dict]) -> List[Dict]:
        """
        Helper function to transform SPARQL query results into a list of dictionaries.

        :param results: A list of query results returned by SPARQLWrapper.
        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        new_results = []
        for result in results:
            new_result = {}
            for key in result:
                new_result[key] = result[key]['value']
            new_results.append(new_result)
        return new_results

    def load_as_dataframe(self) -> pd.DataFrame:
        """
        Executes the SPARQL query and returns the results as a Pandas DataFrame.

        :return: A Pandas DataFrame representing the query results.
        """
        results = self._load()
        return pd.DataFrame.from_dict(results)

    def load_as_list(self, key: str) -> List[str]:
        """
        Executes the SPARQL query and returns a list of values for a specific key.

        :param key: The key for which to retrieve values.
        :return: A list of string values for the specified key.
        """
        results = self._load()
        return [x[key] for x in results]

    def _load(self) -> List[Dict]:
        """
        Helper function that loads the data from Wikidata using the SPARQLWrapper library, and transforms the results into
        a list of dictionaries.

        :return: A list of dictionaries, where each dictionary represents a result row and has keys corresponding to the
        variables in the SPARQL SELECT clause.
        """
        results = self.sparql.query().convert()['results']['bindings']
        results = self.__transform2dicts(results)
        return results

```
```python
# Extract data from Wikidata
query1 = WikiDataQueryResults(settlement_query.format(country="Q55"))
query2 = WikiDataQueryResults(provinces_query)

settlement_df = query1.load_as_dataframe()
provinces = query2.load_as_list(key = 'provinceLabel')

# Filter on provinces
settlement_df = settlement_df[settlement_df["provinceLabel"].isin(provinces)]
```