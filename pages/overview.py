import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.grid import grid
from streamlit_extras.switch_page_button import switch_page
from functions import (
    option_menu,
    image_border_radius,
    page_buttons)

#px.set_mapbox_access_token(open(".mapbox_token").read())
px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

st.set_page_config(
    page_title = "Formula 1 Analytics | Overview",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

#LOADING DATA
circuits = pd.read_pickle("./data/circuits.pkl")
constructors = pd.read_pickle("./data/constructors.pkl")
drivers = pd.read_pickle("./data/drivers.pkl")
races_circuits = pd.read_pickle("./data/races_circuits.pkl")
results = pd.read_pickle("./data/results.pkl")

grid_title = grid([5, 1], vertical_align = True)
container1 = grid_title.container()
container1.title("$$\\large{\\textbf{Formula 1 Analytics | Overview}}$$")
container1.caption("Author: Rafael Silva Coelho")

page_buttons()

st.divider()
image_border_radius("./assets/formula_one_logo.jpg", 20, 270, 150, grid_title)

tabs = st.tabs([
    "$$\\textbf{Circuits}$$",
    "$$\\textbf{Constructors}$$",
    "$$\\textbf{Drivers}$$",
    "$$\\textbf{Races}$$"
])
with tabs[0]: #CIRCUITS
    #st.write("$$\\underline{\\huge{\\textbf{Circuits}}}$$")
    st.markdown("<i><h1 style='text-align:center'>Circuits</h1></i>", unsafe_allow_html = True)
    #cols1 = st.columns(2)
    #with cols1[0]:
    st.subheader("All circuits used by Formula 1 (1950-2023)")
    fig1 = px.scatter_mapbox(
        circuits,
        lat = "lat",
        lon = "lng",
        color = "country",
        center = {"lat": 53.9438324, "lon": -2.55056405},
        #hover_name = "name",
        zoom = 1.5,
        custom_data = ["name", "location", "country"]
    )
    fig1.update_traces(
        showlegend = False,
        marker = {"size": 10},
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>%{customdata[1]}"
                        )
    st.plotly_chart(
        fig1,
        use_container_width = True)
    #with cols1[1]:
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    df1 = circuits[[
        "country",
        "iso_alpha"
    ]].value_counts().reset_index().rename(
        columns = {0: "count"}
    )
    st.subheader("Amount of F1 circuits by country (1950-2023)")
    fig2 = px.choropleth_mapbox(
        df1, 
        geojson = geojson_url, 
        locations = 'iso_alpha', 
        color = 'count',
        color_continuous_scale = "thermal",
        zoom = 2, 
        center = {"lat": 53.9438324, "lon": -2.55056405},
        custom_data = ["country", "count"]
    )
    fig2.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>Circuits: %{customdata[1]}"
    )
    st.plotly_chart(
        fig2,
        use_container_width = True)
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("Percentage of circuits by country (1950-2023)")
        fig3 = px.pie(
            df1,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(
            fig3,
            use_container_width = True)
    with cols2[1]:
        df2 = circuits[[
            "continent",
            "iso_alpha"
        ]].value_counts().reset_index().rename(
            columns = {0: "count"}
        )
        st.subheader("Percentage of circuits by continent (1950-2023)")
        fig4 = px.pie(
            df2,
            values = "count",
            names = "continent",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(
            fig4,
            use_container_width = True)
    st.divider()
    st.header("About the circuits")
    cols3 = st.columns(6)
    continents = circuits["continent"].unique().tolist()
    for i, x in enumerate(continents):
        with cols3[i]:
            st.subheader(f"**{x}**")
            about_df = circuits[circuits["continent"] == x].sort_values(
                by = "country"
            )[[
                "name",
                "location",
                "country",
                "country_flag",
                "url"
            ]]
            countries = about_df[[
                "country",
                "country_flag"]].drop_duplicates()
            for x in countries.iterrows():
                with st.expander(
                    label = f"{x[1]['country_flag']} **{x[1]['country']}**",
                    expanded = False
                ):
                    links = about_df[about_df["country"] == x[1]["country"]]
                    for x in links.iterrows():
                        st.write(f"[{x[1]['name']}, {x[1]['location']}]({x[1]['url']})")
with tabs[1]: #CONSTRUCTORS
    #st.write("$$\\underline{\\huge{\\textbf{Constructors}}}$$")
    st.markdown("<i><h1 style='text-align:center'>Constructors</h1></i>", unsafe_allow_html = True)
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    df1 = constructors[[
        "country",
        "iso_alpha"
    ]].value_counts().reset_index().rename(
        columns = {0: "count"}
    )
    st.subheader("Amount of constructors by country (1950-2023)")
    fig1 = px.choropleth_mapbox(
        df1, 
        geojson = geojson_url, 
        locations = 'iso_alpha', 
        color = 'count',
        color_continuous_scale = "thermal",
        zoom = 2, 
        center = {"lat": 53.9438324, "lon": -2.55056405},
        custom_data = ["country", "count"]
    )
    fig1.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>Constructors: %{customdata[1]}"
    )
    st.plotly_chart(
        fig1,
        use_container_width = True)
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("Percentage of constructors by country (1950-2023)")
        fig3 = px.pie(
            df1,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig3,
            use_container_width = True)
    with cols2[1]:
        df2 = constructors[[
            "continent",
            "iso_alpha"
        ]].value_counts().reset_index().rename(
            columns = {0: "count"}
        )
        st.subheader("Percentage of constructors by continent (1950-2023)")
        fig4 = px.pie(
            df2,
            values = "count",
            names = "continent",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig4,
            use_container_width = True)
    st.divider()
    st.header("About the constructors")
    cols3 = st.columns(6)
    continents = constructors["continent"].unique().tolist()
    for i, x in enumerate(continents):
        with cols3[i]:
            st.subheader(f"**{x}**")
            about_df = constructors[constructors["continent"] == x].sort_values(
                by = "country"
            )[[
                "name",
                "country",
                "country_flag",
                "url"
            ]]
            countries = about_df[[
                "country",
                "country_flag"]].drop_duplicates()
            for x in countries.iterrows():
                with st.expander(
                    label = f"{x[1]['country_flag']} **{x[1]['country']}**",
                    expanded = False
                ):
                    links = about_df[about_df["country"] == x[1]["country"]]
                    for x in links.iterrows():
                        st.write(f"[{x[1]['name']}]({x[1]['url']})")
with tabs[2]: #DRIVERS
    #st.write("$$\\underline{\\huge{\\textbf{Drivers}}}$$")
    st.markdown("<i><h1 style='text-align:center'>Drivers</h1></i>", unsafe_allow_html = True)
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    df1 = drivers[[
        "country",
        "iso_alpha"
    ]].value_counts().reset_index().rename(
        columns = {0: "count"}
    )
    st.subheader("Amount of drivers by country (1950-2023)")
    fig1 = px.choropleth_mapbox(
        df1, 
        geojson = geojson_url, 
        locations = 'iso_alpha', 
        color = 'count',
        color_continuous_scale = "thermal",
        zoom = 2, 
        center = {"lat": 53.9438324, "lon": -2.55056405},
        custom_data = ["country", "count"]
    )
    fig1.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>Drivers: %{customdata[1]}"
    )
    st.plotly_chart(
        fig1,
        use_container_width = True)
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("Percentage of drivers by country (1950-2023)")
        fig3 = px.pie(
            df1,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig3,
            use_container_width = True)
    with cols2[1]:
        df2 = drivers[[
            "continent",
            "iso_alpha"
        ]].value_counts().reset_index().rename(
            columns = {0: "count"}
        )
        st.subheader("Percentage of drivers by continent (1950-2023)")
        fig4 = px.pie(
            df2,
            values = "count",
            names = "continent",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig4,
            use_container_width = True)
    st.divider()
    st.header("About the drivers")
    filtered_data = drivers.copy()[[
        "country",
        "continent",
        "name",
        "number",
        "code",
        "dob",
        "age",
        "url"
    ]]
    filtered_data.columns = [
        "Country",
        "Continent",
        "Name",
        "Number",
        "Code",
        "Date of birth",
        "Age",
        "URL (about the driver)"
    ]
    grid_ftr = grid(2, vertical_align = True)
    ftr1 = grid_ftr.multiselect(
        label = "Country",
        options = drivers["country"].sort_values().unique()
    )
    ftr2 = grid_ftr.multiselect(
        label = "Continent",
        options = drivers["continent"].sort_values().unique()
    )
    if (ftr1 == [] and ftr2 == []):
        pass
    else:
        filtered_data = filtered_data[
            (filtered_data["Country"].isin(ftr1))
            |
            (filtered_data["Continent"].isin(ftr2))].sort_values(
                by = ["Country", "Continent", "Name"]
            ).reset_index(drop = True)
    filtered_data = filtered_data.to_html(render_links = True)
    scrollable_df = f"""
    <div style="height: 400px;overflow: scroll;">
        {filtered_data}
    </div>
    """
    st.markdown(
        scrollable_df, 
        unsafe_allow_html = True)
with tabs[3]: #RACES
    #st.write("$$\\underline{\\huge{\\textbf{Races}}}$$")
    st.markdown("<i><h1 style='text-align:center'>Races</h1></i>", unsafe_allow_html = True)
    geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    #cols1 = st.columns(2)
    #with cols1[0]:
    df1 = races_circuits[[
        "country",
        "iso_alpha"
    ]].value_counts().reset_index().rename(
        columns = {0: "count"}
    )
    fig1 = px.choropleth_mapbox(
        df1, 
        geojson = geojson_url, 
        locations = 'iso_alpha', 
        color = 'count',
        color_continuous_scale = "thermal",
        zoom = 2, 
        center = {"lat": 53.9438324, "lon": -2.55056405},
        title = "Amount of races by country (1950-2023)",
        custom_data = ["country", "count"]
    )
    fig1.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>Drivers: %{customdata[1]}"
    )
    st.plotly_chart(
        fig1,
        use_container_width = True)
    #with cols1[1]:
    df2 = races_circuits[[
        "name_circuit",
        "location",
        "country",
        "lat",
        "lng",
        "continent"
    ]].groupby([
        "name_circuit",
        "location",
        "country",
        "lat",
        "lng"]).count().reset_index().rename(columns = {"continent": "count"})
    fig2 = px.scatter_mapbox(
        df2,
        lat = "lat",
        lon = "lng",
        color = "country",
        center = {"lat": 53.9438324, "lon": -2.55056405},
        size = "count",
        zoom = 0,
        #opacity = 1,
        title = "Amount of races by circuit (1950-2023)",
        custom_data = ["name_circuit", "location", "count"],
        color_discrete_sequence = px.colors.sequential.Rainbow
    )
    fig2.update_traces(
        showlegend = False,
        #marker = {"size": 10},
        hovertemplate = "<b>%{customdata[0]}</b>"
                        "<br>%{customdata[1]}"
                        "<br><b>Count: %{customdata[2]}</b>"
                        )
    st.plotly_chart(
        fig2,
        use_container_width = True)
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("Percentage of races by country (1950-2023)")
        fig3 = px.pie(
            df1,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig3,
            use_container_width = True)
    with cols2[1]:
        df3 = drivers[[
            "continent",
            "iso_alpha"
        ]].value_counts().reset_index().rename(
            columns = {0: "count"}
        )
        st.subheader("Percentage of races by continent (1950-2023)")
        fig4 = px.pie(
            df3,
            values = "count",
            names = "continent",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig4,
            use_container_width = True)
    cols3 = st.columns(2)
    with cols3[0]:
        st.subheader("Top 10 Races (1950 - 2023)")
        fig5 = px.bar(
            df2.sort_values(by = "count", ascending = False)[:10],
            x = "name_circuit",
            y = "count",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(fig5)
    with cols3[1]:
        df4 = races_circuits[[
            "name_race",
            "iso_alpha"
        ]].value_counts().reset_index().rename(
            columns = {0: "count"}
        )
        st.subheader("Percentage of Grand Prix (1950-2023)")
        fig6 = px.pie(
            df4,
            values = "count",
            names = "name_race",
            color_discrete_sequence = px.colors.sequential.RdBu
        )
        st.plotly_chart(
            fig6,
            use_container_width = True)
    st.divider()
    st.header("About the races")
    filtered_data = races_circuits[[
        "name_race",
        "year",
        "date",
        "name_circuit",
        "location",
        "country",
        "continent",
        "url_race"
    ]].sort_values(by = "date", ascending = False).reset_index(drop = True)
    filtered_data.columns = [
        "Grand Prix",
        "Year",
        "Date",
        "Circuit",
        "Location",
        "Country",
        "Continent",
        "About (Race)"]
    grid_ftr = grid(6, vertical_align = True)
    ftr1 = grid_ftr.multiselect(
        label = "Grand Prix",
        options = races_circuits["name_race"].sort_values().unique()
    )
    ftr2 = grid_ftr.multiselect(
        label = "Year",
        options = races_circuits["year"].sort_values(ascending = False).unique()
    )
    ftr3 = grid_ftr.multiselect(
        label = "Circuit",
        options = races_circuits["name_circuit"].sort_values().unique()
    )
    ftr4 = grid_ftr.multiselect(
        label = "Location",
        options = races_circuits["location"].sort_values().unique()
    )
    ftr5 = grid_ftr.multiselect(
        label = "Country",
        options = races_circuits["country"].sort_values().unique()
    )
    ftr6 = grid_ftr.multiselect(
        label = "Continent",
        options = races_circuits["continent"].sort_values().unique()
    )
    if (ftr1 == [] and ftr2 == [] and ftr3 == [] and ftr4 == [] and ftr5 == [] and ftr6 == []):
        pass
    else:
        filtered_data = filtered_data[
            (filtered_data["Grand Prix"].isin(ftr1))
            |
            (filtered_data["Year"].isin(ftr2))
            |
            (filtered_data["Circuit"].isin(ftr3))
            |
            (filtered_data["Location"].isin(ftr4))
            |
            (filtered_data["Country"].isin(ftr5))
            |
            (filtered_data["Continent"].isin(ftr6))
            ].reset_index(drop = True)
    filtered_data = filtered_data.to_html(render_links = True)
    scrollable_df = f"""
    <div style="height: 400px;overflow: scroll;">
        {filtered_data}
    </div>
    """
    st.markdown(
        scrollable_df,
        unsafe_allow_html = True)