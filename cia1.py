import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
import re

st.set_page_config(
    page_title="Silver Price Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Silver Price Calculator")

df = pd.read_csv('historical_silver_price.csv')

col1, col2 = st.columns(2)

with col1:
    st.header("Price Calculator")
    unit = st.radio("Select Unit", ["Grams", "Kilograms"], horizontal=True)    

    weight = st.number_input(
        "Enter Weight of Silver",
        min_value=0.0,
        step=0.1,
        value=1.0,
        format="%.2f"
    )
    
    price_per_gram = st.number_input(
        "Enter Current Price per Gram (INR)",
        min_value=0.0,
        step=0.01,
        value=1.0,
        format="%.2f"
    )
    
    
    weight_in_grams = weight * 1000 if unit == "Kilograms" else weight
    
    total_cost = weight_in_grams * price_per_gram
    
    st.write("Weight in grams:", weight_in_grams)
    st.write("Price per gram (INR):", price_per_gram)
    st.write("Total Cost(INR):", total_cost)
    
    
    

with col2:
    #COnverting the total cost to other currencies (USD)
    st.header("Currency Converter")
    st.write("Convert Total Cost(INR) to other currencies based on current exchange rates.")
    inr_amount=total_cost
    currency = st.selectbox(
        "Select Currency",
        ["USD", "EUR"]
    )
    exchange_rates = {
        "USD": 0.011,
        "EUR": 0.0091
    }
    converted_amount = inr_amount * exchange_rates[currency]
    st.write(f"Total Cost in {currency}: {converted_amount:,.2f}")
    
             
st.header("Historical Silver Price Chart")
st.header("Filters")    
    
filter_option = st.selectbox(
    "Filter by Silver Price Range:",
    [
        "All Data",
        "≤ 20,000 INR per kg",
        "Between 20,000 - 30,000 INR per kg",
        "≥ 30,000 INR per kg"
    ]
)

filtered_df = df.copy()

if filter_option == "≤ 20,000 INR per kg":
    filtered_df = df[df['Silver_Price_INR_per_kg'] <= 20000]
elif filter_option == "Between 20,000 - 30,000 INR per kg":
    filtered_df = df[(df['Silver_Price_INR_per_kg'] >= 20000) & (df['Silver_Price_INR_per_kg'] <= 30000)]
elif filter_option == "≥ 30,000 INR per kg":
    filtered_df = df[df['Silver_Price_INR_per_kg'] >= 30000]

if len(filtered_df) > 0:
    st.info(f"Filtered Data: {len(filtered_df)} records | Price Range: ₹{filtered_df['Silver_Price_INR_per_kg'].min():,.0f} - ₹{filtered_df['Silver_Price_INR_per_kg'].max():,.0f}")
    filtered_df['Date'] = filtered_df['Year'].astype(str) + "-" + filtered_df['Month']
else:
    st.warning("No data available for the selected filter!")

# Line chart to display the data after applying filters by the user
fig=px.line(
    filtered_df,
    x='Date',
    y='Silver_Price_INR_per_kg',
    title="Historical Silver Price (INR per kg)",
    labels={'Silver_Price_INR_per_kg': 'Price (INR per kg)', 'Date': 'Year-Month'},
    markers=True,
    template='plotly_white'
)    
st.plotly_chart(fig, use_container_width=True)  


st.header("Historical Silver Price Data- Statewise")
df1 = pd.read_csv('state_wise_silver_purchased_kg.csv')
st.subheader("State-wise Silver Purchases in India")
st.dataframe(df1)

# st.header("India State-wise Silver Purchases")

st.subheader("Top 5 States by Silver Purchases (kg)")
top5 = df1.sort_values('Silver_Purchased_kg', ascending=False).head(5)
fig_bar = px.bar(
    top5,
    x='State',
    y='Silver_Purchased_kg',
    text='Silver_Purchased_kg',
    color='Silver_Purchased_kg',
    color_continuous_scale='Viridis',
    labels={'Silver_Purchased_kg': 'Silver Purchased (kg)', 'State': 'State'}
)
fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig_bar.update_layout(yaxis=dict(title='Silver Purchased (kg)'), uniformtext_minsize=8, uniformtext_mode='hide', height=450)
st.plotly_chart(fig_bar, use_container_width=True)

st.header("January Silver Prices (Yearly)")
jan_df = df[df['Month'].astype(str).str.strip().str.lower() == 'jan'].copy()
if len(jan_df) == 0:
    st.info("No January records found in the dataset.")
else:
    jan_df = jan_df.sort_values('Year')
    st.dataframe(jan_df[['Year', 'Silver_Price_INR_per_kg']].reset_index(drop=True))

    fig_jan = px.line(
        jan_df,
        x='Year',
        y='Silver_Price_INR_per_kg',
        markers=True,
        title='Silver Price in January (INR per kg)',
        labels={'Silver_Price_INR_per_kg': 'Price (INR per kg)', 'Year': 'Year'},
        template='plotly_white'
    )
    fig_jan.update_traces(line=dict(color='#1f77b4', width=3))
    fig_jan.update_layout(height=400)
    st.plotly_chart(fig_jan, use_container_width=True)



