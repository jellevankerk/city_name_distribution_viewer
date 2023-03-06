import sys
import pandas as pd
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON

class WikiDataQueryResults:
    def __init__(self, query):
        self.user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        self.endpoint_url = "https://query.wikidata.org/sparql"
        self.sparql = SPARQLWrapper(self.endpoint_url, agent=self.user_agent)
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
    
    @staticmethod
    def __transform2dicts(results):
        new_results = []
        for result in results:
            new_result = {}
            for key in result:
                new_result[key] = result[key]['value']
            new_results.append(new_result)
                
        return new_results
    
    def _load(self):
        results = self.sparql.query().convert()['results']['bindings']
        results = self.__transform2dicts(results)
        return results    
    
    def load_as_dataframe(self):
        results = self._load()
        return pd.DataFrame.from_dict(results)
    
    def load_as_list(self, key):
        results = self._load()
        return [x[key] for x in results]
    
    

