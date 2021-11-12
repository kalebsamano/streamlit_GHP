# Data visualization project for GHP
# 
# By: Jose, Rafael and Diego
# libraries
import streamlit as st
from interfaces.Vendors import get_vendors_interface
from interfaces.Venues import get_venues_interface
from interfaces.Materials import get_materials_interface
from interfaces.Purchases import get_purchases_interface
############################################################################################
#Barside
############################################################################################
#barside helpers
st.sidebar.image('src/img/ghp.png', width=200)
st.sidebar.header('Visualization')
# title
st.title('GHP Data Visualization Project')
# menu
menu = st.sidebar.radio(
    "",
    ("Venues", "Materials", "Vendors", 'Purchases'),
)
# sidebar
st.sidebar.markdown('---')
st.sidebar.write('Jose Gonzalez | Diego Samano | Rafael Velasco | Noviembre 2021')
# menu options
if menu == 'Venues':
    get_venues_interface()
elif menu == 'Materials':
    get_materials_interface()
elif menu == 'Vendors':
     get_vendors_interface()
elif menu == 'Purchases':
    get_purchases_interface()
# elif menu == 'Relaciones entre variables':
#     set_relations()
# elif menu == 'Matrices de correlación':
#     set_arrays()
# data 
