import pandas as pd
import geopandas as gpd


def get_latitude_and_longitude(df):
    df['latitude'] = df['coordinates'].str.extract(r'Point\(.*?\s(.*?)\)')
    df['longitude'] = df['coordinates'].str.extract(r'Point\((.*?)\s')
    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])
    
def get_geodataframe(df):
    geometry = gpd.points_from_xy(df.longitude, df.latitude)
    geo_df = gpd.GeoDataFrame(df[[x for x in list(df.columns) if 'Label' in x]+[ "longitude", "latitude"]], geometry=geometry)
    return geo_df