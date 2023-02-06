import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
import mapclassify


# ---INSET PASSWORD---
passwords = ["fietskliniek"]
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
    
    week_1 = dt.today().isocalendar()[1]
    week_2 = dt.today().isocalendar()[1] + 1
    df_filter_data = df[(df["Week"]==week_1) or (df["Week"]==week_2)]
#     date =  str(st.date_input("Choose a date"))
#     df_filter_data = df[df["Date"]==date]

#     # Using "with" notation
    if len(df_filter_data)==0:
      st.info('No appointments', icon="ℹ️")

    else:
        st.dataframe(df_filter_time[["Date", "Week", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                              "Type of reparation", "Remarks"]].T, use_container_width=True)
#       col2, col3, col4 = st.columns([1, 1, 1])
#       time_shift_empty = st.empty()
#       time_shift = time_shift_empty.radio('Chose a time shift',time_shift_choice, horizontal=True)

#       df_filter_time = df_filter_data[df_filter_data["Time shift"]==time_shift].sort_values("Time shift").reset_index(drop=True)

#       n_1 = len(df_filter_data[df_filter_data["Time shift"] == "14-16"])
#       n_2 = len(df_filter_data[df_filter_data["Time shift"] == "16-18"])
#       n_3 = len(df_filter_data[df_filter_data["Time shift"] == "18-20"])

#       col2.metric("14-16", f"{n_1} clients")
#       col3.metric("16-18", f"{n_2} clients")
#       col4.metric("18-20", f"{n_3} clients")

# #       placeholder = st.empty()
# #       placeholder.dataframe(df_filter_time[["Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
# #                                             "Type of reparation", "Remarks"]].T, use_container_width=True)
# #       if not st.checkbox('Show table'):
# #         placeholder.empty()
# #         time_shift_empty.empty()
        
if selected == "Dashboard":

    st.info("... let's do it later!", icon="🚲")
       
        
