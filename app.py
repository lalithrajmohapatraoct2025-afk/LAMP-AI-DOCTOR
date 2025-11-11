import streamlit as st
import pandas as pd
import requests

# -------------------------------
#   CONFIG
# -------------------------------
GOOGLE_API_KEY = "AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"   # 

# Title and header
st.set_page_config(page_title="Lamp AI Doctor", layout="wide")

doctor_gif = "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif"

col1, col2 = st.columns([2, 1])
with col1:
    st.title("🩺 Lamp AI Doctor")
with col2:
    st.image(doctor_gif)

st.write("Hello! I'm your virtual doctor. Please enter your details below.")

# -------------------------------
#   Patient basic info
# -------------------------------
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=1, max_value=110)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])

st.divider()

# -------------------------------
#   Load disease file
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Diseases123.xlsx")
    return df

df = load_data()

st.subheader("🔍 Disease Information")

# Search + Dropdown combined
disease_list = df['Disease'].astype(str).tolist()
search = st.text_input("Search disease:")
dropdown = st.selectbox("Or choose from list:", disease_list)

selected_disease = search if search.strip() != "" else dropdown

if selected_disease:
    filtered = df[df['Disease'].str.lower() == selected_disease.lower()]
    if not filtered.empty:
        st.write("### 🧬 Disease Details")
        st.write(filtered.iloc[0].to_dict())
    else:
        st.write("Disease not found")

st.divider()

# -------------------------------
#   Nearest Hospital Finder
# -------------------------------
st.subheader("🏥 Find Nearest Hospital")

location = st.text_input("Enter your current location (City / Area / Pin Code):")

if st.button("Find nearest hospitals"):
    if location:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=hospitals+near+{location}&key={GOOGLE_API_KEY}"

        response = requests.get(url)
        data = response.json()

        if "results" in data:
            st.write("### Nearby Hospitals:")
            for place in data["results"][:5]:  # Show top 5
                st.write(f"🏥 **{place['name']}**")
                st.write(place.get("formatted_address", "No address available"))
                st.write("---")
        else:
            st.write("No hospital data found. Try again.")
    else:
        st.warning("Please enter a location first.")



