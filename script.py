#%% Imports
import geopandas as gpd

from src.extraction import WikiDataQueryResults
from src.queries import settlement_query, provinces_query
from src.transform import get_latitude_and_longitude, get_geodataframe
from src.visualize import plot_on_map

from parameters import  SUBSTRING, PATH_TO_GEODATA, SEED

#%% Extract data from WikiData
query1 = WikiDataQueryResults(settlement_query)
query2 = WikiDataQueryResults(provinces_query)

settlement_df = query1.load_as_dataframe()
provinces = query2.load_as_list(key = 'provinceLabel')

print(settlement_df.head())
print(provinces)

#%% Transform Data
# Filter on provinces (cleaning step)
settlement_df = settlement_df[settlement_df["provinceLabel"].isin(provinces)]

# Get latitude and longitude
get_latitude_and_longitude(settlement_df)

#%% Get Geodata and Geodataframe
geodata = gpd.read_file(PATH_TO_GEODATA)

# Filter on SUBSTRING
settlement_sub_geo_df = settlement_df[settlement_df['settlementLabel'].str.contains(SUBSTRING)]

# Transform to Geodata_dataframe
settlement_sub_geo_df = get_geodataframe(settlement_sub_geo_df)

#%% Visualization
plot_on_map(settlement_sub_geo_df, geodata, SUBSTRING, SEED)