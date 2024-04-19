import requests
import streamlit as st

API_HOST = st.secrets["api_host"]


def format_option(option):
    if isinstance(option, dict) and "name" in option:
        return option["name"]
    else:
        return str(option)


st.title("API for the model")

available_articles = requests.get(f"http://{API_HOST}/articles/all").json()

article_names = [article["name"] for article in available_articles]

desired_article = st.selectbox(
    "Desired article", available_articles, index=None, format_func=format_option
)

if not desired_article:
    st.error("Please select an article")
    st.stop()

article_id = f"{desired_article['doc_id']}_{desired_article['name']}"
article = requests.get(f"http://{API_HOST}/articles/{article_id}").json()

# Use the format_func parameter to display only the names
desired_material = st.selectbox(
    "Desired material", article["materials"], format_func=format_option
)
desired_material_cost = desired_material["price"]

desired_finishing = st.selectbox(
    "Desired finishing", article["finishings"], format_func=format_option
)
desired_finishing_cost = desired_finishing["price"]

col1, col2, col3 = st.columns(3)

with col1:
    unique_lengths = sorted(set([dim["length"] for dim in article["dimensions"]]))
    selected_length = st.selectbox("Select Length", unique_lengths)

with col2:
    width_options = [
        dim["width"]
        for dim in article["dimensions"]
        if dim["length"] == selected_length
    ]
    selected_width = st.selectbox("Select Width", width_options)

with col3:
    thickness_options = [
        dim["thickness"]
        for dim in article["dimensions"]
        if dim["length"] == selected_length
    ]
    selected_thickness = st.selectbox("Select Thickness", thickness_options)

final_dimensions = {
    "length": selected_length,
    "width": selected_width,
    "thickness": selected_thickness,
}


st.write(f"Material cost: {desired_material_cost}")
st.write(f"Finishing cost: {desired_finishing_cost}")
st.write(f"Dimensions cost: {final_dimensions['thickness']}")

total_cost = (
    desired_material_cost + final_dimensions["thickness"] + desired_finishing_cost
)
st.subheader(f"The total cost is: {total_cost}")
