from pyarrow import py_buffer
import streamlit as st
import pandas as pd

st.title("Amazon Delivery Dashboard")
st.write("Explore Amazon delivery data using this interactive dashboard. You can upload your own CSV file or use the default dataset.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Load the default dataset
try:
    default_df = pd.read_csv('amazon_delivery.csv')
except FileNotFoundError:
    st.error("Default dataset 'amazon_delivery.csv' not found. Please ensure it's in the /content directory.")
    default_df = pd.DataFrame() # Initialize an empty DataFrame if default not found

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Successfully loaded uploaded file.")
else:
    df = default_df.copy() # Use a copy of the default DataFrame
    if not df.empty:
        st.success("Using default dataset 'amazon_delivery.csv'.")
    else:
        st.warning("No dataset loaded. Please upload a file or ensure the default dataset is available.")

# Reset index if it's not a default integer index (and if DataFrame is not empty)
if not df.empty and not isinstance(df.index, pd.RangeIndex):
    df = df.reset_index(drop=True)

st.write("### Data Preview")
st.dataframe(df.head())
