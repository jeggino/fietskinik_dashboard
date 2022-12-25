import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt


time_shift_choice = ["14-16", "16-18", "18-20"]

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])
date =  str(st.date_input("Choose a date"))


# Create a new database
db = deta.Base("project_fietskliniek")
db_content = db.fetch().items
df = pd.DataFrame(db_content)
df_filter_data = df[df.date==date]

if len(df_filter_data)==0:
  st.info('No appointments', icon="ℹ️")

else:
  col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
  time_shift = col1.selectbox('Chose a time shift',time_shift_choice)
  df_filter_time = df_filter_data[df_filter_data.time_shift==time_shift].sort_values("time_shift").reset_index(drop=True)
  
  n_1 = len(df_filter_data[df_filter_data.time_shift=="14-16"])
  n_2 = len(df_filter_data[df_filter_data.time_shift=="16-18"])
  n_3 = len(df_filter_data[df_filter_data.time_shift=="18-20"])

  col2.metric("14-16", f"{n_1} clients")
  col3.metric("16-18", f"{n_2} clients")
  col4.metric("18-20", f"{n_3} clients")
    
  st.dataframe(df_filter_time[["name","e_mail","buurt","opmerking","materiaal","werkzaamheedeb"]].T, use_container_width=True)
  
  
placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Hello")

# Replace the text with a chart:
placeholder.line_chart({"data": [1, 5, 2, 6]})

# Replace the chart with several elements:
with placeholder.container():
    st.write("This is one element")
    st.write("This is another")

# Clear all those elements:
placeholder.empty()



