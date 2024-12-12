"""
Name:       Jonathan L'Esperance
CS230:      Section 3
Data:       Boston Airbnb Dataset
URL:

Description: This application explores the Boston Airbnb dataset, providing visualizations
and interactive features to analyze key metrics such as pricing, availability, and geographical trends.
"""

import pandas as pd
import streamlit as st
import pydeck as pdk
import json
import matplotlib.pyplot as plt
import seaborn as sns


# did research on @st.cache_data decided it was useful to use
@st.cache_data
def load_data(filepath, dropna=True):
    try:
        data = pd.read_csv(filepath)
        if dropna:
            data.dropna(subset=["latitude", "longitude"], inplace=True)
        data["price"] = data["price"].replace('[\\$,]', '', regex=True).astype(float)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


# had to search how to do this
@st.cache_data
def load_geojson(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def sidebar_filters(data):
    st.sidebar.header("Filter Listings")
    neighborhoods = st.sidebar.multiselect(
        "Select Neighborhoods", options=data["neighbourhood"].unique(), default=None
    )
    price_range = st.sidebar.slider("Select Price Range", 0, int(data["price"].max()), (50, 300))
    return neighborhoods, price_range


def filter_data(data, neighborhoods, price_range):
    filtered_data = data[
        (data["price"] >= price_range[0]) &
        (data["price"] <= price_range[1])
        ]
    if neighborhoods:
        filtered_data = filtered_data[filtered_data["neighbourhood"].isin(neighborhoods)]
    return filtered_data


def top_largest_values(data, column, n=5):
    return data.nlargest(n, column)


def analyze_with_pivot_table(data):
    st.header("Average Prices")
    pivot_table = pd.pivot_table(
        data,
        values="price",
        index="neighbourhood",
        columns="room_type",
        aggfunc="mean"
    )
    st.dataframe(pivot_table)


def create_visualizations(data):
    st.header("Visualizations")

    st.subheader("Average Price by Neighborhood")
    avg_price = data.groupby("neighbourhood")["price"].mean().sort_values(ascending=False)
    st.bar_chart(avg_price)

    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    scatter = ax.scatter(data["longitude"], data["latitude"], c=data["price"], cmap="viridis", alpha=0.5)
    ax.set_title("Price Distribution Across Locations")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.colorbar(scatter, ax=ax, label="Price")
    st.pyplot(fig)


def room_type_visualization(data):
    st.header("Room Type Distribution")

    room_type_counts = data["room_type"].value_counts()
    total_listings = len(data)
    room_type_percentages = (room_type_counts / total_listings) * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=room_type_counts.values,
        y=room_type_counts.index,
        palette=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],   #searched
        ax=ax
    )

    for i, (count, percentage) in enumerate(zip(room_type_counts, room_type_percentages)):
        ax.text(count + 10, i, f"{count} ({percentage:.1f}%)", va="center")

    ax.set_title("Room Type", fontsize=16, fontweight="bold")
    ax.set_xlabel("Number of Listings", fontsize=12)
    ax.set_ylabel("Room Type", fontsize=12)
    sns.despine(left=True, bottom=True)

    st.markdown("""
        Airbnb hosts can list entire homes/apartments, private rooms, shared rooms, 
        and more recently, hotel rooms. Depending on the room type and activity, 
        a residential Airbnb listing could be more like a hotel, disruptive for neighbors, 
        or even illegal.
    """)

    entire_home_only = st.checkbox("Only entire homes/apartments")
    if entire_home_only:
        filtered_data = data[data["room_type"] == "Entire home/apt"]
        st.write(f"Filtered dataset contains {len(filtered_data)} listings.")
    else:
        st.write(f"Full dataset contains {len(data)} listings.")

    st.pyplot(fig)

def add_price_category(data):
    data["price_category"] = ["Low" if price <= 100 else "Medium" if price <= 300 else "High" for price in
                              data["price"]]
    return data

# used outside resources to figure out some details, used web and chat(ai),
# pretty proud of my map I think its unique and stands out
#I was inspired by the sample that was given worked off that used some outside resources to figure out some details
def enhanced_map(data, geojson_data):
    st.write("Customized Map with Neighborhoods and Airbnb Listings")

    view_state = pdk.ViewState(
        latitude=data["latitude"].mean(),
        longitude=data["longitude"].mean(),
        zoom=12,
        pitch=50
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_radius=50,
        get_color=[
            "255 * (price <= 100)",
            "255 * (100 < price <= 300)",
            "255 * (price > 300)",
            140
        ],
        pickable=True
    )

    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        pickable=True,
        stroked=True,
        filled=False,
        line_width_min_pixels=2,
        get_line_color=[0, 0, 0, 200],
    )

    tool_tip = {
        "html": "<b>{name}</b><br/>Price: ${price}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[geojson_layer, scatter_layer],
        tooltip=tool_tip
    )

    st.pydeck_chart(deck)


def home_page():
    st.title("Welcome to the Boston Airbnb Explorer")
    st.image(
        "https://www.pixelstalk.net/wp-content/uploads/2016/07/FreeBoston-Skyline-Wallpaper-Download.jpg",
        use_container_width=True,
        caption="Explore Boston's vibrant Airbnb ecosystem."
    )
    st.markdown("""
        ## About the App

        This interactive web application allows you to explore Boston's Airbnb listings 
        with visualizations, data insights, and filtering options.

        ### Features
        - **Interactive Visualizations**: View data through customizable charts and graphs.
        - **Filter Listings**: Filter by neighborhood, price range, and more.
        - **Map Integration**: Visualize Airbnb listings on an interactive map.

        ---

        ### How to Navigate
        Use the sidebar to access different sections of the app:
        - **Explore Data**: View and analyze the Airbnb dataset.
        - **Visualizations**: Dive into charts and graphs for insights.
        - **Map**: Locate Airbnb listings on a Boston map.

        ---
        #### Get Started by Selecting an Option from the Sidebar!
    """)


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Explore Data", "Visualizations", "Map"])

    filepath = "listings.csv"
    geojson_path = "neighbourhoods.geojson"
    data = load_data(filepath)
    data = add_price_category(data)

    if page == "Home":
        home_page()
    elif page == "Explore Data":
        st.header("Explore Data")
        if data.empty:
            st.error("Data not loaded correctly.")
        else:
            neighborhoods, price_range = sidebar_filters(data)
            filtered_data = filter_data(data, neighborhoods, price_range)
            st.write(f"Showing {len(filtered_data)} listings.")
            st.dataframe(filtered_data)
            analyze_with_pivot_table(filtered_data)
    elif page == "Visualizations":
        if data.empty:
            st.error("Data not loaded correctly.")
        else:
            neighborhoods, price_range = sidebar_filters(data)
            filtered_data = filter_data(data, neighborhoods, price_range)
            room_type_visualization(filtered_data)
            create_visualizations(filtered_data)
    elif page == "Map":
        geojson_data = load_geojson(geojson_path)
        if data.empty:
            st.error("Data not loaded correctly.")
        else:
            enhanced_map(data, geojson_data)


if __name__ == "__main__":
    main()
