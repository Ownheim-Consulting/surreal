import os
from datetime import datetime

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from scipy.stats import pearsonr

Salaries_DF = None
Weather_DF = None
Disasters_DF = None
NaturalDisasters = None
DeltaX_DF = None
Relationships = None

fp_county = None
county = None
fig = None

def setup_graphing():
    global Salaries_DF
    global Weather_DF
    global Disasters_DF
    global NaturalDisasters
    global DeltaX_DF
    global Relationships

    global fp_county
    global county
    global fig

    Salaries_DF = pd.read_csv('src/graphing/csv/Salaries.csv')
    Weather_DF = pd.read_csv('src/graphing/csv/Weather.csv')
    Disasters_DF = pd.read_csv('src/graphing/csv/NaturalDisasters_Year.csv')
    NaturalDisasters = pd.read_csv('src/graphing/csv/NaturalDisasters.csv')
    DeltaX_DF = pd.read_csv('src/graphing/csv/DeltaX.csv')
    Relationships = pd.read_csv('src/graphing/csv/Relationships.csv')

    fp_county="src/graphing/maps/US_COUNTY.shp"
    county= gpd.read_file(fp_county).to_crs('epsg:4326')
    county['state_county'] = county['STATE'] +' '+ county['COUNTY']

    fig = px.choropleth_mapbox(county,
                            locations = "COUNTY",
                            featureidkey="properties.County",
                            height=500,
                            center={"lat": float(DeltaX_DF['latitude'].mean()), "lon": float(DeltaX_DF['longitude'].mean())},
                            zoom = 6,
                            mapbox_style="open-street-map",
                        color_continuous_scale="YlGn")

    fig.add_scattermapbox(
        lat = DeltaX_DF['latitude'],
        lon = DeltaX_DF['longitude'],
        mode = 'markers+text',
        marker_size=10,
        opacity = 0.2,
        marker_color='red'
    )

def graph_disasters():
    for disaster in ['Flood', 'Hurricane', 'Severe Storm(s)', 'Snow', 'Tornado', 'Fire', 'Severe Ice Storm', 'Coastal Storm']:

        df = NaturalDisasters[NaturalDisasters['incidentType'] == disaster]
        fig = px.choropleth(df, geojson=county,
                            locations = "state_county",
                            featureidkey="properties.state_county",
                            color='size',
                            height=500,
                        color_continuous_scale="Turbo")
        fig.update_geos(fitbounds="geojson", visible=True)
        fig.update_layout(
            title_text= disaster + ' alerts by County'
            )
        fig.update(layout = dict(title=dict(x=0.5)))
        fig.update_layout(
                margin={"r":0,"t":30,"l":10,"b":10},
                coloraxis_colorbar={
                    'title': disaster + ' threats'})
    return fig

def graph_total_disasters():
    fig = graph_disasters()
    Totals = NaturalDisasters.groupby('state_county').sum().reset_index()

    fig = px.choropleth(Totals, geojson=county,
                            locations = "state_county",
                            featureidkey="properties.state_county",
                            color='size',
                            height=500,
                        color_continuous_scale="Turbo")
    fig.update_geos(fitbounds="geojson", visible=True)
    fig.update_layout(
            title_text= 'Alerts by County'
            )
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
                margin={"r":0,"t":30,"l":10,"b":10},
                coloraxis_colorbar={
                    'title': 'Total number of alerts'})
    return fig

def graph_weather_value(year: int, category: str):
    Year = year
    Category = category
    fig = px.choropleth(Weather_DF[Weather_DF['year'] == Year], geojson=county,
                        locations = "state_county",
                        featureidkey="properties.state_county",
                        color=Category,
                        height=500,
                        color_continuous_scale="Turbo")
    fig.update_geos(
                        fitbounds="geojson", visible=True)
    fig.update_layout(title_text= Category + ' by County in ' + str(Year))
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
                        margin={"r":0,"t":30,"l":10,"b":10},
                        coloraxis_colorbar={
                        'title': Category})
    return fig

def graph_salaries(year: int):
    df = Salaries_DF[Salaries_DF['YEAR'] == year]
    fig = px.choropleth(df, geojson=county,
                        locations = "state_county",
                        featureidkey="properties.state_county",
                        color='salary (thousands)',
                        height=500,
                        color_continuous_scale="Turbo")
    fig.update_geos(fitbounds="geojson", visible=True)
    fig.update_layout(
            title_text= str(year) + ' anual salary'
            )
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
                margin={"r":0,"t":30,"l":10,"b":10},
                coloraxis_colorbar={
                    'title': 'annual salary'})
    return fig

def graph_salary_temp_correlation():
    fig = px.choropleth(Relationships, geojson=county,
                        locations = "county",
                        featureidkey="properties.state_county",
                        color='abs r',
                        height=500,
                        color_continuous_scale="Turbo")
    fig.update_geos(
                        fitbounds="geojson", visible=True)
    fig.update_layout(title_text= 'Correlation between avg temperature and salary')
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
                        margin={"r":0,"t":30,"l":10,"b":10},
                        coloraxis_colorbar={
                        'title': 'r'})
    return fig

def graph_p_val_between_avg_temp_and_salary():
    fig = px.choropleth(Relationships, geojson=county,
                        locations = "county",
                        featureidkey="properties.state_county",
                        color='p-value',
                        height=500,
                        color_continuous_scale="Turbo")
    fig.update_geos(
                        fitbounds="geojson", visible=True)
    fig.update_layout(title_text= 'p-value between avg temperature and salary')
    fig.update(layout = dict(title=dict(x=0.5)))
    fig.update_layout(
                        margin={"r":0,"t":30,"l":10,"b":10},
                        coloraxis_colorbar={
                        'title': 'r'})
    return fig

def save_plot_as_png(plot, filename):
    if not os.path.exists(filename):
        os.mkdir(filename)
    plot.write_image(filename)
