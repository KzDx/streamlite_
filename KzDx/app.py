import pandas as pd
import time
import streamlit as st

def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset

titanic_link = "https://raw.githubusercontent.com/fivethirtyeight/data/master/covid-geography/mmsa-icu-beds.csv"
titanic_data = load_dataset(titanic_link)
st.dataframe(titanic_data)