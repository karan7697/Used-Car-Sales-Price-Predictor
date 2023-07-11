import streamlit as st
import pandas as pd
import numpy as np
import io
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle
import json
import sklearn
import requests

data = pd.read_csv(r"cars_new.csv")
data2 = pd.read_csv(r"CarsML.csv")

data_num = data[['odometer_value', 'year_produced', 'price_usd', 'number_of_photos', 'up_counter', 'duration_listed']]
data_obj = data[
    ['manufacturer_name', 'model_name', 'transmission', 'color', 'engine_fuel', 'engine_type', 'body_type', 'state',
     'drivetrain', 'location_region']]
data_bool = data[
    ['transmission', 'color', 'engine_fuel', 'engine_type', 'body_type', 'manufacturer_name', 'engine_has_gas',
     'has_warranty', 'is_exchangeable', 'sunroof', 'ABS', 'heated seats', 'dualzone AC', 'hill assist',
     'Cruise control', 'TPM system', 'GPS', 'Electric Seats', 'lane assist']]

x = st.sidebar.selectbox('Navigation:', ['Home', 'Dataset Overview', 'Dataset Information', 'Dataset Description',
                                         'Dataset Analysis/ Visualisations', 'Find Your Car','Find Selling Price'])

if x == 'Home':
    st.title('Used Car MarketPlace!')
    st.markdown(
        'In this project I look into one of the biggest markets today that is the used car markets where people sell their cars.')
    st.image(
        'https://thumbor.forbes.com/thumbor/fit-in/960x/https://www.forbes.com/wheels/wp-content/uploads/2022/07/Used_Car_Shopping_1.jpg')

if x == 'Dataset Overview':
    st.title('Ovreview of the dataset:')
    st.write(data.head())

if x == 'Dataset Information':
    st.title('Information of the dataset:')
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

if x == 'Dataset Description':
    st.title('Description of the Dataset:')
    st.write(data.describe())

if x == 'Dataset Analysis/ Visualisations':
    st.title('Analysis and Dashboard:')
    x1 = st.sidebar.radio('Select Type of Graph:', ['1. Countplot', '2. Line Plot', '3. Relation Plot', '4. Piechart'])

    if x1 == '1. Countplot':
        col = st.sidebar.radio('Select Columns:', data_obj.columns)
        fig = plt.figure(figsize=(14, 7))
        p = sns.countplot(x=col, data=data)
        p.tick_params(axis='x', rotation=90)
        st.pyplot(fig)

    if x1 == '2. Line Plot':
        col1 = st.selectbox('Select Columns:', data_num.columns, key=1)
        col2 = st.selectbox('Select Columns:', data_num.columns, key=2)
        col3 = st.selectbox('Select Columns:', data_bool.columns, key=3)
        fig = plt.figure(figsize=(14, 7))
        # st.line_chart(data=data,x=col1, y=col2)
        sns.lineplot(x=col1, y=col2, hue=col3, data=data)
        st.pyplot(fig)

    if x1 == '3. Relation Plot':
        col1 = st.selectbox('Select Columns:', data_num.columns, key=1)
        col2 = st.selectbox('Select Columns:', data_num.columns, key=2)
        col3 = st.selectbox('Select Columns:', data_bool.columns, key=3)
        fig = plt.figure(figsize=(14, 7))
        p = sns.scatterplot(data=data, x=col1, y=col2, hue=col3)
        st.pyplot(fig)

    if x1 == '4. Piechart':
        input_col, pie_col = st.columns(2)
        col1 = st.selectbox('Select Columns:', data_bool.columns, key=1)
        fig = px.pie(data, names=col1, color_discrete_sequence=px.colors.sequential.RdBu, width=800, height=400)
        fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
        pie_col.write(fig)

if x == 'Find Your Car':
    st.title('Find the Perfect Car:')
    # st.dataframe(data)

    company = data['manufacturer_name'].unique().tolist()
    price = data['price_usd'].unique().tolist()
    body_types = data['body_type'].unique().tolist()
    colors = data['color'].unique().tolist()
    odometer = data['odometer_value'].unique().tolist()

    price_selection = st.slider('Price Range:', min_value=min(price), max_value=max(price),
                                value=(min(price), max(price)))
    odometer_selection = st.slider('Odometer Range', min_value=min(odometer), max_value=max(odometer),
                                   value=(min(odometer), max(odometer)))
    company_selection = st.multiselect('Select Company:', company)
    bodytype_selection = st.multiselect('Select Body Type:', body_types)
    color_selection = st.multiselect('Select Color:', colors)

    mask = (data['price_usd'].between(*price_selection)) & (data['odometer_value'].between(*odometer_selection)) & (
        data['manufacturer_name'].isin(company_selection)) & (data['body_type'].isin(bodytype_selection)) & (
               data['color'].isin(color_selection))
    number_of_result = data[mask].shape[0]
    result = data[mask]
    result = result.reset_index()
    st.markdown(f'*Available Results: {number_of_result}*')
    st.write(result)

if x == 'Find Selling Price':

    st.title('Predict the Price of the Car!')
    model = pickle.load(open('model_2.pkl', 'rb'))

    # wheelbase1 = data2['wheelbase'].unique().tolist()
    # carlenght1 = data2['carlength'].unique().tolist()
    # carwidth1 = data2['carwidth'].unique().tolist()
    # carheight1 = data2['carheight'].unique().tolist()
    # curbweight1 = data2['curbweight'].unique().tolist()
    # enginsize1 = data2['enginesize'].unique().tolist()
    # boreratio1 = data2['boreratio'].unique().tolist()
    # stroke1 = data2['stroke'].unique().tolist()
    # compressionratio1 = data2['compressionratio'].unique().tolist()
    # horsepower1 = data2['horsepower'].unique().tolist()
    # peakrpm1 = data2['peakrpm'].unique().tolist()

    wheelbase_selection = st.slider('Wheelbase Range:', 10.0,130.0,25.0)
    carlenght_selection = st.slider('Lenght Of Car:', 130.0,240.0, 140.0)
    carwidth_selection = st.slider('Width of Car:', 50.0,80.0, 65.0)
    carheight_selection = st.slider('Height of Car:', 45.0,70.0, 50.0)
    curbweight_selection = st.slider('Curb Weight Of Car:',1200,4500, 1500)
    engine_selection = st.slider('Engine Capacity:', 55,3500, 140)
    boreratio_selection = st.slider('Bore Ratio:', 1.0,5.0, 2.0)
    stroke_selection = st.slider('Stroke Range:', 2.0,6.0, 3.0)
    compression_selection = st.slider('Engine Compression Range:', 5.0,30.0, 14.0)
    horsepower_selection = st.slider('Horse Power of the car:',40.0,450.0, 150.0)
    peakrpm_selection = st.slider('Peak RPM:', 4000,12000, 5000)

    makeprediction = model.predict([[float(wheelbase_selection), float(carlenght_selection), float(carwidth_selection),
                                     float(carheight_selection), int(curbweight_selection), int(engine_selection),
                                     float(boreratio_selection), float(stroke_selection), float(compression_selection),
                                     float(horsepower_selection), int(peakrpm_selection)]])
    output = makeprediction[0]
#     Prediction code
    if st.button('Predict Price'):
        st.success('You Can Sell Your Car for {}'.format(output))