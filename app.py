import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt


# ---INSET PASSWORD---
passwords = ["a"]
password_empty = st.empty()
password = password_empty.text_input('password', placeholder='insert password ...',type="password", label_visibility="collapsed")

if not password:
    st.stop()

elif password not in passwords:
    st.warning('The password is not correct', icon="⚠️")
    st.stop()
    
password_empty.empty()


# ---Connect to Deta Base with your Project Key---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("project_fietskliniek")
db_content = db.fetch().items
df = pd.DataFrame(db_content)

# ---trial---


# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Agenda", "Dashboard"],
    icons=["bi-journal-check", "bi bi-bar-chart-line-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# ---VARIABLES---
time_shift_choice = ["14-16", "16-18", "18-20"]

if selected == "Agenda":
    
    date =  str(st.date_input("Choose a date"))
    df_filter_data = df[df.date==date]

    # Using "with" notation
    if len(df_filter_data)==0:
      st.info('No appointments', icon="ℹ️")

    else:
      col2, col3, col4 = st.columns([1, 1, 1])
      time_shift_empty = st.empty()
      time_shift = time_shift_empty.radio('Chose a time shift',time_shift_choice, horizontal=True)

      df_filter_time = df_filter_data[df_filter_data.time_shift==time_shift].sort_values("time_shift").reset_index(drop=True)

      n_1 = len(df_filter_data[df_filter_data.time_shift=="14-16"])
      n_2 = len(df_filter_data[df_filter_data.time_shift=="16-18"])
      n_3 = len(df_filter_data[df_filter_data.time_shift=="18-20"])

      col2.metric("14-16", f"{n_1} clients")
      col3.metric("16-18", f"{n_2} clients")
      col4.metric("18-20", f"{n_3} clients")

      placeholder = st.empty()
      placeholder.dataframe(df_filter_time[["name","e_mail","buurt","opmerking","materiaal","werkzaamheedeb"]].T, use_container_width=True)

      if not st.checkbox('Show table'):
        placeholder.empty()
        time_shift_empty.empty()
        
if selected == "Dashboard":

    import folium
    from streamlit_folium import st_folium
    import geopandas
    
    drive = deta.Drive("project_2_drive_1")
    db_point = deta.Base("project_1")
    db_content = db_point.fetch().items
    df_point = pd.DataFrame(db_content)
    gdf = geopandas.GeoDataFrame(df_point, geometry=geopandas.points_from_xy(df_point.lon, df_point.lat))
    


    "## Unemployment in the United States"

    """
    The National Parks Service provides an [API](https://www.nps.gov/subjects/digital/nps-data-api.htm) to programmatically explore NPS data. 

    We can take data about each park and display it on the map _conditionally_ based on whether it is in the viewport. 

    ---
    """
    
    """(_Click on a pin to bring up more information_)"""
    
    # define layout
    c1, c2 = st.columns([3,1])
        
    with c1:     
         m = folium.Map(location = [40, -95], zoom_start = 4)
         pol_m = gdf.to_json()
         folium.GeoJson(pol_m,
                        control = True,
                        marker = folium.CircleMarker(radius = 3, # Radius in metres
                                                   weight = 0, #outline weight
                                                   fill_color = lambda x: {'fillColor':'red' if x['properties']['species'] == 'Ischnura elegans' else 'green','fillOpacity':0.75}, 
                                                   fill_opacity = 1),
                        tooltip = folium.GeoJsonTooltip(fields = ['image_name'],
                                                        aliases=['Image: '],
                                                        style = ("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                                         sticky = True)
                        ).add_to(m)
        
        map_data = st_folium(m, key="fig1")

        
    with c2:
        try:
            properties = map_data["last_active_drawing"]["properties"]
            st.metric(label="Date", value=properties["date"])
            st.metric(label="Species", value=properties["species"])
            st.metric(label="Number of specimens", value=properties["n_specimens"])
            img = drive.get(properties["image_name"]).read()
            st.image(img, caption=properties["comment"])
            
            
        except:
             st.info('Click on a State to see the uneplonment', icon="ℹ️")
       
        
