import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt


# # ---INSET PASSWORD---
# passwords = ["a"]
# password_empty = st.empty()
# password = password_empty.text_input('password', placeholder='insert password ...',type="password", label_visibility="collapsed")

# if not password:
#     st.stop()

# elif password not in passwords:
#     st.warning('The password is not correct', icon="⚠️")
#     st.stop()
    
# password_empty.empty()


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


    

    ############################# 
    # Streamlit app
    #############################

    "## National Parks in the United States"

    """
    The National Parks Service provides an [API](https://www.nps.gov/subjects/digital/nps-data-api.htm) to programmatically explore NPS data. 

    We can take data about each park and display it on the map _conditionally_ based on whether it is in the viewport. 

    ---
    """

    # define layout
    c1, c2 = st.columns(2)



    # layout map
    with c1:
        """(_Click on a pin to bring up more information_)"""
        # getting the data
        url = (
            "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
        )
        state_geo = f"{url}/us-states.json"
        state_unemployment = f"{url}/US_Unemployment_Oct2012.csv"
        state_data = pd.read_csv(state_unemployment)
        
        
        m = folium.Map(location = [40, -95], zoom_start = 4)
        folium.Choropleth(
   
              # geographical locations
            geo_data = state_geo,                    
            name = "choropleth",

              # the data set we are using
            data = state_data,                       
            columns = ["State", "Unemployment"],    

              # YlGn refers to yellow and green
            fill_color = "YlGn",                     
            fill_opacity = 0.7,
            line_opacity = .1,
              key_on = "feature.id",
            legend_name = "Unemployment Rate (%)",
        ).add_to(m)      


        map_data = st_folium(m, key="fig1", width=700, height=700)
    with c2:
        state = map_data["last_active_drawing"]["id"]
        value = state_data[state_data["State"]==state]["Unemployment"][0]
        st.metric(label="Unemployment", value=value)
