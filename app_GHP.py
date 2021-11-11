# Data visualization project for GHP
# 
# By: Jose, Rafael and Diego

# libraries

import streamlit as st
from interfaces.Venues import get_venues_interface
from interfaces.Materials import get_materials_interface



############################################################################################
#Barside
############################################################################################
#barside helpers
st.sidebar.image('src/img/ghp.png', width=200)
st.sidebar.header('Visualization')
# title
st.title('GHP Data Visualization Project')

menu = st.sidebar.radio(
    "",
    ("Venues", "Materials", "Purchases", 'Vendor'),
)
st.sidebar.markdown('---')

st.sidebar.write('Jose Gonzalez | Diego Samano | Rafa Velasco | Noviembre 2021')

if menu == 'Venues':
    get_venues_interface()
elif menu == 'Materials':
    get_materials_interface()
# elif menu == 'Variables de estudio':
#     set_variables()
# elif menu == 'Otras variables':
#     set_otras_variables()
# elif menu == 'Relaciones entre variables':
#     set_relations()
# elif menu == 'Matrices de correlación':
#     set_arrays()
# data 
