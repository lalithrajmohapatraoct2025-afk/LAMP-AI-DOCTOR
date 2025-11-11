import streamlit as st
import pandas as pd
import requests

# ------------ LOAD DISEASE DATA ------------
disease_data = pd.read_csv("diseases123.csv")  # Make sure the file name is correct

# ------------ GOOGLE MAPS API KEY ------------
GOOGLE_MAPS_API_KEY = "AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"

# ------------ PAGE CONFIG ------------
st.set_page_config(page_title="AI Doctor", page_icon="🩺", layout="centered")

# ------------ HEADER ------------
st.markdown("<h1 style='text-align:center;'>🩺 AI Doctor Assistant</h1>", unsafe_allow_html=True)
st.write("Describe your symptoms or type a disease name to get medical guidance.")

# ------------ TEXT INPUT ------------
user_query = st.text_input("Enter disease or symptom:")

# ------------ SEARCH FUNCTION ------------
def search_disease(query):
    result = disease_data[disease_data["Disease"].str.contains(query, case=False, na=False)]
    return result

# ------------ GOOGLE HOSPITAL SEARCH ------------
def find_hospitals(location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
    geo = requests.get(url).json()

    if geo["status"] != "OK":
        return None, None

    lat = geo["results"][0]["geometry"]["location"]["lat"]
    lng = geo["results"][0]["geometry"]["location"]["lng"]

    nearby_url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius=3000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    )
    hospital_data = requests.get(nearby_url).json()
    return lat, lng, hospital_data


# ------------ MAIN SEARCH RESULT ------------
if user_query:
    st.subheader("📌 Results:")
    result_df = search_disease(user_query)

    if result_df.empty:
        st.warning("No matching disease found!")
    else:
        st.dataframe(result_df)

        st.subheader("📍 Find nearby hospitals")
        location = st.text_input("Enter your city or location:")

        if location:
            lat, lng, hospitals = find_hospitals(location)

            if hospitals:
                st.success("✅ Nearby hospitals found")
                for item in hospitals["results"]:
                    st.write(f"🏥 **{item['name']}**")
                    st.write(item.get("vicinity", "Address not available"))
                    st.write("---")
            else:
                st.error("Could not find hospitals. Try a different location.")


# ------------ FOOTER ------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.write("Made with ❤️ using Streamlit")
