import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.grid import grid
from streamlit_extras.switch_page_button import switch_page
from streamlit_timeline import timeline
from functions import (
    option_menu,
    image_border_radius,
    page_buttons)

results = pd.read_pickle("./data/results.pkl")
constructors_df = pd.read_pickle("./data/constructors.pkl")
drivers_df = pd.read_pickle("./data/drivers.pkl")

#px.set_mapbox_access_token(open(".mapbox_token").read())
px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

st.set_page_config(
    page_title = "Formula 1 Analytics | Insights",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

grid_title = grid([5, 1], vertical_align = True)
container1 = grid_title.container()
container1.title("$$\\large{\\textbf{Formula 1 Analytics | Insights}}$$")
container1.caption("Author: Rafael Silva Coelho")

page_buttons()

st.divider()
image_border_radius("./assets/formula_one_logo.jpg", 20, 270, 150, grid_title)

tabs = st.tabs([
    "$$\\textbf{Circuits}$$",
    "$$\\textbf{Constructors}$$",
    "$$\\textbf{Drivers}$$",
    "$$\\textbf{Champions}$$",
])

with tabs[0]: #CIRCUITS
    title_cont = st.container()
    grid_ftr1 = grid(2, vertical_align = True)
    country_filter = grid_ftr1.multiselect(
        label = "Country",
        options = results["country"].sort_values().unique(),
        default = ["Italy"],
        key = "country1"
    )
    circuit_filter = grid_ftr1.selectbox(
        label = "Circuit",
        options = results[results["country"].isin(country_filter)]["circuit_name"].sort_values().unique(),
        #index = 2
    )
    title_cont.markdown("<i><h1 style='text-align:center'>Circuits</h1></i>", unsafe_allow_html = True)
    title_cont.markdown(f"<i><h3 style='text-align:center'>{circuit_filter}</h3></i>", unsafe_allow_html = True)
    circuit_insights = results[
        results["circuit_name"] == circuit_filter]
    icols1 = st.columns(2)
    with icols1[0]:
        st.subheader("Winning constructors in this circuit")
        insight1 = circuit_insights[
            circuit_insights["position"] == 1
        ]["constructor_name"].value_counts().reset_index().rename(
            columns = {"index": "constructor_name", "constructor_name": "count"}
        )
        ifig1 = px.pie(
            insight1,
            names = "constructor_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig1)
    with icols1[1]:
        st.subheader("Nationality of the winning constructors in this circuit")
        insight2 = circuit_insights[
            circuit_insights["position"] == 1
        ]["constructor_nationality"].value_counts().reset_index().rename(
            columns = {"index": "constructor_nationality", "constructor_nationality": "count"}
        )
        ifig2 = px.pie(
            insight2,   
            names = "constructor_nationality",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig2)
    icols2 = st.columns(2)
    with icols2[0]:
        st.subheader("Winning drivers in this circuit")
        insight1 = circuit_insights[
            circuit_insights["position"] == 1
        ]["driver_name"].value_counts().reset_index().rename(
            columns = {"index": "driver_name", "driver_name": "count"}
        )
        ifig1 = px.pie(
            insight1,
            names = "driver_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig1)
    with icols2[1]:
        st.subheader("Nationality of the winning drivers in this circuit")
        insight2 = circuit_insights[
            circuit_insights["position"] == 1
        ]["driver_nationality"].value_counts().reset_index().rename(
            columns = {"index": "driver_nationality", "driver_nationality": "count"}
        )
        ifig2 = px.pie(
            insight2,
            names = "driver_nationality",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig2)
    st.divider()
    st.subheader(f"The fastest laps in this circuit - {circuit_filter}")
    insight3 = circuit_insights[
        circuit_insights["fastestLapTime"].notnull()
        ].sort_values(by = "fastestLapTime")[[
        "year",
        "round",
        "name_race",
        "date",
        "driver_name",
        "constructor_name",
        "position",
        "fastestLap",
        "fastestLapTime",
        "fastestLapSpeed"
    ]].reset_index(drop = True)
    try:
        with st.expander(
            label = "**Fastest lap in this circuit**",
            expanded = True
        ):
            grid_constructor1 = grid(3, vertical_align = True)
            grid_constructor2 = grid(3, vertical_align = True)
            grid_constructor1.metric(
                label = "Driver",
                value = insight3["driver_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Constructor",
                value = insight3["constructor_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Season",
                value = int(insight3["year"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap",
                value = int(insight3["fastestLap"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap Time",
                value = insight3["fastestLapTime"].iloc[0]
            )
            grid_constructor2.metric(
                label = "Fastest Lap Speed (km/h)",
                value = insight3["fastestLapSpeed"].iloc[0]
            )
    except:
        pass
    st.dataframe(insight3, use_container_width = True)
with tabs[1]: #CONSTRUCTORS
    title_cont = st.container()
    grid_ftr1 = grid(2, vertical_align = True)
    country_filter = grid_ftr1.multiselect(
        label = "Nationality",
        options = results["constructor_nationality"].sort_values().unique(),
        default = ["Austrian"],
        key = "country2"
    )
    constructor_filter = grid_ftr1.selectbox(
        label = "Constructor",
        options = results[results["constructor_nationality"].isin(country_filter)]["constructor_name"].sort_values().unique(),
        #index = 50
    )
    title_cont.markdown("<i><h1 style='text-align:center'>Constructors</h1></i>", unsafe_allow_html = True)
    title_cont.markdown(f"<i><h3 style='text-align:center'>{constructor_filter}</h3></i>", unsafe_allow_html = True)
    constructor_insights = results[
        results["constructor_name"] == constructor_filter]
    icols1 = st.columns(2)
    with icols1[0]:
        st.subheader("Circuits most won by this constructor")
        insight1 = constructor_insights[
            constructor_insights["position"] == 1
        ]["circuit_name"].value_counts().reset_index().rename(
            columns = {"index": "circuit_name", "circuit_name": "count"}
        )
        ifig1 = px.pie(
            insight1,
            names = "circuit_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig1)
    with icols1[1]:
        st.subheader("Winning drivers by this constructor")
        insight2 = constructor_insights[
            constructor_insights["position"] == 1
        ]["driver_name"].value_counts().reset_index().rename(
            columns = {"index": "driver_name", "driver_name": "count"}
        )
        ifig2 = px.pie(
            insight2,
            names = "driver_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig2)
    st.divider()
    st.subheader(f"The fastest laps by cars of this constructor - {constructor_filter}")
    insight3 = constructor_insights[
        constructor_insights["fastestLapTime"].notnull()
        ].sort_values(by = "fastestLapTime")[[
        "year",
        "round",
        "name_race",
        "circuit_name",
        "date",
        "driver_name",
        "position",
        "fastestLap",
        "fastestLapTime",
        "fastestLapSpeed"
    ]].reset_index(drop = True)
    try:
        with st.expander(
            label = "**Fastest lap by this constructor**",
            expanded = True
        ):
            grid_constructor1 = grid(3, vertical_align = True)
            grid_constructor2 = grid(3, vertical_align = True)
            grid_constructor1.metric(
                label = "Driver",
                value = insight3["driver_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Circuit",
                value = insight3["circuit_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Season",
                value = int(insight3["year"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap",
                value = int(insight3["fastestLap"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap Time",
                value = insight3["fastestLapTime"].iloc[0]
            )
            grid_constructor2.metric(
                label = "Fastest Lap Speed (km/h)",
                value = insight3["fastestLapSpeed"].iloc[0]
            )
    except:
        pass
    st.dataframe(insight3, use_container_width = True)
with tabs[2]: #DRIVERS
    title_cont = st.container()
    grid_ftr1 = grid(2, vertical_align = True)
    country_filter = grid_ftr1.multiselect(
        label = "Nationality",
        options = results["driver_nationality"].sort_values().unique(),
        default = ["French"],
        key = "country3"
    )
    driver_filter = grid_ftr1.selectbox(
        label = "Driver",
        options = results[results["driver_nationality"].isin(country_filter)]["driver_name"].sort_values().unique(),
        #index = 279
    )
    title_cont.markdown("<i><h1 style='text-align:center'>Drivers</h1></i>", unsafe_allow_html = True)
    title_cont.markdown(f"<i><h3 style='text-align:center'>{driver_filter}</h3></i>", unsafe_allow_html = True)
    driver_insights = results[
        results["driver_name"] == driver_filter]
    icols1 = st.columns(2)
    with icols1[0]:
        st.subheader("Circuits most won by this driver")
        insight1 = driver_insights[
            driver_insights["position"] == 1
        ]["circuit_name"].value_counts().reset_index().rename(
            columns = {"index": "circuit_name", "circuit_name": "count"}
        )
        ifig1 = px.pie(
            insight1,
            names = "circuit_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig1)
    with icols1[1]:
        st.subheader("Grand Prix most won by this driver")
        insight2 = driver_insights[
            driver_insights["position"] == 1
        ]["name_race"].value_counts().reset_index().rename(
            columns = {"index": "name_race", "name_race": "count"}
        )
        ifig2 = px.pie(
            insight2,
            names = "name_race",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig2)
    icols2 = st.columns(2)
    with icols2[0]:
        st.subheader("Constructor winning by this driver")
        insight3 = driver_insights[
            driver_insights["position"] == 1
        ]["constructor_name"].value_counts().reset_index().rename(
            columns = {"index": "constructor_name", "constructor_name": "count"}
        )
        ifig3 = px.pie(
            insight3,
            names = "constructor_name",
            values = "count",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(ifig3)
    st.divider()
    st.subheader(f"The fastest laps by cars of this driver - {driver_filter}")
    insight4 = driver_insights[
        driver_insights["fastestLapTime"].notnull()
        ].sort_values(by = "fastestLapTime")[[
        "year",
        "round",
        "name_race",
        "circuit_name",
        "date",
        "constructor_name",
        "position",
        "fastestLap",
        "fastestLapTime",
        "fastestLapSpeed"
    ]].reset_index(drop = True)
    try:
        with st.expander(
            label = "**Fastest lap by this driver**",
            expanded = True
        ):
            grid_constructor1 = grid(3, vertical_align = True)
            grid_constructor2 = grid(3, vertical_align = True)
            grid_constructor1.metric(
                label = "Circuit",
                value = insight4["circuit_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Constructor",
                value = insight4["constructor_name"].iloc[0]
            )
            grid_constructor1.metric(
                label = "Season",
                value = int(insight4["year"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap",
                value = int(insight4["fastestLap"].iloc[0])
            )
            grid_constructor2.metric(
                label = "Fastest Lap Time",
                value = insight4["fastestLapTime"].iloc[0]
            )
            grid_constructor2.metric(
                label = "Fastest Lap Speed (km/h)",
                value = insight4["fastestLapSpeed"].iloc[0]
            )
    except:
        pass
    st.dataframe(insight4, use_container_width = True)
with tabs[3]: #CHAMPIONS
    champion_data = pd.read_html("https://f1.fandom.com/wiki/List_of_World_Drivers%27_Champions")
    st.markdown("<i><h1 style='text-align:center'>Champion Drivers</h1></i>", unsafe_allow_html = True)
    champion_drivers = champion_data[0]
    champion_drivers["Driver"] = champion_drivers["Driver"].str.replace(
        "Juan Manuel Fangio",
        "Juan Fangio")
    champion_drivers = pd.merge(
        champion_drivers,
        drivers_df,
        left_on = "Driver",
        right_on = "name",
        how = "left"
    )[[
        "Season",
        "Driver",
        "country",
        "country_flag"
    ]]
    champion_drivers["Driver"] = champion_drivers["Driver"].str.replace(
        "Juan Fangio",
        "Juan Manuel Fangio")
    champ_cols2 = st.columns(2)
    with champ_cols2[0]:
        st.subheader("Champion drivers")
        champion_drivers["Driver_flag"] = champion_drivers["Driver"] + " " + champion_drivers["country_flag"]
        aux_df = champion_drivers["Driver_flag"].value_counts().reset_index()
        aux_df.columns = ["Driver_flag", "count"]
        fig1 = go.Figure(
            go.Bar(
                x = aux_df["count"],
                y = aux_df["Driver_flag"],
                marker_color = px.colors.sequential.Viridis,
                text = aux_df["count"],
                textposition = "outside",
                orientation = "h",
            )
        )
        fig1.update_yaxes(autorange = "reversed")
        fig1.update_layout(yaxis_tickmode = "linear", height = 1000)
        st.plotly_chart(fig1)
    with champ_cols2[1]:
        st.subheader("Countries from champion drivers")
        aux_df = champion_drivers["country"].value_counts().reset_index()
        aux_df.columns = ["country", "count"]
        fig2 = px.pie(
            aux_df,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(fig2)
    drivers_image = json.load(open("assets/drivers_image.json"))
    champion_drivers["url"] = champion_drivers["Driver"].map(drivers_image)
    events = []
    for row in champion_drivers.iterrows():
        events.append(
            {
                "start_date": {
                    "year": row[1]["Season"]
                },
                "media": {
                    "url": row[1]["url"]
                },
                "text": {
                    "headline": row[1]["Driver"] + " " + row[1]["country_flag"],
                    "text": f'{row[1]["country"]}'
                }
            })
    data = {"events": events}
    st.subheader("Formula 1 Champions Timeline")
    timeline(data)
    st.divider()
    st.markdown("<i><h1 style='text-align:center'>Champion Constructors</h1></i>", unsafe_allow_html = True)
    champion_constructors = champion_data[3]
    champion_constructors = pd.merge(
        champion_constructors,
        constructors_df,
        left_on = "Constructor",
        right_on = "name",
        how = "left"
    )[[
        "Constructor",
        "country",
        "Total"
    ]]
    champion_constructors.loc[10, "country"] = "Italy"
    constructors_image = json.load(open("assets/constructors_image.json"))
    images_col = st.columns(len(constructors_image.keys()))
    for i in range(len(constructors_image.keys())):
        with images_col[i]:
            st.image(
                list(constructors_image.values())[i],
                caption = list(constructors_image.keys())[i])
    champ_cols1 = st.columns(2)
    with champ_cols1[0]:
        st.subheader("Champion constructors")
        fig1 = go.Figure(
            go.Bar(
                x = champion_constructors["Total"],
                y = champion_constructors["Constructor"],
                text = champion_constructors["Total"],
                textposition = "outside",
                marker_color = px.colors.sequential.Viridis,
                orientation = "h",
            )
        )
        fig1.update_yaxes(autorange = "reversed")
        st.plotly_chart(fig1)
    with champ_cols1[1]:
        st.subheader("Countries from champion constructors")
        aux_df = champion_constructors["country"].value_counts().reset_index()
        aux_df.columns = ["country", "count"]
        fig2 = px.pie(
            aux_df,
            values = "count",
            names = "country",
            color_discrete_sequence = px.colors.sequential.RdBu,
        )
        st.plotly_chart(fig2)