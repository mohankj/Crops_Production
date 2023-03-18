import streamlit as st
import numpy as np
import pandas as pd
import pickle
import time
import base64

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: 2000px 900px;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('img\crp.gif')


st.set_page_config(layout="wide")

video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%; 
		  min-height: 100%;
		}

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}

		</style>	
		<video autoplay muted loop id="myVideo">
		  <source src="https://v1.pinimg.com/videos/mc/720p/c6/74/94/c674943f324f2210c1b9e5d7766ebf30.mp4")>
		  Your browser does not support HTML5 video.
		</video>
        """

st.markdown(video_html, unsafe_allow_html=True)
st.title('Crops Production')


st.subheader('Predict the Production of Crops at any Particular Season')

with open('Production_Model/mapping_dict.pkl', 'rb') as f:
    mapping_dict = pickle.load(f)

with open('Production_Model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('Production_Model/original_data.pkl', 'rb') as f:
    data = pickle.load(f)


def predict(State,District,Crop,Season,Area):
    ## Predicting the Production Of Crops.
    state = mapping_dict['State'][State]
    district = mapping_dict['District'][District]
    crop = mapping_dict['Crop'][Crop]
    season = mapping_dict['Season'][Season]
    
    

    prediction = model.predict(pd.DataFrame(np.array([state,district,crop,season,Area]).reshape(1,5),columns=['State','District','Crop','Season','Area']))
    prediction = float(prediction)
    prediction = round(prediction,2)
    return prediction

# Input
state_list = data['State'].unique()
selected_state = st.selectbox(
    "Type or select a State from the dropdown",
    options = state_list
)

district_list = data['District'].unique()
selected_district = st.selectbox(
    "Type or select a District from the dropdown",
    district_list
)

crop_list = data['Crop'].unique()
selected_crop = st.selectbox(
    "Type or select a Crops from the dropdown",
    crop_list
)

season_list = data['Season'].unique()
selected_season = st.selectbox(
    "Type or select a Season from the dropdown",
    season_list
)

area = st.number_input('Areas of Plot in (Hectares):', min_value=0.00001, max_value=100000000.0, value=1.0)


if st.button('Predict Production'):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
        if percent_complete==98:
            my_bar.progress(percent_complete+1,text="Sucessfully Completed")
        

    col1,col2,col3,col4,col5,col6 =st.columns(6)
    col1.subheader(predict(selected_state,selected_district,selected_crop,selected_season,area))
    col3.subheader('Tonnes of')
    col4.subheader(selected_crop)
    # col5.subheader('Produced in')
    # col6.subheader(selected_season)





