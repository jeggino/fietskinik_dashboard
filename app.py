import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt


time_shift_choice = ["14-16", "16-18", "18-20"]

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
date =  str(st.date_input("Choose a date"))
time_shift = st.multiselect('Chose a time shift',time_shift_choice, time_shift_choice)

# Create a new database
db = deta.Base("project_fietskliniek")
db_content = db.fetch().items
df = pd.DataFrame(db_content)
df_filter = df[(df.date==date) & (df.time_shift.isin(time_shift))].T


st.dataframe(df_filter)
