from typing import List, Any
import plotly.graph_objects as go
import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Michigan Climbing Club Alums")

def get_city_lat_long(city: str) -> List[float]:
    location = geolocator.geocode(city)
    print(location)
    if location:
        return [location.latitude, location.longitude]
    else:
        return None

def get_lat_longs(data_frame: pd.DataFrame) -> List[List[float]]:
    output = []
    print(data_frame.Location)
    for city in data_frame.Location:
        output.append(get_city_lat_long(city))
    output = [x for x in output if x is not None]
    return output

url = 'https://docs.google.com/spreadsheets/d/1PG0qEpWlBS8FYxCOwYU13VbmpY3UZFEvQ_oMXLl5zDE/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
data = pd.read_csv(path, engine = 'python')
#data = pd.read_csv('test.csv')
data.head()

city_locs = get_lat_longs(data)

fig = go.Figure()
lats = [x[0] for x in city_locs]
longs = [x[1] for x in city_locs]

fig.add_scattergeo(lat = lats
                    ,lon = longs
                    ,hoverinfo = 'none'
                    ,marker_size = 10
                    ,marker_color = 'rgb(65, 105, 225)' # blue
                    ,marker_symbol = 'star'
                    ,showlegend = False
                    )

fig.show()
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)