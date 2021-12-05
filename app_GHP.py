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
st.sidebar.header('Menu')
# title
st.title('Abastecimiento general')
# menu
menu = st.sidebar.radio(
    "",
    ("Hoteles", "Materiales", "Proveedores", 'Compras'),
)
# sidebar
st.sidebar.markdown('---')
st.sidebar.write('Jose Gonzalez | Diego Samano | Rafa Velasco | Noviembre 2021')
# menu options
if menu == 'Hoteles':
    get_venues_interface()
# elif menu == 'Materiales':
#     get_materials_interface()
elif menu == 'Proveedores':
     get_vendors_interface()
elif menu == 'Compras':
    get_purchases_interface()
# elif menu == 'Relaciones entre variables':
#     set_relations()
# elif menu == 'Matrices de correlación':
#     set_arrays()
# data 
