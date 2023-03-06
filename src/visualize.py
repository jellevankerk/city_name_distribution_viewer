import matplotlib.pyplot as plt


def plot_settlements_on_map(geo_df, geodata, substring, random_state):
    """
    Plot a map of settlements with a given substring in their name.

    Args:
        geo_df (GeoDataFrame): A GeoDataFrame containing information about the settlements.
        geodata (GeoDataFrame): A GeoDataFrame containing the map data.
        substring (str): The substring to search for in the settlement names.
        random_state (int): A random seed for reproducibility.

    Returns:
        None. Displays a plot of the settlements on a map.
    """
    # Create the figure and axis for the plot
    _, ax = plt.subplots(figsize=(24, 18))

    # Plot the map data
    geodata.plot(ax=ax, alpha=0.4, color="grey")

    # Plot the settlements with the given substring in their name
    geo_df[geo_df['settlementLabel'].str.contains(substring)].plot(column="provinceLabel", ax=ax, legend=True)

    # Annotate the settlements on the map
    for i, item in geo_df.sample(len(geo_df)//10, random_state = random_state).iterrows():
        ax.annotate(item.settlementLabel, (item.longitude, item.latitude))

    # Set the plot title and show the plot
    plt.title(f"Places with '{substring}' in name")
    plt.show()