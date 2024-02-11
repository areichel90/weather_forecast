import requests, pprint
import numpy as np
import pandas as pd
from weather_plots import plot_temp, plot_forecast_interactive

class location():
    def __init__(self, pos):
        self.lat, self.lon = pos[0], pos[1]
        self.loc_string = str(self.lat) + "," + str(self.lon)
        self.json = requests.get(f"https://api.weather.gov/points/{self.loc_string}").json()
        self.reqProp = self.json["properties"]
        #self.forecast_url = self.reqProp["forecastGridData"]
        self.grid_data = requests.get(self.reqProp["forecastGridData"]).json()
        self.data_props = self.grid_data["properties"]

    def get_forecast(self):
        #self.forecast = requests.get(self.forecast_url).json()
        self.forecastTemps = self.data_props['apparentTemperature']['values']
        self.snowfallAmount = self.data_props['snowfallAmount']['values']

def c_to_f(c):
    return 1.8*c + 32

def format_data(data_in):
    df_in = pd.DataFrame(data_in)
    df_in["validTime"] = df_in.validTime.apply(lambda x: x.split("/")[0].split("+")[0])
    df_in["dateTime"] = pd.to_datetime(df_in.validTime, format="%Y-%m-%dT%H:%M:%S")
    df_in = df_in.set_index("dateTime").drop("validTime", axis=1)
    return df_in


def main(loc:location):
    loc.get_forecast()
    temps = loc.forecastTemps
    snow = pd.DataFrame(loc.snowfallAmount)
    # create dataframe from individual data 'series'

    # format temperature forecast
    df_temps = format_data(temps)
    df_temps["temperature"] = [c_to_f(i) for i in df_temps.value]
    # format snowfall forecast
    df_snow = format_data(snow)
    df_snow["snowfall"] = df_snow.value/25.4  # mm / in
    # combine all data field(s)
    df_data = df_temps[["temperature"]].join(df_snow["snowfall"])

    df_data['day'] = df_data.index.day
    df_data.snowfall.fillna(0, inplace=True)
    df_data['cum_snow'] = df_data.groupby('day')['snowfall'].transform(pd.Series.cumsum)


    # plot temp forecast
    #plot_temp(df_data)
    plot_forecast_interactive(df_data)


if __name__ == "__main__":
    # instantiate location
    latlon = [42.68, -71.13]  # north andover
    loc = location(latlon)

    main(loc)

