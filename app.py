import pandas as pd
import streamlit as st


def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset

database_link = "https://raw.githubusercontent.com/fivethirtyeight/data/master/covid-geography/mmsa-icu-beds.csv"
database_data = load_dataset(database_link)
st.dataframe(database_data)
_min=0
_max=0

with st.sidebar:
    st.title("Análisis de COVID-19 por área metropolitana")
    selected_decks = st.multiselect(
        "Señala el área a evaluar", database_data['MMSA'].unique())  
    st.title("Según que rango quieres evaluar")
    ev_data = st.radio(
    "Opciones:",
    ('','Porcentaje total de riesgo', 'Riesgo por cama de UCI','Riesgo por hospital'))
    
    if ev_data == "":
        st.write()

    if ev_data == 'Porcentaje total de riesgo':
        max_ = database_data['total_percent_at_risk'].max()
        min_ = database_data['total_percent_at_risk'].min()
        st.title("Análisis de COVID-19 por porcentaje de riesgo")
        optionals = st.expander("Señala el rango de porcentajes de riesgo", True)
        _min = optionals.slider(
            "Porcentaje mínimo de riesgo",
            min_value=float(min_.replace('%', ''))-1,
            max_value=float(max_.replace('%', ''))
        )
        _max = optionals.slider(
            "Porcentaje máximo de riesgo",

            min_value=float(min_.replace('%', ''))-1,
            max_value=float(max_.replace('%', ''))
        )

        
    if ev_data == 'Riesgo por cama de UCI':
        max_ = database_data['high_risk_per_ICU_bed'].max()
        min_ = database_data['high_risk_per_ICU_bed'].min()
        st.title("Análisis de riesgo de COVID-19 por cama UCI")
        optionals = st.expander("Señala el rango de riesgos por cama UCI", True)
        _min = optionals.slider(
            "Riesgo mínimo",
            min_value=float(min_),
            max_value=max_
        )
        _max = optionals.slider(
            "Riesgo máximo",

            min_value=float(min_),
            max_value=max_
        )
        
    if ev_data == 'Riesgo por hospital':
        max_ = database_data['high_risk_per_hospital'].max()
        min_ = database_data['high_risk_per_hospital'].min()
        st.title("Análisis de riesgo de COVID-19 por hospital")
        optionals = st.expander("Señala el rango de riesgos por hospital", True)
        _min = optionals.slider(
            "Riesgo mínimo",
            min_value=float(min_),
            max_value=max_
        )
        _max = optionals.slider(
            "Riesgo máximo",

            min_value=float(min_),
            max_value=max_
        )

    st.title("Datos gráficos de las evaluaciones por área")
    option = st.selectbox(
    'Opciones',
    ('','Alto riesgo por cama UCI en cada área', 'Alto riesgo por hospital en cada área', 'Camas UCI por área', 'Hospitales en cada área', 'Riesgo Total en cada área')
    )
min_ = database_data[database_data['total_percent_at_risk']>= ((str(_min) + "%") + ("%"))]
max_ = min_[database_data['total_percent_at_risk'] <= ((str(_max) + "%") + ("%"))]
chart_df = max_.groupby(["MMSA"]).sum()
chart_df["MMSA"] = chart_df.index      
if(len(max_) == 0):
    st.write("")
else:
    st.write(max_)

min_ = database_data[database_data['high_risk_per_ICU_bed']>= _min]
max_ = min_[database_data['high_risk_per_ICU_bed'] <= _max]
chart_df = max_.groupby(["MMSA"]).sum()
chart_df["MMSA"] = chart_df.index      
if(len(max_) == 0):
    st.write("")
else:
    st.write(max_)

min_ = database_data[database_data['high_risk_per_hospital']>= _min]
max_ = min_[database_data['high_risk_per_hospital'] <= _max]
chart_df = max_.groupby(["MMSA"]).sum()
chart_df["MMSA"] = chart_df.index      
if(len(max_) == 0):
    st.write("")
else:
    st.write(max_)
        

if(len(selected_decks) > 0):
    for i in selected_decks:
        df = database_data
        da = df[database_data["MMSA"] == i]
        st.write(da)

if option == '':
    st.write()

if option == 'Alto riesgo por cama UCI en cada área':
    df = database_data[["MMSA", 'high_risk_per_ICU_bed']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.line_chart(chart_df, x=["MMSA"], y='high_risk_per_ICU_bed')

if option == 'Alto riesgo por hospital en cada área':
    df = database_data[["MMSA", 'high_risk_per_hospital']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.line_chart(chart_df, x=["MMSA"], y='high_risk_per_hospital')

if option == 'Camas UCI por área':
    df = database_data[["MMSA", 'icu_beds']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.line_chart(chart_df, x=["MMSA"], y='icu_beds')

if option == 'Hospitales en cada área':
    df = database_data[["MMSA", 'hospitals']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.line_chart(chart_df, x=["MMSA"], y='hospitals')
    
if option == 'Riesgo Total en cada área':
    df = database_data[["MMSA", 'total_at_risk']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.bar_chart(chart_df, x=["MMSA"], y='total_at_risk')



