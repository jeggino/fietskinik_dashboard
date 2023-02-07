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
left, right = st.columns([1, 1]) 
if selected == "Agenda":
    
    week_1 = dt.today().isocalendar()[1]
    week_2 = dt.today().isocalendar()[1] + 1
    df_filter_week_1 = df[(df["Week"]==week_1)]
    df_filter_week_2 = df[(df["Week"]==week_2)]
    
    option = st.selectbox(
        'Select a week',
        ('This week', 'Next week'))
    
    
    
    
    if option == 'This week':
        if len(df_filter_week_1)==0:
          st.info('No appointments', icon="ℹ️")

        else:
            option_day = st.selectbox(
                'Select a day',
                ('select a day ','Tuesday', 'Thursday'))
            
            tuesday = len(df_filter_week_1[df_filter_week_1["Day"] == "Tuesday"])
            thursday = len(df_filter_week_1[df_filter_week_1["Day"] == "Thursday"])
            left.metric("Tuesday", f"{tuesday} clients")
            right.metric("Thursday", f"{thursday} clients")
            
            
            
            df_filter_week_1 = df_filter_week_1[df_filter_week_1["Day"]==option_day]
            
            if option_day == 'Tuesday':
                if len(df_filter_week_1)==0:
                    st.info('No appointments', icon="ℹ️")
                else:
                    col2, col3, col4 = st.columns([1, 1, 1])

                    n_1 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "14-16"])
                    n_2 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "16-18"])
                    n_3 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "18-20"])

                    col2.metric("14-16", f"{n_1} clients")
                    col3.metric("16-18", f"{n_2} clients")
                    col4.metric("18-20", f"{n_3} clients")

                    option_time = st.selectbox(
                        'Select a time shift',
                        ("14-16",  "16-18", "18-20"))

                    df_filter_week_1 = df_filter_week_1[df_filter_week_1["Time shift"]==option_time]

                    columns = []
                    df_show = df_filter_week_1[[ "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                 "Type of reparation", "Remarks"]].T
                    if len(df_filter_week_1)==0:
                        st.info('No appointments', icon="ℹ️")
                    else:
                        for i in range(df_show.shape[1]):
                            columns.append(f"Client {i + 1}")
                        df_show.columns = columns
                        st.dataframe(df_show, use_container_width=True)
                    
            elif option_day == 'Thursday':
                if len(df_filter_week_1)==0:
                    st.info('No appointments', icon="ℹ️")
                else:
                    col2, col3, col4 = st.columns([1, 1, 1])

                    n_1 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "14-16"])
                    n_2 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "16-18"])
                    n_3 = len(df_filter_week_1[df_filter_week_1["Time shift"] == "18-20"])

                    col2.metric("14-16", f"{n_1} clients")
                    col3.metric("16-18", f"{n_2} clients")
                    col4.metric("18-20", f"{n_3} clients")

                    option_time = st.selectbox(
                        'Select a time shift',
                        ("14-16",  "16-18", "18-20"))

                    df_filter_week_1 = df_filter_week_1[df_filter_week_1["Time shift"]==option_time]
                               
                    columns = []
                    df_show = df_filter_week_1[["Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                 "Type of reparation", "Remarks"]].T
                    if len(df_filter_week_1)==0:
                        st.info('No appointments', icon="ℹ️")
                    else:
                        for i in range(df_show.shape[1]):
                            columns.append(f"Client {i + 1}")
                        df_show.columns = columns
                        st.dataframe(df_show, use_container_width=True)
            
    elif option == 'Next week':
        if len(df_filter_week_2)==0:
          st.info('No appointments', icon="ℹ️")

        else:
            
            option_day = st.selectbox(
                'Select a day',
                ('select a day ','Tuesday', 'Thursday'))
            
            tuesday = len(df_filter_week_2[df_filter_week_2["Day"] == "Tuesday"])
            thursday = len(df_filter_week_2[df_filter_week_2["Day"] == "Thursday"])
            left.metric("Tuesday", f"{tuesday} clients")
            right.metric("Thursday", f"{thursday} clients")
            
            df_filter_week_2 = df_filter_week_2[df_filter_week_2["Day"]==option_day]
            
            if option_day == 'Tuesday':
                if len(df_filter_week_2)==0:
                    st.info('No appointments', icon="ℹ️")
                else:
                    col2, col3, col4 = st.columns([1, 1, 1])

                    n_1 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "14-16"])
                    n_2 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "16-18"])
                    n_3 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "18-20"])

                    col2.metric("14-16", f"{n_1} clients")
                    col3.metric("16-18", f"{n_2} clients")
                    col4.metric("18-20", f"{n_3} clients")

                    option_time = st.selectbox(
                        'Select a time shift',
                        ("14-16",  "16-18", "18-20"))

                    df_filter_week_2 = df_filter_week_2[df_filter_week_2["Time shift"]==option_time]

                    columns = []
                    df_show = df_filter_week_2[[ "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                 "Type of reparation", "Remarks"]].T
                    if len(df_filter_week_2)==0:
                        st.info('No appointments', icon="ℹ️")
                    else:
                        for i in range(df_show.shape[1]):
                            columns.append(f"Client {i + 1}")
                        df_show.columns = columns
                        st.dataframe(df_show, use_container_width=True)
                    
            elif option_day == 'Thursday':
                if len(df_filter_week_2)==0:
                    st.info('No appointments', icon="ℹ️")
                else:
                    col2, col3, col4 = st.columns([1, 1, 1])

                    n_1 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "14-16"])
                    n_2 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "16-18"])
                    n_3 = len(df_filter_week_2[df_filter_week_2["Time shift"] == "18-20"])

                    col2.metric("14-16", f"{n_1} clients")
                    col3.metric("16-18", f"{n_2} clients")
                    col4.metric("18-20", f"{n_3} clients")

                    option_time = st.selectbox(
                        'Select a time shift',
                        ("14-16",  "16-18", "18-20"))

                    df_filter_week_2 = df_filter_week_2[df_filter_week_2["Time shift"]==option_time]
                               
                    columns = []
                    df_show = df_filter_week_2[["Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                 "Type of reparation", "Remarks"]].T
                    if len(df_filter_week_2)==0:
                        st.info('No appointments', icon="ℹ️")
                    else:
                        for i in range(df_show.shape[1]):
                            columns.append(f"Client {i + 1}")
                        df_show.columns = columns
                        st.dataframe(df_show, use_container_width=True)
        
if selected == "Dashboard":

    st.info("... let's do it later!", icon="🚲")
    
    source = df.groupby('Date',as_index=False).size()

    time_series = alt.Chart(source
             ).mark_bar(
    ).encode(
        x=alt.X('Date:T', axis=alt.Axis(domain=False, format='%Y-%d-%b (%A)', tickSize=0)),
        y=alt.Y('size:Q', axis=None)
    )

    st.altair_chart(time_series)
        
        
    with left:
        source_3 = df.groupby('Expertise',as_index=False).size()
        base = alt.Chart(source_3).encode(
        theta=alt.Theta("size:Q", stack=True),
        radius=alt.Radius("size", scale=alt.Scale(type="sqrt", zero=True)),
        color="size:N",
        )

        c1 = base.mark_arc(innerRadius=20, stroke="#fff")

        c2 = base.mark_text(radiusOffset=30).encode(text="Neighborhood:N")

        pie_chart = c1 + c2
        st.altair_chart(pie_chart)
        
    
    with right:
        source_2 = df.groupby('Neighborhood',as_index=False).size()
        base = alt.Chart(source_2).encode(
        theta=alt.Theta("size:Q", stack=True),
        radius=alt.Radius("size", scale=alt.Scale(type="sqrt", zero=True)),
        color="size:N",
        )

        c1 = base.mark_arc(innerRadius=20, stroke="#fff")

        c2 = base.mark_text(radiusOffset=30).encode(text="Neighborhood:N")

        pie_chart = c1 + c2
        st.altair_chart(pie_chart)
       
        
