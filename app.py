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
        m = folium.Map(location=[39.949610, -75.150282], zoom_start=4)

#         for park in parks:
#             popup = folium.Popup(f"""
#                       <a href="{park["url"]}" target="_blank">{park["fullName"]}</a><br>
#                       <br>
#                       {park["operatingHours"][0]["description"]}<br>
#                       <br>
#                       Phone: {park["contacts"]["phoneNumbers"][0]["phoneNumber"]}<br>
#                       """,
#                       max_width = 250)
#             folium.Marker(
#                 [park["latitude"], park["longitude"]], popup=popup
#             ).add_to(m)


        map_data = st_folium(m, key="fig1", width=700, height=700)

#     # get data from map for further processing
#     map_bounds = Bounds.from_dict(map_data["bounds"])

#     # when a point is clicked, display additional information about the park
#     try:
#         point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])

#         if point_clicked is not None:
#             with st.spinner(text="loading image..."):
#                 for park in parks:
#                     if park["_point"].is_close_to(point_clicked):
#                         with c2:
#                             f"""### _{park["fullName"]}_"""
#                             park["description"]
#                             st.image(park["images"][0]["url"], caption = park["images"][0]["caption"])
#                             st.expander("Show park full details").write(park)
#     except TypeError:
#         point_clicked = None

#     # even though there is a c1 reference above, we can do it again
#     # output will get appended after original content
#     with c1: 

#         parks_in_view: List[Dict] = []
#         for park in parks:
#             if map_bounds.contains_point(park["_point"]):
#                 parks_in_view.append(park)

#         "Parks visible:", len(parks_in_view)
#         "Bounding box:", map_bounds
