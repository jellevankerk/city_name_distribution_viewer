import matplotlib.pyplot as plt


def plot_on_map(geo_df, geodata, substring, random_state):
    fig, ax = plt.subplots(figsize=(24, 18))
    geodata.plot(ax=ax, alpha=0.4, color="grey")
    geo_df.plot(column="provinceLabel", ax=ax, legend=True)
    for i, item in geo_df.sample(len(geo_df)//10, random_state = random_state).iterrows():
        ax.annotate(item.settlementLabel, (item.longitude, item.latitude))
    plt.title(f"Places with '{substring}' in name")
    plt.show()