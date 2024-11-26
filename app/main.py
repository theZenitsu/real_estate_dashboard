import streamlit as st
import pandas as pd
from database import fetch_data
import plotly.express as px

# Streamlit app configuration
st.set_page_config(
    page_title="Real Estate Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Real Estate Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
min_price, max_price = st.sidebar.slider("Price Range", 0, 1000000, (100000, 500000))
selected_city = st.sidebar.selectbox(
    "City", ["All", "Casablanca", "Rabat", "Marrakech", "Tangier"]
)

# Updated SQL query
query = """
SELECT a.title, a.price, a.nb_rooms, a.nb_baths, a.surface_area, v.name AS city
FROM annonce a
JOIN ville v ON a.city_id = v.id
WHERE a.price ~ '^[0-9]+$' AND a.price::NUMERIC BETWEEN %s AND %s
"""
params = (min_price, max_price)

if selected_city != "All":
    query += " AND v.name = %s"
    params += (selected_city,)

# Fetch filtered data
data = fetch_data(query, params)

# Optional: Handle non-numeric prices in Python
data["price"] = pd.to_numeric(data["price"], errors="coerce")
data = data.dropna(subset=["price"])

# Display data and visualizations
st.write(f"Displaying results for price range {min_price} to {max_price}")
st.dataframe(data)

# Query for city analysis
city_query = """
SELECT v.name AS city, COUNT(a.id) AS listing_count
FROM annonce a
JOIN ville v ON a.city_id = v.id
GROUP BY v.name
"""
city_data = fetch_data(city_query)

# Bar chart for listings by city
st.subheader("Listings by City")
st.bar_chart(city_data.set_index("city")["listing_count"])

# Scatter plot for surface area vs. price
st.subheader("Relationship Between Surface Area and Price")
st.write("Explore the relationship between property size and price.")
st.scatter_chart(data, x="surface_area", y="price")




equipment_query = """
SELECT e.name AS equipment, COUNT(ae.id) AS count
FROM equipement e
JOIN annonce_equipement ae ON e.id = ae.equipement_id
GROUP BY e.name
"""
equipment_data = fetch_data(equipment_query)

st.subheader("Equipment Distribution")
st.write("Percentage of listings with specific equipment features.")
st.plotly_chart(px.pie(equipment_data, values="count", names="equipment"))

# Sidebar filters
st.sidebar.header("Filters")
min_price, max_price = st.sidebar.slider(
    "Price Range", 0, 1000000, (100000, 500000), key="price_range_slider"
)
selected_city = st.sidebar.selectbox(
    "City", ["All", "Casablanca", "Rabat", "Marrakech", "Tangier"], key="city_selectbox"
)
nb_rooms = st.sidebar.slider(
    "Number of Rooms", 1, 10, (1, 5), key="rooms_slider"
)
nb_baths = st.sidebar.slider(
    "Number of Bathrooms", 1, 5, (1, 3), key="baths_slider"
)
date_range = st.sidebar.date_input(
    "Date Range", [], key="date_range_input"
)

temporal_query = """
SELECT DATE_TRUNC('month', a.datetime) AS month, COUNT(a.id) AS listing_count
FROM annonce a
GROUP BY DATE_TRUNC('month', a.datetime)
ORDER BY month
"""
temporal_data = fetch_data(temporal_query)

st.subheader("Number of Listings Over Time")
st.line_chart(temporal_data.set_index("month")["listing_count"])

csv = data.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)




