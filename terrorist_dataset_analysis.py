
#importing the libraries
import webbrowser
import pandas as pd
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate
import plotly.figure_factory as ff

# Global variables
app = dash.Dash()


def load_data():
  dataset_name = "global_terror.csv"

  #this line we use to hide some warnings which gives by pandas
  pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  
  #pd.set_option("display.max_rows", None)
  #pd.set_option('display.max_columns', None)
  print(df.head(5))
  print(df.tail(5))

  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  #region_list.insert(0, {"label":"All", "value":"All"} )

  #print(region_list)  
  # Total 12 Regions

  global country_list
  #country_list = [{"label": str(i), "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())]
  #print(country_list)
  # Total 205 Countries
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  global state_list
  #state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
  #print(state_list)
  # Total 2580 states
  state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()


  global city_list
  #city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
  #print(city_list)
  # Total 39489 cities
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  #print(attack_type_list)


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  #print(year_dict)
  
  #chart dropdown options
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  global winfoPieSelector
  winfoPieSelector = {"Attack type":"attacktype1_txt", "weapon type":"weaptype1_txt", "Target type":"targtype1_txt"}

  global IinfoPieSelector
  IinfoPieSelector = {"Attack type":"attacktype1_txt", "weapon type":"weaptype1_txt", "Target type":"targtype1_txt", "State analysis":"provstate"}


def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app8_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div([
  html.H1('Terrorism Analysis with Insights', id='Main_title'),
  dcc.Tabs(id="Tabs", value="Map",children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
          dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
              ]),
          dcc.Dropdown(
              id='month', 
                options=month_list,
                placeholder='Select Month',
                multi = True
                  ),
          dcc.Dropdown(
                id='date', 
                placeholder='Select Day',
                multi = True
                  ),
          dcc.Dropdown(
                id='region-dropdown', 
                options=region_list,
                placeholder='Select Region',
                multi = True
                  ),
          dcc.Dropdown(
                id='country-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select Country',
                multi = True
                  ),
          dcc.Dropdown(
                id='state-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True
                  ),
          dcc.Dropdown(
                id='city-dropdown', 
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True
                  ),
          dcc.Dropdown(
                id='attacktype-dropdown', 
                options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                placeholder='Select Attack Type',
                multi = True
                  ),

          html.H5('Select the Year', id='year_title'),
          dcc.RangeSlider(
                    id='year-slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]),
      dcc.Tab(label = "Infographics", id="info tool", value = "info", children = [
          dcc.Tabs(id="subtabs3", value="World Infographics", children =[
              dcc.Tab(label = "World Inforgraphics", id = "WorldI", value = "World Infographics",children = [
              
                    dcc.Tabs(id="subtabs3_1", value="wstacked", children =[
                        dcc.Tab(label = "stacked bar chart", id = "wsbc", value = "wstacked", children = [
                            
                            html.Br(),
                            html.Br(),
                            
                            dcc.RangeSlider(
                            id='stacked_year_slider',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict,
                            step=None),
                            
                            html.Br(),
                            html.Br(),
                            html.Hr()
                            ]),
                            
                        dcc.Tab(label = "density map", id = "wdm", value ="wdensity", children = [
                            
                            html.Br(),
                            html.Br(),
                            
                            dcc.RangeSlider(
                            id='density_year_slider',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict,
                            step=None),
                            
                            html.Br(),
                            html.Br(),
                            html.Hr()
                            ]),              
                        
                        
                        dcc.Tab(label = "scatter plot", id = "wsp", value = "wscatter", children = [
                            dcc.Dropdown(id="wscatter_dd",
                                         options = [{"label":m, "value":m} for m in df["region_txt"].unique().tolist()],
                                         placeholder = "Select region",
                                         value = "South Asia"
                                         )
                            ]),
                        
                        
                        dcc.Tab(label = "scatter geo plot", id = "wsgp", value = "wsgeo"),
                        
                        
                        dcc.Tab(label = "piechart", id = "wpc", value = "wpie", children = [
                            html.Br(),
                            html.Br(),
                            
                            
                            dcc.Dropdown(id = "pie_selector", 
                                         options = [{"label":key, "value":value} for key, value in winfoPieSelector.items()], 
                                         value = "attacktype1_txt"),
                            
                            html.Br(),
                            html.Br(),
                            html.Hr()
                            ]),
                        dcc.Tab(label = "heatmap", id = "whm", value = "wheat"),
                        
                        dcc.Tab(label = "bar & line charts", id = "wbc", value = "wbar",
                                 children = [
                                     html.Br(),
                                     html.Br(),
                                     dcc.Dropdown(id = "bar_selector", 
                                          options = [{"label":value, "value":value} for value in ["Animated", "Static", "Time Series"]], 
                                          value = "Animated"), 
                                     html.Br(),
                                     html.Br(),
                                     html.Hr()
                                     
                                     
                                     ]),
                          ])
                  ]),
              dcc.Tab(label = "Indian Inforgraphics", id = "IndiaI", value = "Indian Infographics",children = [
                  dcc.Tabs(id="subtabs3_2", value="istacked", children =[
                      dcc.Tab(label = "stacked bar chart", id = "isbc", value = "istacked", children = [
                                        
                                        html.Br(),
                                        dcc.Dropdown(id = "istacked_dd",
                                                     options = [{"label":"State", "value":"State"}],
                                                     placeholder = "Select here"),
                                    
                                        
                                        html.Br(),
                                        html.Br(),
                                        
                                        
                                        
                                        
                                        dcc.RangeSlider(
                                        id='istacked_year_slider',
                                        min=min(year_list),
                                        max=max(year_list),
                                        value=[min(year_list),max(year_list)],
                                        marks=year_dict,
                                        step=None),
                                        
                                        html.Br(),
                                        html.Br(),
                                        html.Hr()
                                        ]),
                      
                      
                      dcc.Tab(label = "state stacked bar chart", id = "issbc", value = "isstacked", children = [
                                        
                                        html.Br(),
                                        dcc.Dropdown(id = "isstacked_dd",
                                                     options = [{"label":m, "value":m} for m in df[df["country_txt"]=="India"]["provstate"].unique().tolist()],
                                                     placeholder = "Select here", 
                                                     value = "Delhi", 
                                                     clearable = False),
                                    
                                        
                                        html.Br(),
                                        html.Br(),
                                        
                                        
                                        
                                        
                                        dcc.RangeSlider(
                                        id='isstacked_year_slider',
                                        min=min(year_list),
                                        max=max(year_list),
                                        value=[min(year_list),max(year_list)],
                                        marks=year_dict,
                                        step=None),
                                        
                                        html.Br(),
                                        html.Br(),
                                        html.Hr()
                                        ]),
                                dcc.Tab(label = "density map", id = "idm", value ="idensity", children = [
                            
                            html.Br(),
                            html.Br(),
                            
                            dcc.RangeSlider(
                            id='idensity_year_slider',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict,
                            step=None),
                            
                            html.Br(),
                            html.Br(),
                            html.Hr()
                            ]),              
                                dcc.Tab(label = "scatter plot", id = "isp", value = "iscatter", children = [
                                    dcc.Dropdown(id = "iscatter_dd",
                                                 options = [{"label":m, "value":m} for m in df[df["country_txt"]=="India"]["provstate"].unique().tolist()],
                                                 placeholder = "select state", value = "Delhi")
                                    ]),
                                dcc.Tab(label = "scatter geo plot", id = "isgp", value = "isgeo"),
                                dcc.Tab(label = "piechart", id = "ipc", value = "ipie",children = [
                            html.Br(),
                            html.Br(),
                            
                            
                            dcc.Dropdown(id = "ipie_selector", 
                                         options = [{"label":key, "value":value} for key, value in IinfoPieSelector.items()], 
                                         value = "attacktype1_txt"),
                            
                            html.Br(),
                            html.Br(),
                            html.Hr()
                            ]),
                                dcc.Tab(label = "heatmap", id = "ihm", value = "iheat"),
                                dcc.Tab(label = "bar & line charts", id = "ibc", value = "ibar", children = [
                                     html.Br(),
                                     html.Br(),
                                     dcc.Dropdown(id = "ibar_selector", 
                                          options = [{"label":value, "value":value} for value in ["Animated", "Static", "Time Series"]], 
                                          value = "Animated"), 
                                     html.Br(),
                                     html.Br(),
                                     html.Hr()
                                     
                                     
                                     ] )
                    ])
              ])
          ])
        ])
      ]),
  
  html.Br(),
  html.Br(),
  html.Div(id = "graph-object", children ="Graph will be shown here")
  ])
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'), 
    dash.dependencies.Input('cyear_slider', 'value'),    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs2", "value"),
    dash.dependencies.Input("subtabs3", "value"),
    dash.dependencies.Input("subtabs3_1", "value"),
    dash.dependencies.Input("subtabs3_2", "value"),
    dash.dependencies.Input("stacked_year_slider", "value"),
    dash.dependencies.Input("density_year_slider", "value"),
    dash.dependencies.Input("wscatter_dd", "value"),
    dash.dependencies.Input("pie_selector", "value"),
    dash.dependencies.Input("bar_selector", "value"),
    dash.dependencies.Input("istacked_year_slider", "value"),
    dash.dependencies.Input("idensity_year_slider", "value"),
    dash.dependencies.Input("iscatter_dd", "value"),
    dash.dependencies.Input("ipie_selector", "value"),
    dash.dependencies.Input("ibar_selector", "value"),
    dash.dependencies.Input("istacked_dd", "value"),
    dash.dependencies.Input("isstacked_dd", "value"),
    dash.dependencies.Input("isstacked_year_slider", "value")
    ]
    )

def update_app9_ui(Tabs, 
                   month_value, 
                   date_value,
                   region_value,
                   country_value,
                   state_value,
                   city_value,
                   attack_value,
                   year_value,
                   chart_year_selector,
                   chart_dp_value, 
                   search,
                   subtabs2, 
                   subtabs3, 
                   option,
                   option2, 
                   stacked_year_selector,
                   density_year_selector, 
                   wscatter_dd,
                   pie_selector, 
                   bar_selector,
                   istacked_year_selector,
                   idensity_year_selector,
                   iscatter_dd, 
                   ipie_selector, 
                   ibar_selector, 
                   istacked_dd, 
                   isstacked_dd,
                   isstacked_year_slider):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Data of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Data of year value = " , year_value)
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(state_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        
         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure


    elif Tabs=="Chart":
        fig = None
        
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure 
        
    elif Tabs == "info":
        fig = None
        if subtabs3 == "World Infographics":
            if option == "wstacked":
                year_range_2 = range(stacked_year_selector[0], stacked_year_selector[1]+1)
                
                stacked_data = df[df["iyear"].isin(year_range_2)].groupby("iyear")["attacktype1_txt"].value_counts().reset_index(name="count") 
                
                fig = px.bar(stacked_data, x="iyear", y="count", color="attacktype1_txt", barmode = 'stack') 
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
            elif option =="wdensity":
                year_range_3 = range(density_year_selector[0], density_year_selector[1]+1)
                df["attacks"] = df.groupby("country_txt")["country"].transform("count")
                density_data = df[df["iyear"].isin(year_range_3)].filter(['country_txt','attacks','latitude','longitude']).drop_duplicates()
                fig = px.density_mapbox(density_data, lat='latitude', lon='longitude', zoom=1,hover_data = ["country_txt", "attacks"],
                            mapbox_style="open-street-map")
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
                
                
            elif option == "wscatter":
                if wscatter_dd is not None:
                    scatter_data = df[df["region_txt"]==wscatter_dd].groupby(["iyear"])["attacktype1_txt"].value_counts().reset_index(name = "size")
                else:
                    scatter_data = df.groupby(["iyear"])["attacktype1_txt"].value_counts().reset_index(name = "size")
                fig = px.scatter(scatter_data, x = "iyear", y = "attacktype1_txt", size = "size", template = "plotly_dark",color = "attacktype1_txt" )
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
            elif option == "wsgeo":
                fig = px.scatter_geo(df, lat='latitude', lon='longitude',
                            hover_name="country_txt", hover_data=['iyear', 'city', "attacktype1_txt"],
                            labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude'},
                            animation_frame="iyear", color = "attacktype1_txt",
                            projection="natural earth")
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
            elif option == "wpie":
                attack_type = df[pie_selector].value_counts().reset_index(name="count")
                attack_type =  attack_type.rename(columns = {"index":pie_selector, "count":"Frequency"})
                fig = px.pie(attack_type, names =pie_selector , values="Frequency", color = pie_selector, hole=.1)
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
                
            elif option == "wheat":
                df["attacks"] = df.groupby("region_txt")["region_txt"].transform("count")
        
                heat_data = df.filter(['region_txt','attacks']).drop_duplicates()
                
                fig = ff.create_annotated_heatmap(heat_data["attacks"].values.reshape(4,3), annotation_text=heat_data["region_txt"].values.reshape(4,3), colorscale='Viridis', hoverinfo='z', showscale=True)
                fig.update_layout(autosize=True,
                            title={"text" : "Region-Wise Concentration of Attacks using Heatmap", 'x' : 0.5, 'y' : 0.93},
                            font=dict(size=18),
                            )
        
                
            elif option == "wbar":
                if bar_selector =="Animated":
                    animated_bar = df.groupby(["iyear", "region_txt"])["nkill"].apply(lambda x: x.sum()).reset_index(name="Fatalities")
                    fig = px.bar(animated_bar, x ="region_txt" , y ="Fatalities",color= "region_txt", animation_frame =  "iyear",template = "plotly_dark")
                    fig.update_layout(autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
                elif bar_selector == "Static":
                    static_bar = df.groupby(["region_txt"])["nkill"].apply(lambda x: x.sum()).reset_index(name="Fatalities")
                    fig = px.bar(static_bar, x ="region_txt" , y ="Fatalities",color= "region_txt",template = "plotly_dark")
                    fig.update_layout(
                                      autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
                else:
                    time_Series = df.groupby("iyear")["nkill"].apply(lambda x: x.sum()).reset_index(name="Death")
                    fig = px.line(time_Series, x = "iyear", y = "Death", template = "plotly_dark")
                    fig.update_layout(
                                      autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
        elif subtabs3=="Indian Infographics":
            new_df = df[df["country_txt"] == "India"]
            if option2 == "istacked":
                iyear_range_2 = range(istacked_year_selector[0], istacked_year_selector[1]+1)
                ix = None
                
                istacked_data = new_df[new_df["iyear"].isin(iyear_range_2)]
                
                if istacked_dd == "State" and istacked_data.shape[0]:
                    istacked_data = istacked_data.groupby("provstate")["attacktype1_txt"].value_counts().reset_index(name="count")
                    ix = "provstate" 
                elif istacked_dd is None and istacked_data.shape[0]:
                    istacked_data =istacked_data.groupby("iyear")["attacktype1_txt"].value_counts().reset_index(name="count") 
                    ix = "iyear"
                else:
                    istacked_data = pd.DataFrame(columns = ['iyear', 'count', "attacktype1_txt"])
            
                    istacked_data.loc[0] = [0, 0,"No data"]
                    ix = "iyear"
                fig = px.bar(istacked_data, x=ix, y="count", color="attacktype1_txt", barmode = 'stack') 
                fig.update_layout(autosize=True,
                                      margin=dict(l=0, r=0, t=25, b=20),
                                      )
            elif option2 =="isstacked":
                iyear_range_ss = range(isstacked_year_slider[0], isstacked_year_slider[1]+1)
                isstacked_data = new_df[new_df["provstate"]==isstacked_dd].groupby(["iyear", "city"])["attacktype1_txt"].value_counts().reset_index(name="count")
                isstacked_data = isstacked_data[isstacked_data["iyear"].isin(iyear_range_ss)]
                fig = px.bar(isstacked_data, x="city", y="count", color="attacktype1_txt", barmode = 'stack') 
                fig.update_layout(autosize=True,
                                      margin=dict(l=0, r=0, t=25, b=20),
                                      )
            elif option2 =="idensity)":
                iyear_range_3 = range(density_year_selector[0], density_year_selector[1]+1)
                new_df["attacks"] = new_df.groupby("country_txt")["country"].transform("count")
                idensity_data = new_df[new_df["iyear"].isin(iyear_range_3)].filter(['country_txt','attacks','latitude','longitude']).drop_duplicates()
                fig = px.density_mapbox(idensity_data, lat='latitude', lon='longitude', zoom=3,hover_data = ["country_txt", "attacks"],
                            mapbox_style="open-street-map")
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
                    
            elif option2 == "iscatter":
                if iscatter_dd is not None:
                    iscatter_data = new_df[new_df["provstate"] == iscatter_dd].groupby(["iyear"])["attacktype1_txt"].value_counts().reset_index(name = "size")
                else:
                    iscatter_data = new_df.groupby(["iyear"])["attacktype1_txt"].value_counts().reset_index(name = "size")
                fig = px.scatter(iscatter_data, x = "iyear", y = "attacktype1_txt", size = "size", template = "plotly_dark",color = "attacktype1_txt" )
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
            elif option2 == "isgeo":
                fig = px.scatter_geo(new_df, lat='latitude', lon='longitude',
                            hover_name="country_txt", hover_data=['iyear', 'city',"attacktype1_txt"],
                            labels={'iyear':'Year', 'city': 'City', 'latitude':'Latitude', 'longitude':'Longitude'},
                            animation_frame="iyear", color = "attacktype1_txt",
                            projection="natural earth")
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
            elif option2 == "ipie":
                iattack_type = new_df[ipie_selector].value_counts().reset_index(name="count")
                iattack_type =  iattack_type.rename(columns = {"index":ipie_selector, "count":"Frequency"})
                fig = px.pie(iattack_type, names =ipie_selector, values="Frequency", color = ipie_selector, hole=.1)
                fig.update_layout(autosize=True,
                                  margin=dict(l=0, r=0, t=25, b=20),
                                  )
                
            elif option2 == "iheat":
                new_df["iattacks"] = new_df.groupby("provstate")["provstate"].transform("count")
        
                iheat_data = new_df.filter(['provstate','iattacks']).drop_duplicates()
                
                fig = ff.create_annotated_heatmap(iheat_data["iattacks"].values.reshape(7,5), annotation_text=iheat_data["provstate"].values.reshape(7,5), colorscale='Viridis', hoverinfo='z', showscale=True)
                fig.update_layout(autosize=True,
                            title={"text" : "State-wise Concentration of Attacks using Heatmap", 'x' : 0.5, 'y' : 0.93},
                            font=dict(size=18),
                            )
        
                
            elif option2 == "ibar":
                if ibar_selector =="Animated":
                    ianimated_bar = new_df.groupby(["iyear", "provstate"])["nkill"].apply(lambda x: x.sum()).reset_index(name="Fatalities")
                    fig = px.bar(ianimated_bar, x ="provstate" , y ="Fatalities",
                                 color= "Fatalities",
                                 hover_data=['provstate', 'iyear', "Fatalities"],
                                 animation_frame ="iyear",
                                 template = "plotly_dark")
                    fig.update_layout(
                                      autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
                elif ibar_selector == "Static":
                    istatic_bar = new_df.groupby(["provstate"])["nkill"].apply(lambda x: x.sum()).reset_index(name="Fatalities")
                    fig = px.bar(istatic_bar, x ="provstate" , y ="Fatalities",color= "provstate",template = "plotly_dark")
                    fig.update_layout(
                                      autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
                else:
                    itime_Series = new_df.groupby("iyear")["nkill"].apply(lambda x: x.sum()).reset_index(name="Death")
                    fig = px.line(itime_Series, x = "iyear", y = "Death", template = "plotly_dark")
                    fig.update_layout(
                                      autosize=True,
                                      margin=dict(l=20, r=20, t=10, b=20),
                                      )
            
        else:
            return None
    return dcc.Graph(figure = fig)


@app.callback(
  Output("date", "options"),
  [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region-dropdown", "value"),
               Output("region-dropdown", "disabled"),
               Output("country-dropdown", "value"),
               Output("country-dropdown", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of your Project
def main8():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app8_ui()
  app.title = "Terrorism Analysis with Insights"
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() # debug=True

  print("This would be executed only after the script is closed")
  df = None
  app = None



if __name__ == '__main__':
    main8()




'''
     0         1        2         3         4            5            6            7            8
['eventid', 'iyear', 'imonth', 'iday', 'approxdate', 'extended', 'resolution', 'country', 'country_txt', 
   9           10           11         12        13          14            15             16
'region', 'region_txt', 'provstate', 'city', 'latitude', 'longitude', 'specificity', 'vicinity', 
    17         18         19       20       21        22            23                14
'location', 'summary', 'crit1', 'crit2', 'crit3', 'doubtterr', 'alternative', 'alternative_txt', 
    25          26         27           28              29               30              31
'multiple', 'success', 'suicide', 'attacktype1', 'attacktype1_txt', 'attacktype2', 'attacktype2_txt', 
     32                33             34              35              36                37
'attacktype3', 'attacktype3_txt', 'targtype1', 'targtype1_txt', 'targsubtype1', 'targsubtype1_txt', 
   38       39         40            41            42            43              44 
'corp1', 'target1', 'natlty1', 'natlty1_txt', 'targtype2', 'targtype2_txt', 'targsubtype2', 
    45                 46       47         48           49             50           51
'targsubtype2_txt', 'corp2', 'target2', 'natlty2', 'natlty2_txt', 'targtype3', 'targtype3_txt', 
      52               53              54        55         56          57           58
'targsubtype3', 'targsubtype3_txt', 'corp3', 'target3', 'natlty3', 'natlty3_txt', 'gname', 
    59         60         61          62          63         64          65             66
'gsubname', 'gname2', 'gsubname2', 'gname3', 'gsubname3', 'motive', 'guncertain1', 'guncertain2', 
     67              68          69        70          71          72             73 
'guncertain3', 'individual', 'nperps', 'nperpcap', 'claimed', 'claimmode', 'claimmode_txt', 
   74           75             76            77          78              79              80
'claim2', 'claimmode2', 'claimmode2_txt', 'claim3', 'claimmode3', 'claimmode3_txt', 'compclaim', 
    81              82              83                84               85            86    
'weaptype1', 'weaptype1_txt', 'weapsubtype1', 'weapsubtype1_txt', 'weaptype2', 'weaptype2_txt', 
     87                  88             89             90               91                92
'weapsubtype2', 'weapsubtype2_txt', 'weaptype3', 'weaptype3_txt', 'weapsubtype3', 'weapsubtype3_txt', 
    93               94            95                96                97          98        99
'weaptype4', 'weaptype4_txt', 'weapsubtype4', 'weapsubtype4_txt', 'weapdetail', 'nkill', 'nkillus', 
    100       101         102        103          104          105            106              107
'nkillter', 'nwound', 'nwoundus', 'nwoundte', 'property', 'propextent', 'propextent_txt', 'propvalue', 
     108           109          110         111         112       113       114          115 
'propcomment', 'ishostkid', 'nhostkid', 'nhostkidus', 'nhours', 'ndays', 'divert', 'kidhijcountry', 
   116        117           118            119          120             121              122 
'ransom', 'ransomamt', 'ransomamtus', 'ransompaid', 'ransompaidus', 'ransomnote', 'hostkidoutcome', 
       123                124          125        126       127       128      129          130
'hostkidoutcome_txt', 'nreleased', 'addnotes', 'scite1', 'scite2', 'scite3', 'dbsource', 'INT_LOG', 
   131         132         133        134
'INT_IDEO', 'INT_MISC', 'INT_ANY', 'related']
'''

'''
  1         2         3        7            8           9          10            11         12        
iyear  || imonth || iday || country || country_txt || region || region_txt || provstate || city || 

   13           14           28               29                34           35
latitude || longitude || attacktype1 || attacktype1_txt || targtype1 || targtype1_txt || 

   40           41          58         81             82             98          105            106
natlty1 || natlty1_txt || gname || weaptype1  || weaptype1_txt ||  nkill || propextent||  propextent_txt ||
'''

'''
iyear              191464 non-null int64
imonth             191464 non-null int64
iday               191464 non-null int64
country            191464 non-null int64
country_txt        191464 non-null object
region             191464 non-null int64
region_txt         191464 non-null object
provstate          191462 non-null object
city               191038 non-null object
latitude           186884 non-null float64
longitude          186883 non-null float64
attacktype1        191464 non-null int64
attacktype1_txt    191464 non-null object
targtype1          191464 non-null int64
targtype1_txt      191464 non-null object
natlty1            189742 non-null float64
natlty1_txt        189742 non-null object
gname              191464 non-null object
weaptype1          191464 non-null int64
weaptype1_txt      191464 non-null object
nkill              180435 non-null float64
propextent         67286 non-null float64
propextent_txt     67286 non-null object
'''

'''
  df_ = df

  if (month_value != None and date_value != None ):
    df_ = df[(df["imonth"]==month_value) & (df["iday"]==date_value)]

'''


