import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Streamlit page configuration
st.set_page_config(layout='wide', page_title='Pizza Sales Dashboard')
st.title('Pizza Sales Dashboard')

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('pizza_sales.csv')
    return df

df = load_data()

# Data Preprocessing and Feature Engineering
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True)

# Extract unique toppings
all_ingredients = df['pizza_ingredients'].str.split(', ').explode()
unique_toppings = sorted(all_ingredients.unique())

# Create additional date features
df['order_month'] = df['order_date'].dt.month
df['order_day_of_week'] = df['order_date'].dt.day_name()

st.write("### Data Loaded and Preprocessed Successfully")

# Sidebar for Filters
st.sidebar.header('Filter Options')

# Filter 1: Pizza Size
pizza_sizes = df['pizza_size'].unique().tolist()
selected_sizes = st.sidebar.multiselect(
    'Select Pizza Size(s)',
    options=pizza_sizes,
    default=pizza_sizes
)

# Filter 2: Toppings
selected_toppings = st.sidebar.multiselect(
    'Select Topping(s)',
    options=unique_toppings,
    default=[] # Start with no toppings selected by default
)

# Filter 3: Unit Price Range
min_price = float(df['unit_price'].min())
max_price = float(df['unit_price'].max())
price_range = st.sidebar.slider(
    'Select Unit Price Range',
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Apply filters to the DataFrame
df_filtered = df[df['pizza_size'].isin(selected_sizes)]
df_filtered = df_filtered[(df_filtered['unit_price'] >= price_range[0]) & (df_filtered['unit_price'] <= price_range[1])]

if selected_toppings:
    # Filter for rows where any of the selected toppings are present in pizza_ingredients
    toppings_filter = df_filtered['pizza_ingredients'].apply(lambda x: any(topping in x for topping in selected_toppings))
    df_filtered = df_filtered[toppings_filter]

# --- Data Overview Section ---
st.subheader('Data Overview')
st.write(f"Showing {len(df_filtered)} rows after filtering.")

# Create a copy for display and convert 'order_date' to string to avoid pyarrow error
df_display = df_filtered.copy()
df_display['order_date'] = df_display['order_date'].dt.strftime('%Y-%m-%d %H:%M:%S')

st.dataframe(df_display.head())

st.subheader('Summary Statistics')
st.dataframe(df_filtered.describe())

st.write("Further development for visualizations will go here.")

print("Streamlit application code with interactive filters and data overview generated. Save this as a .py file and run with 'streamlit run app.py'.")
