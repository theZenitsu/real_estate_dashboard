import streamlit as st
import pandas as pd

st.title("Simple Streamlit App")
st.write("Welcome to your first Streamlit app!")

data = {'Numbers': [1, 2, 3, 4, 5]}
df = pd.DataFrame(data)
st.write("Here's a simple table:")
st.write(df)

option = st.slider("Select a number", 1, 5)
st.write("You selected:", option)
