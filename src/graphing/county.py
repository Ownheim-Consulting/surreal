from urllib.request import urlopen
import json

import plotly.express as px
import numpy as np
import pandas as pd

# Get the county data
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Get the data that we are mapping per county
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

# Set the county names
county_names = []
for fip in df['fips']:
    county = [x for x in counties['features'] if str(x['id']) == fip]
    if (len(county) > 0):
        county_names.append(county[0]['properties']['NAME'])
    else:
        county_names.append("Unknown County Name")
df['county_name'] = county_names

df.to_csv('data_usa_counties_unemp.csv', index=False)

# # Map between county FIPS number and the unemployment
# fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
#                            color_continuous_scale='Viridis', range_color=(0, 12),
#                            mapbox_style="carto-positron", zoom=3, center={"lat":37.0902, "lon":-95.7129},
#                            opacity=0.5, labels={'unemp':'Unemployment Rate'})
# fig.update_layout(margin={ "r": 0, "t": 0, "l": 0, "b": 0 })
# fig.show()
