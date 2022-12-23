import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
from dateutil import parser


# Connect to Deta Base with your Project Key
deta = Deta(st.secrets["deta_key"])

# Create a new database
db = deta.Base("project_fietskliniek")

# find if there are available shift in that data
db_content = db.fetch().items
df = pd.DataFrame(db_content)

st.dataframe(df)
