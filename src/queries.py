
#%% sparql Queries
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
#TODO Make Query more efficient
#TODO Make Query more flexible

# Get all the provinces of the Netherlands
provinces_query =  """SELECT ?province ?provinceLabel WHERE {

    ?province wdt:P31 wd:Q134390 . # sovereign state


    SERVICE wikibase:label {
       bd:serviceParam wikibase:language "nl"
    }
}"""

#TODO Make Query get country subdivision unrelated it has provinces, states or other