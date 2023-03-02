import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure
import altair as alt


def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset

database_link = "https://raw.githubusercontent.com/fivethirtyeight/data/master/covid-geography/mmsa-icu-beds.csv"
database_data = load_dataset(database_link)
st.title("DATOS COVID-19")
st.dataframe(database_data)
_min=0
_max=0
arr_hosp = []
arr_arcu = []
fig=0

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
    ('','Alto riesgo por cama UCI en cada hospital', 'Alto riesgo por hospital en cada área', 'Camas UCI por área', 'Hospitales en cada área', 'Riesgo Total en cada área','Hospitales existentes')
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
        
xs = database_data.icu_beds
xt = database_data.high_risk_per_ICU_bed
for i in xs:
    if (pd.isna(i)):
        i=0
        arr_hosp.append(int(i))
    else:
        arr_hosp.append(int(i))
        
for i in xt:
    if (pd.isna(i)):
        i=0
        arr_arcu.append(int(i))
    else:
        arr_arcu.append(int(i))

if(len(selected_decks) > 0):
    for i in selected_decks:
        df = database_data
        da = df[database_data["MMSA"] == i]
        st.write(da)

if option == '':
    st.write()


x = arr_hosp
y = arr_arcu

p = figure(
    title='Riesgo por cama según hospital',
    x_axis_label='x',
    y_axis_label='y')
if option == 'Alto riesgo por cama UCI en cada hospital':
    df = database_data[["MMSA", 'high_risk_per_ICU_bed']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    p.line(x, y, legend_label='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)

if option == 'Alto riesgo por hospital en cada área':
    chart = alt.Chart(database_data).mark_circle().encode(
        x='MMSA',
        y='high_risk_per_hospital',
        color='hospitals',
    ).interactive()

    tab1, tab2 = st.tabs(["Bonito", "Nativo"])

    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)

if option == 'Camas UCI por área':
    df = database_data[["MMSA", 'icu_beds']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.area_chart(chart_df, x=["MMSA"], y='icu_beds')
    
if option == 'Hospitales en cada área':
    df = database_data[["MMSA", 'hospitals']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.line_chart(chart_df, x=["MMSA"], y='hospitals')
    
if option == 'Hospitales existentes':
    st.header(option)
    fig, ax = plt.subplots()
    ax.hist(arr_hosp, bins=20)
    st.pyplot(fig)

if option == 'Riesgo Total en cada área':
    df = database_data[["MMSA", 'total_at_risk']]
    chart_df = df.groupby(['MMSA']).sum()
    st.header(option)
    st.bar_chart(chart_df, x=["MMSA"], y='total_at_risk')
    



