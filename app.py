import streamlit as st
import pandas as pd
import requests

# Load Excel data
df = pd.read_excel("Diseases123.xlsx")

st.title("Lamp AI Doctor")

# User basic info
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120)
gender = st.selectbox("Select gender", ["Male", "Female", "Other"])

st.write("---")

# Disease Assistant
st.subheader("Disease Information Assistant")

disease_list = df["Disease"].dropna().unique()
selected_disease = st.selectbox("Select a disease", disease_list)

if selected_disease:
    info = df[df["Disease"] == selected_disease].iloc[0]

    st.write("### Disease Details")
    st.write(f"**Category:** {info['Category']}")
    st.write(f"**Common Symptoms:** {info['Common Symptoms']}")
    st.write(f"**Specialist to Consult:** {info['Specialist to Consult']}")

st.write("---")

# Location + Nearby hospital search
st.subheader("Find Nearest Hospital")

location_query = st.text_input("Enter your city or area name")

if location_query:
    api_key = st.secrets["AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"]

    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location_query}&key={api_key}"
    geocode_response = requests.get(geocode_url).json()

    if geocode_response["status"] == "OK":
        lat = geocode_response["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_response["results"][0]["geometry"]["location"]["lng"]

        places_url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}&radius=3000&type=hospital&key={api_key}"
        )

        places_response = requests.get(places_url).json()

        st.write("### Nearby Hospitals")

        if "results" in places_response and len(places_response["results"]) > 0:
            for place in places_response["results"][:5]:
                st.write(f"**Name:** {place['name']}")
                st.write(f"Address: {place.get('vicinity','N/A')}")
                st.write("---")
        else:
            st.write("No hospitals found near this area.")
    else:
        st.write("Invalid location. Please try again.")
