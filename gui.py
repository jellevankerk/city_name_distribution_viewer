import tkinter as tk
import geopandas as gpd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parameters import  SEED, PATH_TO_GEODATA

from src.extraction import WikiDataQueryResults
from src.queries import settlement_query, provinces_query
from src.transform import get_latitude_and_longitude, get_geodataframe

class GeopandasGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.fig, _ = plt.subplots(figsize=(18, 18))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_placeholder)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        
        self.__extract_data()
        self.__transform_data()
    
    def __extract_data(self):
        query1 = WikiDataQueryResults(settlement_query)
        query2 = WikiDataQueryResults(provinces_query)

        self.settlement_df = query1.load_as_dataframe()
        self.provinces = query2.load_as_list(key = 'provinceLabel')
        self.shapefile = gpd.read_file(PATH_TO_GEODATA)
    
    def __transform_data(self):
        # Filter on provinces (cleaning step)
        self.settlement_df = self.settlement_df[self.settlement_df["provinceLabel"].isin(self.provinces)]

        # Get latitude and longitude
        get_latitude_and_longitude(self.settlement_df)

    def create_widgets(self):
        # Entry widget for substring filter
        self.filter_entry = tk.Entry(self)
        self.filter_entry.insert(0, "dijk") 
        self.filter_entry.pack(side="top")
        
        self.plot_button = tk.Button(self)
        self.plot_button["text"] = "Plot Shapefile"
        self.plot_button["command"] = self.plot_shapefile
        self.plot_button.pack(side="top")

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

        # Placeholder for the plot
        self.plot_placeholder = tk.Frame(self)
        self.plot_placeholder.pack(side='top', fill='both', expand=1)
        
    def plot_shapefile(self):
        # Remove any existing plots
        if self.fig is not None:
            self.fig.clf()
            self.canvas.get_tk_widget().destroy()

        # Filter shapefile by substring entered in the Entry widget
        substring = self.filter_entry.get()
        settlement_sub_geo_df = self.settlement_df[self.settlement_df['settlementLabel'].str.contains(substring)]
        
        
        self.fig, ax = plt.subplots(figsize=(18, 18))
        
        self.shapefile.plot(ax=ax, alpha=0.4, color="grey")
        
        # Plot the settlements with the given substring in their name
        settlement_sub_geo_df = get_geodataframe(settlement_sub_geo_df)
        settlement_sub_geo_df.plot(column="provinceLabel", ax=ax, legend=True)
        
        # Annotate the settlements on the map
        for i, item in settlement_sub_geo_df.sample(len(settlement_sub_geo_df)//10, random_state = SEED).iterrows():
            ax.annotate(item.settlementLabel, (item.longitude, item.latitude))
        
        # Set the plot title and show the plot
        plt.title(f"Places with '{substring}' in name")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_placeholder)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        
           
    def destroy(self):
        # Properly close any existing plots before destroying the application
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.master.quit()

root = tk.Tk()
app = GeopandasGUI(master=root)
app.mainloop()

