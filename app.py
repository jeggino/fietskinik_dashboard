import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
import mapclassify
from datetime import datetime as dt


# ---INSET PASSWORD---
passwords = ["fietskliniek"]
password_empty = st.empty()
password = password_empty.text_input('password', placeholder='insert password ...',type="password", label_visibility="collapsed")

if not password:
    st.stop()

elif password not in passwords:
    st.warning('The password is not correct', icon="â ī¸")
    st.stop()
    
password_empty.empty()


# ---Connect to Deta Base with your Project Key---
deta = Deta(st.secrets["deta_key"])
db = deta.Base("project_fietskliniek")
db_content = db.fetch().items
df = pd.DataFrame(db_content)

# ---trial---


this_week = dt.today().isocalendar()[1]
next_week = dt.today().isocalendar()[1] + 1
df_filter_this_week = df[(df["Week"]==this_week)]
df_filter_next_week = df[(df["Week"]==next_week)]

len_this_week = f"This week - {len(df_filter_this_week)} clients"
len_next_week = f"Next week - {len(df_filter_next_week)} clients"

st.title("Agenda đ", anchor=None)
# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=[len_this_week, len_next_week],
#     icons=["bi-journal-check", "bi bi-bar-chart-line-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)



if selected == len_this_week:
    left, right = st.columns([1, 1])
            
    tuesday = len(df_filter_this_week[df_filter_this_week["Day"] == "Tuesday"])
    thursday = len(df_filter_this_week[df_filter_this_week["Day"] == "Thursday"])
        
    if left.button(f'Tuesday - {tuesday} clients'):
        if tuesday==0:
            st.info('No appointments', icon="âšī¸")
        else:
            df_filter_this_week_tuesday = df_filter_this_week[df_filter_this_week["Day"] == "Tuesday"]

            
            df_show = df_filter_this_week_tuesday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                   "Type of reparation", "Remarks"]].T
            columns = []
            for i in range(df_show.shape[1]):
                columns.append(f"Client {i + 1}")
            df_show.columns = columns
            st.dataframe(df_show, use_container_width=True)
    
    if right.button(f'Thursday - {thursday} clients'):
        if thursday==0:
            st.info('No appointments', icon="âšī¸")
        else:
            df_filter_this_week_thursday = df_filter_this_week[df_filter_this_week["Day"] == "Thursday"]

            
            df_show = df_filter_this_week_thursday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                   "Type of reparation", "Remarks"]].T
            
            columns = []
            for i in range(df_show.shape[1]):
                columns.append(f"Client {i + 1}")
            df_show.columns = columns
            st.dataframe(df_show, use_container_width=True)
                      
elif selected == len_next_week:
    left, right = st.columns([1, 1])
            
    tuesday = len(df_filter_next_week[df_filter_next_week["Day"] == "Tuesday"])
    thursday = len(df_filter_next_week[df_filter_next_week["Day"] == "Thursday"])
        
    if left.button(f'Tuesday - {tuesday} clients'):
        if tuesday==0:
            st.info('No appointments', icon="âšī¸")
        else:
            df_filter_next_week_tuesday = df_filter_next_week[df_filter_next_week["Day"] == "Tuesday"]

            
            df_show = df_filter_next_week_tuesday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                   "Type of reparation", "Remarks"]].T
            columns = []
            for i in range(df_show.shape[1]):
                columns.append(f"Client {i + 1}")
            df_show.columns = columns
            st.dataframe(df_show, use_container_width=True)
            
        
    if right.button(f'Thursday - {thursday} clients'):
        if thursday==0:
            st.info('No appointments', icon="âšī¸")
        else:
            df_filter_next_week_thursday = df_filter_next_week[df_filter_next_week["Day"] == "Thursday"]

            
            df_show = df_filter_next_week_thursday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                   "Type of reparation", "Remarks"]].T
            
            columns = []
            for i in range(df_show.shape[1]):
                columns.append(f"Client {i + 1}")
            df_show.columns = columns
            st.dataframe(df_show, use_container_width=True)
       
        
