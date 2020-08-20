#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 16:53:00 2019

@author: Xiaoyu Zhu
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import googlemaps
import base64
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
gmaps_key = googlemaps.Client(key="AIzaSyA17Dzrox_iokVB7TbbyoNf4JwZRNPPWxE")
from geopy.geocoders import Nominatim
nom = Nominatim()
mapbox_access_token = "pk.eyJ1Ijoidm9sYW5kYXpodSIsImEiOiJjazFhMjYycHYwMXg3M21zYjhvdmRpNDM5In0.mSiYu8ku8iMAVSc9lYiOVA"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

image_filename = './images/foodine.png'  #company logo
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/1.png'  #food image1 on header
encoded_image1 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/2.png'  #food image2
encoded_image2 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/3.png'  #food image3
encoded_image3 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/4.png'  #food image4
encoded_image4 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/5.png'  #food image5
encoded_image5 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/6.png'  #food image6
encoded_image6 = base64.b64encode(open(image_filename, 'rb').read())
image_filename = './images/7.png'  #food image7
encoded_image7 = base64.b64encode(open(image_filename, 'rb').read())
header_image_height = 60
header_image_width = 0.996 * header_image_height  # preserving aspect ratio of image
header_image_height1 = 75
header_image_width1 = 1.336 * header_image_height1

css_style = {
    "title": {
        "color": "white",
        "background-color": "#3182bd",
        "margin": "0",
        "padding": "100px",
        "border-bottom": "solid thin black",
        "border-radius": "10px"
    },

    "plotting-area": {
        "border": "solid thin lightgrey",
        "background-color": "#F5F6F9",
        "padding": "50",
        "margin-bottom": "80"
    },

    "heading": {
        "text-align": "center",
        "text-decoration": "underline"
    }
}
#type of cuisine
ctype = ['American', 'Caribbean', 'Burger', 'Asian', 'Pizza', 'European',
         'Italian', 'German', 'Southern', 'Breakfast', 'Vegetarian',
         'International', 'Thai', 'Japanese', 'BBQ', 'Chinese', 'Sandwich',
         'Mexican', 'Tapas', 'French', 'Desserts', 'Latin American',
         'Brazilian', 'Mediterranean', 'Korean', 'Lebanese',
         'Coffee and Tea', 'nan', 'Fast Food', 'Seafood', 'Indian', 'Greek',
         'Vietnamese', 'Taco', 'Cafe', 'Bar Food', 'Ice Cream', 'African',
         'Middle Eastern', 'Sushi', 'Dim Sum', 'Steak', 'Diner',
         'New American', 'Donuts', 'Deli', 'Beverages', 'Pub Food',
         'Spanish', 'Eastern European', 'Healthy Food', 'Tea', 'Hungarian',
         'Drinks Only', 'Taiwanese', 'Turkish', 'Salad', 'Bakery',
         'Southwestern', 'Cajun', 'Fusion', 'California', 'Frozen Yogurt',
         'Portuguese', 'Armenian', 'Juices', 'Moroccan', 'Ethiopian',
         'Hawaiian']
#regions
area = ['Downtown-CBD', 'Strip District', 'South Side',
        'Aspinwall/Blawnox', 'Oakland', 'Lawrenceville', 'Point Breeze',
        'Mt Lebanon', 'Bloomfield', 'East Liberty', 'Shadyside',
        'North Side', 'Far South/South Hills', 'Regent Square',
        'Mt Washington', 'Robinson', 'Squirrel Hill/CMU', 'Dormont',
        'Highland Park/Morningside', 'Greenfield/Hazelwood',
        'Station Square', 'Waterfront', 'Canonsburg', 'Penn Hills',
        'Forest Hills', 'Bethel Park', 'Cecil', 'Collier Township',
        'Troy Hill', 'Oakmont', 'Bellevue/Emsworth', 'Wexford',
        'Monroeville', 'Harmony', 'Cranberry Twp', 'Homestead/Munhall',
        'West View', 'Garfield', 'McMurray', 'East', 'Beaver',
        'Moon Township', 'Greensburg', 'West End', 'Washington',
        'Carnegie', 'Sewickley', 'North', 'Leetsdale', 'Bakerstown',
        'Freeport', 'Millvale', 'Seven Fields', 'Glenshaw', 'Gibsonia',
        'East Pittsburgh', 'Blairsville', 'Pleasant Hills', 'Swissvale',
        'McKeesport', 'Mars', 'Ambridge', 'Oakdale', 'South',
        'Murrysville', 'Butler', 'South Park', 'Aliquippa', 'Allison Park',
        'Elizabeth', 'Clairton', 'New Brighton', 'North Huntingdon',
        'Sharpsburg', 'McKees Rocks', 'Leechburg', 'Verona',
        'Homewood/Larimer', 'Venetia', 'Belle Vernon', 'Evans City',
        'New Kensington', 'Plum', 'Meadow Lands', 'Coraopolis',
        'Beaver Falls', 'White Oak', 'Sarver', 'Vandergrift', 'Tarentum',
        'Cheswick', 'Monongahela', 'Ellwood City', 'West Newton',
        'Russellton', 'Latrobe', 'Wilkinsburg', 'Export', 'Delmont',
        'Lower Burrell', 'Eighty Four', 'Monaca', 'Zelienople',
        'Turtle Creek', 'Etna', 'Imperial', 'Bentleyville',
        'Natrona Heights', 'Apollo', 'Mt Pleasant', 'Wilmerding',
        'Ford City', 'Rochester', 'Trafford', 'Saxonburg', 'Clinton',
        'Irwin', 'Springdale', 'Glassport', 'Finleyville', 'Scottdale',
        'Grindstone', 'West Elizabeth', 'Brownsville', 'Houston',
        'Charleroi', 'Coal Ctr', 'Brackenridge', 'Dravosburg', 'Jeannette', ]

#sourse data
AllData = pd.read_csv('./data/merge_data_final.csv', delimiter=',')


def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns[:]])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns[:]
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cusine = ''

app.layout = html.Div([
    html.Div(
        className="container",
        style={"max-width": "100%"},
        children=[
            # facilitate multi-page app
            dcc.Location(id="url", refresh=True),
            # header
            html.Div(
                className="row",
                children=[
                    html.Img(
                        style={"margin-right": 5},
                        src='data:image/png;base64,{}'.format(encoded_image.decode()),
                        height=header_image_height,
                        width=header_image_width
                    ),
                    html.H1(
                        style={"display": "inline-block"},
                        children="Foodine"
                    ),

                    html.Img(
                        style={"margin-left": 30},
                        src='data:image/png;base64,{}'.format(encoded_image1.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image2.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image3.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image4.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image5.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image6.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),
                    html.Img(
                        style={"margin-left": 1},
                        src='data:image/png;base64,{}'.format(encoded_image7.decode()),
                        height=header_image_height1,
                        width=header_image_width1
                    ),

                    html.Div(
                        className="row",
                        style={"float": "right"},
                        children=[html.Div([
                            html.H1(
                                style={"display": "inline-block"},
                                children="Group 4"),
                            html.Div('''
                             Xiaoyu Zhu Xindi Shi 
                             Jiang Chang Ananya Gohsh
                            ''')
                        ]),
                        ]
                    )
                ]
            ),
            html.Div(
                children=html.Div([
                    html.Div('''
                Welcome to Foodine. Let's explore food in Pittsburgh!
            ''')
                ])
            ),

            html.Div([
                html.Div([
                    html.Label('Cusine'),
                    dcc.Dropdown(
                        id='cusine_',
                        options=[{'label': i, 'value': i} for i in ctype],
                        value='American'
                    )],
                    style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    html.Label('Area'),
                    dcc.Dropdown(
                        id='area_',
                        options=[{'label': i, 'value': i} for i in area],
                        value='Shadyside'
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),


                html.Div([
                    html.Label('Price'),
                    dcc.Dropdown(
                        id='price_',
                        options=[
                            {'label': '$', 'value': '$'},
                            {'label': '$$', 'value': '$$'},
                            {'label': '$$$', 'value': '$$$'},
                            {'label': '$$$$', 'value': '$$$$'},
                        ],
                        value='$'
                    )],

                    style={'width': '50%', 'display': 'inline-block'}),
                html.Button(id='submit-button', n_clicks=0, children='Submit',
                            style={'width': '9%', 'float': 'middle'}),
                html.Div(id='output-state')
            ],

                style={'columnCount': 1,
                       'borderBottom': 'thin lightgrey solid',
                       'backgroundColor': 'rgb(250, 250, 250)',
                       'padding': '10px 5px',
                        'margin': '0 auto'
                       }
            )
        ]),

    html.Div([
        html.Table(id='table', style={'align':'center','margin': '0 auto'}),
    ]),

    html.Div(
        id='graph',
        className="five columns"
    ),
    html.Div(
        dcc.Graph(id='map',
        style={'margin-top': '50'}),
        className="six columns"
    )

])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('cusine_', 'value'),
               State('area_', 'value'),
               State('price_', 'value'), ])
# def update_output(n_clicks, input1, input2, input3):
def okoutput(n_clicks, input1, input2, input3):
    return u'''
        Cusine choice is "{}",
        and Area choice is "{}",
        and price choice is "{}",
    '''.format(input1, input2, input3)


@app.callback(Output('table', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('cusine_', 'value'),
               State('area_', 'value'),
               State('price_', 'value'), ])
# def update_output(n_clicks, input1, input2, input3):
def table(n_clicks, input1, input2, input3):
    return generate_table(generateFrame(input1, input2, input3, AllData))


def generateFrame(cusine, regin, cost, data):
    if regin != None:
        data = data[(data['area'] == regin)]
    if cost != None:
        data = data[(data['cost'] == cost)]
    if cusine != None:
        data = data[(data['cuisine_style'] == cusine)]


    Data_ = {'name': data['name']}

    Data = pd.DataFrame(Data_)
    Data['name'] = data['name']
    Data['address'] = data['address']
    Data['area'] = data['area']
    Data['cost'] = data['cost']
    Data['phone'] = data['phone number']
    Data['cuisine_style'] = data['cuisine_style']
    Data['zomato_rating_rating'] = data['zomato_rating']
    Data['yelp_rating'] = data['yelp_rating']
    Data['tripadvisor_rating'] = data['ta_rating']
    Data['dzdp_rating'] = data['dzdp_rating']
    Data['suggested_rating'] = round(data['suggested_rating'],1)
    # Data['review_num'] = round((data['zomato_rev_num']+data['yelp_rev_num']+data['ta_rev_num'])/3)
    Data = Data.sort_values(by='suggested_rating', ascending=False)
    return Data


@app.callback(Output('graph', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('cusine_', 'value'),
               State('area_', 'value'),
               State('price_', 'value'), ])

def updateGraph(n_clicks, input1, input2, input3):
    df = generateFrame_2(input1, input2, input3, AllData)
    if len(df['name']) > 5:
        xname = list(df['name'].head(5))
    else:
        xname = list(df['name'])

    trace1 = go.Bar(name='zomato', x=xname, y=df['zomato_rating'], text=df['zomato_rev_num'])
    trace2 = go.Bar(name='ta', x=xname, y=df['ta_rating'],text=df['ta_rev_num'])
    trace3 = go.Bar(name='yelp', x=xname, y=df['yelp_rating'],text=df['yelp_rev_num'])
    trace4 = go.Bar(name='dzdp', x=xname, y=df['dzdp_rating'])
    return html.Div([
        dcc.Graph(
            figure={
                "data": [trace1, trace2, trace3, trace4],
                "layout": go.Layout(title='Ratings by customer', barmode='group',
                                    colorway=["lightcoral", "#EF533B", "saddlebrown", "gold"], hovermode="closest"
                                    )
            }
        )
    ])


def generateFrame_2(cusine, regin, cost, data):
    if regin != None:
        data = data[(data['area'] == regin)]
    if cost != None:
        data = data[(data['cost'] == cost)]
    if cusine != None:
        data = data[(data['cuisine_style'] == cusine)]

    Data_ = {'name': data['name']}
    Data = pd.DataFrame(Data_)
    Data['address'] = data['address']
    Data['area'] = data['area']
    Data['cost'] = data['cost']
    Data['cuisine_style'] = data['cuisine_style']
    Data['suggested_rating'] = data['suggested_rating']
    Data['zomato_rating'] = data['zomato_rating']
    Data['yelp_rating'] = data['yelp_rating']
    Data['dzdp_rating'] = data['dzdp_rating']
    Data['ta_rating'] = data['ta_rating']
    Data['zomato_rev_num'] = data['zomato_rev_num']
    Data['yelp_rev_num'] = data['yelp_rev_num']
    Data['ta_rev_num'] = data['ta_rev_num']
    Data = Data.sort_values(by='suggested_rating', ascending=False)
    return Data


@app.callback(Output('map', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('cusine_', 'value'),
               State('area_', 'value'),
               State('price_', 'value'), ])
def updateMap(n_clicks, input1, input2, input3):
    df = generateFrame_3(input1, input2, input3, AllData)
    if len(df) > 5:
        df = df.head(5)

    df['cord'] = df['address'].apply(nom.geocode)
    df['lat'] = df['cord'].apply(lambda x: x.latitude if x != None else None)
    df['lon'] = df['cord'].apply(lambda x: x.longitude if x != None else None)
    site_lat = df.lat
    site_lon = df.lon
    locations_name = df.index
    data = [
        go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            ),
            text=locations_name,
            hoverinfo='text'
        ),
        go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=8,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            hoverinfo='none'
        )]

    layout = go.Layout(
        title='Geolocation of restaurants',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=3,
            style='light'
        ),
    )
    return go.Figure(data=data, layout=layout)


def generateFrame_3(cusine, regin, cost, data):
    if regin != None:
        data = data[(data['area'] == regin)]
    if cost != None:
        data = data[(data['cost'] == cost)]
    if cusine != None:
        data = data[(data['cuisine_style'] == cusine)]

    Data_ = {'name': data['name']}
    Data = pd.DataFrame(Data_)
    Data['address'] = data['address']
    Data['area'] = data['area']
    Data['cost'] = data['cost']
    Data['cuisine_style'] = data['cuisine_style']
    Data['suggested_rating'] = data['suggested_rating']
    Data = Data.sort_values(by='suggested_rating', ascending=False)
    return Data


if __name__ == '__main__':
    app.run_server(debug=True)
