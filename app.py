import streamlit as st  
from streamlit_option_menu import option_menu  
from deta import Deta
import pandas as pd
import altair as alt
import mapclassify
from datetime import datetime as dt


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

#---PASSWORD---
placeholder = st.empty()
password = placeholder.text_input("Password", value=None, label_visibility= 'collapsed', placeholder = "schrijf hier uw wachtwoord ...",)


if password == 'fietskliniek':
    placeholder.empty()

elif password == None:
            st.stop()

else:
            st.error("Verkeerd wachtwoord ...")
            st.stop()


#---APP---
def Agenda():

    # ---Connect to Deta Base with your Project Key---
    deta = Deta(st.secrets["deta_key"])
    db = deta.Base("db_data")
    db_content = db.fetch().items
    df = pd.DataFrame(db_content)
    drive = deta.Drive("df_pictures")
    
    df['Date'] =  pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['year'] = df['Date'].dt.year
     
        
    this_week = dt.today().isocalendar()[1]
    next_week = dt.today().isocalendar()[1] + 1
    year = dt.today().isocalendar()[0]
    df_filter_this_week = df[(df["Week"]==this_week)&(df["year"]==year)]
    df_filter_next_week = df[(df["Week"]==next_week)&(df["year"]==year)]
    
    len_this_week = f"This week - {len(df_filter_this_week)} clients"
    len_next_week = f"Next week - {len(df_filter_next_week)} clients"
    
    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=[len_this_week, len_next_week],
        orientation="horizontal",
    )
    
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df)
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='fietskliniek_df.csv',
        mime='text/csv',
    )
    
    
    
    if selected == len_this_week:
        left, middle, right = st.columns([1, 1, 1])
                
        tuesday = len(df_filter_this_week[df_filter_this_week["Day"] == "Tuesday"])
        thursday = len(df_filter_this_week[df_filter_this_week["Day"] == "Thursday"])
        friday = len(df_filter_this_week[df_filter_this_week["Day"] == "Friday"])
            
        if left.button(f'Tuesday - {tuesday} clients'):
            if tuesday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                df_filter_this_week_tuesday = df_filter_this_week[df_filter_this_week["Day"] == "Tuesday"]
    
                
                df_show = df_filter_this_week_tuesday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                       "Type of reparation", "Remarks"]].T
                columns = []
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                for client, pics, comments in zip(columns, df_filter_this_week_tuesday["Name_picture"], df_filter_this_week_tuesday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue
        
        if middle.button(f'Thursday - {thursday} clients'):
            if thursday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                df_filter_this_week_thursday = df_filter_this_week[df_filter_this_week["Day"] == "Thursday"]
    
                
                df_show = df_filter_this_week_thursday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                       "Type of reparation", "Remarks"]].T
                
                columns = []
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                for client, pics, comments in zip(columns, df_filter_this_week_thursday["Name_picture"], df_filter_this_week_thursday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue
    
        if right.button(f'Friday - {friday} clients'):
            if friday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                df_filter_this_week_friday = df_filter_this_week[df_filter_this_week["Day"] == "Friday"]
    
                
                df_show = df_filter_this_week_friday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                       "Type of reparation", "Remarks"]].T
                
                columns = []
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                for client, pics, comments in zip(columns, df_filter_this_week_friday["Name_picture"], df_filter_this_week_friday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue
                          
    elif selected == len_next_week:
        left, middle, right = st.columns([1, 1, 1])
                
        tuesday = len(df_filter_next_week[df_filter_next_week["Day"] == "Tuesday"])
        thursday = len(df_filter_next_week[df_filter_next_week["Day"] == "Thursday"])
        friday = len(df_filter_next_week[df_filter_next_week["Day"] == "Friday"])
            
        if left.button(f'Tuesday - {tuesday} clients'):
            if tuesday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                df_filter_next_week_tuesday = df_filter_next_week[df_filter_next_week["Day"] == "Tuesday"]
    
                
                df_show = df_filter_next_week_tuesday[["Membership","Membership_number","Time shift", "Name", "e_mail", "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                       "Type of reparation", "Remarks"]].T
                columns = []
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                for client, pics, comments in zip(columns, df_filter_next_week_tuesday["Name_picture"], df_filter_next_week_tuesday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue
        if middle.button(f'Thursday - {thursday} clients'):
            if thursday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                df_filter_next_week_thursday = df_filter_next_week[df_filter_next_week["Day"] == "Thursday"]
    
                
                df_show = df_filter_next_week_thursday[["Membership","Membership_number","Time shift", "Name", "e_mail", 
                                                        "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                       "Type of reparation", "Remarks"]].T
                
                columns = []
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                for client, pics, comments in zip(columns, df_filter_next_week_thursday["Name_picture"], df_filter_next_week_thursday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue
    
        if right.button(f'Friday - {friday} clients'):
            if friday==0:
                st.info('No appointments', icon="ℹ️")
            else:
                
                df_filter_next_week_friday = df_filter_next_week[df_filter_next_week["Day"] == "Friday"]
                          
                df_show = df_filter_next_week_friday[["Membership","Membership_number","Time shift", "Name", "e_mail", 
                                                      "Phone number", "Neighborhood", "Expertise", "Type of bike",
                                                      "Type of reparation", "Remarks"]].T
                
                columns = []
                
                for i in range(df_show.shape[1]):
                    columns.append(f"Client {i + 1}")
                    
                df_show.columns = columns
                st.dataframe(df_show, use_container_width=True)
    
                df_pictures_2 = df_filter_next_week_friday["Name_picture"]
                df_pictures_2.index = columns
                for client, pics, comments in zip(columns, df_filter_next_week_friday["Name_picture"], df_filter_next_week_friday["Remarks"]):
                    try:
                        res = drive.get(pics).read()
                        st.image(res,caption=f"{client} - {comments}")
                    except:
                        continue


def Statistik():
            image = "https://www.thesignmaker.co.nz/wp-content/uploads/2019/04/C16_Work-In-Progress.png"
            st.image(image)
            
    


pg = st.navigation([st.Page(Agenda,icon="📓"), st.Page(Statistik,icon="📊")])
pg.run()

