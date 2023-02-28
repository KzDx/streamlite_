import pandas as pd
import time
import streamlit as st

def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset

database_link = "https://raw.githubusercontent.com/fivethirtyeight/data/master/covid-geography/mmsa-icu-beds.csv"
database_data = load_dataset(database_link)
st.dataframe(database_data)