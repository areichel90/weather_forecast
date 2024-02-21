import datetime

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
        self.lastUpdated = datetime.datetime.fromisoformat(self.data_props["updateTime"]) - datetime.timedelta(hours=5)
        self.location = self.grid_data["geometry"]["coordinates"]

        # --- format locations
        df_loc = pd.DataFrame(np.array(self.location).reshape(5, 2))
        self.actual_loc = [round(df_loc[i].mean(), 5) for i in df_loc]

    def get_forecast(self):
        print(f"fetching forecast for location: self: [{self.lat}, {self.lon}]")
        self.apparentTemps = self.data_props['apparentTemperature']['values']
        self.forecastTemps = self.data_props["temperature"]['values']
        self.windchillTemps = self.data_props["windChill"]['values']
        self.snowfallAmount = self.data_props['snowfallAmount']['values']
        self.cloudCover = self.data_props["skyCover"]['values']
        self.windSpeed = self.data_props["windSpeed"]['values']
        self.percPrecip = self.data_props["probabilityOfPrecipitation"]['values']



def c_to_f(c):
    return 1.8*c + 32

def format_data(data_in, verbose=False):
    df_in = pd.DataFrame(data_in)
    if verbose: print(df_in)

    df_in["validTime"] = df_in.validTime.apply(lambda x: x.split("/")[0].split("+")[0])
    df_in["dateTime"] = pd.to_datetime(df_in.validTime, format="%Y-%m-%dT%H:%M:%S")
    # adjust timezone
    df_in["dateTime"] = df_in.dateTime - datetime.timedelta(hours=5)
    df_in = df_in.set_index("dateTime").drop("validTime", axis=1)
    return df_in


def process_data(loc):
    temps = loc.forecastTemps
    snow = pd.DataFrame(loc.snowfallAmount)
    # create dataframe from individual data 'series'
    # format temperature forecast
    df_temps = format_data(temps)
    df_temps["temperature"] = [c_to_f(i) for i in df_temps.value]
    df_apTemps = format_data(loc.apparentTemps)
    df_apTemps["apparent_temp"] = [c_to_f(i) for i in df_apTemps.value]
    df_chill = format_data(loc.windchillTemps)
    df_chill["windchill_temp"] = [c_to_f(i) for i in df_chill.value]

    # clouds and wind
    df_cloudcover = format_data(loc.cloudCover)
    df_cloudcover["cover"] = df_cloudcover.value
    df_wind = format_data(loc.windSpeed)
    df_wind["wind_speed"] = df_wind.value
    df_precip = format_data(loc.percPrecip)
    df_precip["perc_precip"] = df_precip.value

    # format snowfall forecast
    df_snow = format_data(snow)
    df_snow["snowfall"] = df_snow.value / 25.4  # mm / in

    # combine all data field(s)
    df_data = df_temps[["temperature"]].join(df_snow["snowfall"])
    df_data = df_data.join(df_apTemps["apparent_temp"])
    df_data = df_data.join(df_chill["windchill_temp"])
    df_data = df_data.join(df_cloudcover["cover"])
    df_data = df_data.join(df_wind["wind_speed"])
    df_data = df_data.join(df_precip["perc_precip"])
    df_data = df_data.fillna(method="ffill")

    # caculate daily accumulation of snow
    df_data['day'] = df_data.index.day
    df_data.snowfall.fillna(0, inplace=True)
    df_data['cum_snow'] = df_data.groupby('day')['snowfall'].transform(pd.Series.cumsum)

    return df_data


def main(loc:location):
    loc.get_forecast()
    df_data = process_data(loc)

    # --- plot temp forecast
    #plot_temp(df_data)
    plot_forecast_interactive(df_data, loc)


if __name__ == "__main__":
    # instantiate location
    latlon = [42.68, -71.13]  # north andover
    loc = location(latlon)

    main(loc)

