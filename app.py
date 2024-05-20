import streamlit as st
from predict_page import show_predict_page

try:
    show_predict_page()
except:
    st.write("""###### Invalid Input ######""")
