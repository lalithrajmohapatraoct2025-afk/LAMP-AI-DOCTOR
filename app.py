import streamlit as st
import pandas as pd
import requests

# ------------ LOAD DISEASE DATA ------------
disease_data = pd.read_excel("Diseases123.xlsx")
disease_data = disease_data.loc[:, ~disease_data.columns.str.contains('^Unnamed')]

# ------------ GOOGLE MAPS API KEY ------------
GOOGLE_MAPS_API_KEY = "AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"

# ------------ PAGE CONFIG ------------
st.set_page_config(page_title="AI Doctor", page_icon="🩺", layout="centered")

# ------------ HEADER ------------
st.markdown("<h1 style='text-align:center;'>🩺 AI Doctor Assistant</h1>", unsafe_allow_html=True)
st.write("Describe your symptoms or type a disease name to get medical guidance.")
st.subheader("🧑 Patient Information")

user_name = st.text_input("Enter your name:")
user_age = st.number_input("Enter your age:", min_value=1, max_value=120)
user_gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

# ------------ TEXT INPUT ------------
user_query = st.text_input("Enter disease or symptom:")

# ------------ SEARCH FUNCTION ------------
def search_disease(query):
    result = disease_data[disease_data["Disease"].str.contains(query, case=False, na=False)]
    return result

# ------------ GOOGLE HOSPITAL SEARCH ------------
def find_hospitals(location):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url).json()

        if "status" not in geocode_response or geocode_response["status"] != "OK":
            return None, None, []

        lat = geocode_response["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_response["results"][0]["geometry"]["location"]["lng"]

        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
        places_response = requests.get(places_url).json()

        hospitals = []
        if "results" in places_response:
            for place in places_response["results"]:
                hospitals.append(place["name"])

        return lat, lng, hospitals

    except Exception as e:
        return None, None, []



# ------------ MAIN SEARCH RESULT ------------
if user_query:
    st.subheader("📌 Results:")
    result_df = search_disease(user_query)

    if result_df.empty:
        st.warning("No matching disease found!")
    else:
        row = result_df.iloc[0]

        # ✅ PATIENT DETAILS (ADD HERE)
        st.subheader("👤 Patient Details")
        st.write(f"**Name:** {user_name}")
        st.write(f"**Age:** {user_age}")
        st.write(f"**Gender:** {user_gender}")

        st.subheader("✅ Disease Information")
        st.write(f"**Disease:** {row['Disease']}")
        st.write(f"**Category:** {row['Category']}")
        st.write(f"**Common Symptoms:** {row['Common Symptoms']}")
        st.write(f"**Specialist to Consult:** {row['Specialist to Consult']}")

        st.subheader("📍 Find nearby hospitals")
        location = st.text_input("Enter your city or location:")

        if location:
            lat, lng, hospitals = find_hospitals(location)

            if hospitals:
                st.success("✅ Nearby hospitals found")
                for item in hospitals:
                    st.write(f"🏥 {item}")

            else:
                st.error("Could not find hospitals. Try a different location.")


# ------------ FOOTER ------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.write("Made with ❤️ using Streamlit")
