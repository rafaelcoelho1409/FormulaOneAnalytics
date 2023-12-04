import streamlit as st
import pandas as pd
import numpy as np
import os
import fastf1
import fastf1.plotting
from fastf1.core import Laps
from fastf1.ergast import Ergast
from timple.timedelta import strftimedelta
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
from streamlit_extras.grid import grid
from streamlit_extras.switch_page_button import switch_page
from functions import (
    option_menu,
    image_border_radius,
    load_f1_session,
    season_results,
    page_buttons)

#px.set_mapbox_access_token(open(".mapbox_token").read())
px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))
try:
    os.mkdir("cache_fastf1")
except:
    pass
fastf1.Cache.enable_cache("./cache_fastf1")

st.set_page_config(
    page_title = "Formula 1 Analytics | Seasons",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

races = pd.read_csv("./data/races.csv")
results = pd.read_pickle("./data/results.pkl")
drivers_df = pd.read_pickle("./data/drivers.pkl")

grid_title = grid([5, 1], vertical_align = True)
container1 = grid_title.container()
container1.title("$$\\large{\\textbf{Formula 1 Analytics | Seasons}}$$")
container1.caption("Author: Rafael Silva Coelho")

page_buttons()

st.divider()
image_border_radius("./assets/formula_one_logo.jpg", 20, 270, 150, grid_title)

ergast = Ergast()

col_ftr = st.columns(3)
with col_ftr[0]:
    season_ftr = st.selectbox(
        label = "Season",
        options = [2023, 2022, 2021, 2020, 2019]
    )
    race_option_ftr = races[races["year"] == season_ftr][[
        "name",
        "round"
    ]].sort_values(by = "round")
with col_ftr[1]:
    race_ftr = st.selectbox(
        label = "Race",
        options = race_option_ftr["name"]
    )
with col_ftr[2]:
    session_ftr = st.selectbox(
        label = "Session",
        options = [
            'Practice 1', 
            'Practice 2', 
            'Practice 3', 
            'Sprint', 
            'Sprint Shootout', 
            'Qualifying', 
            'Race'
        ],
        index = 6
    )

session = load_f1_session(
    season_ftr,
    race_option_ftr[race_option_ftr["name"] == race_ftr]["round"].iloc[0],
    session_ftr
)

st.write(f'<i><h1 style="text-align:center;">{session.event["OfficialEventName"]}</h1></i>', unsafe_allow_html = True)

tabs = st.tabs([
    "$$\\textbf{Championship}$$",
    "$$\\textbf{Drivers}$$"
])

with tabs[0]: #CHAMPIONSHIP
    cols1 = st.columns(2)
    with cols1[0]:
        st.subheader("Circuit (track map)")
        lap = session.laps.pick_fastest()
        pos = lap.get_pos_data()
        circuit_info = session.get_circuit_info()
        # Define a helper function for rotating points
        def rotate(xy, *, angle):
            rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                                [-np.sin(angle), np.cos(angle)]])
            return np.matmul(xy, rot_mat)
        # Get the coordinates of the track map and rotate them
        track = pos.loc[:, ('X', 'Y')].to_numpy()
        track_angle = circuit_info.rotation / 180 * np.pi
        rotated_track = rotate(track, angle=track_angle)
        # Create a figure and an ax element
        fig, ax = plt.subplots()
        ax.plot(rotated_track[:, 0], rotated_track[:, 1], 'r')  # Plotting the track map
        # Define an offset vector for corner numbers
        offset_vector = [500, 0]
        # Annotate each corner
        for _, corner in circuit_info.corners.iterrows():
            txt = f"{corner['Number']}{corner['Letter']}"
            offset_angle = corner['Angle'] / 180 * np.pi
            offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
            text_x, text_y = corner['X'] + offset_x, corner['Y'] + offset_y
            text_x, text_y = rotate([text_x, text_y], angle=track_angle)
            track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

            ax.scatter(text_x, text_y, color='grey', s=140)
            ax.plot([track_x, text_x], [track_y, text_y], color='grey')
            ax.text(text_x, text_y, txt, va='center', ha='center', size='small', color='white')
        # Customize the plot
        ax.set_title(f"{session.event['Location']} - {session.event['Country']} ({session.total_laps} laps)")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        st.pyplot(ax.figure)
    with cols1[1]:
        st.subheader("Gear shifts on track")
        lap = session.laps.pick_fastest()
        tel = lap.get_telemetry()
        x = np.array(tel['X'].values)
        y = np.array(tel['Y'].values)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel['nGear'].to_numpy().astype(float)
        fig, ax = plt.subplots()
        cmap = cm.get_cmap('Paired')
        lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
        lc_comp.set_array(gear)
        lc_comp.set_linewidth(4)
        ax.add_collection(lc_comp)
        ax.axis('equal')
        ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
        title = plt.suptitle(
            f"Fastest Lap Gear Shift Visualization\n"
            f"{lap['Driver']} - {session.event['EventName']} {session.event.year} {session_ftr}"
        )
        cbar = plt.colorbar(mappable=lc_comp, label="Gear", boundaries=np.arange(1, 10))
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1, 9))
        st.pyplot(ax.figure)
    for i in range(3):
        st.write("")
    cols2 = st.columns(2)
    with cols2[0]:
        st.subheader("Position changes")
        fig1 = go.Figure()
        for drv in session.drivers:
            drv_laps = session.laps.pick_driver(drv)
            try:
                fig1.add_trace(
                    go.Scatter(
                        x = drv_laps["LapNumber"],
                        y = drv_laps["Position"],
                        mode = "markers+lines",
                        name = drv_laps['Driver'].iloc[0],
                        marker = {"size": 8}
                    )
            )
            except:
                pass
        fig1.update_layout(
            xaxis_title = "Lap Number",
            yaxis_title = "Position",
            yaxis_tickmode = "linear"
        )
        fig1.update_yaxes(autorange = "reversed")
        st.plotly_chart(fig1)
    with cols2[1]:
        st.subheader(f"Driver standings ({season_ftr})")
        season_results(ergast, season_ftr)
    cols3 = st.columns(2)
    with cols3[0]:
        st.subheader("Overlaying speed traces of fastest laps")
        drivers = st.multiselect(
            label = "Drivers",
            options = session.laps["Driver"].unique(),
            default = session.laps["Driver"].unique(),
            key = "drivers_multiselect"
        )
        fig2 = go.Figure()
        for driver in drivers:
            try:
                fastest_lap = session.laps.pick_driver(driver).pick_fastest()
                telemetry = fastest_lap.get_car_data().add_distance()
                fig2.add_trace(
                    go.Scatter(
                        x = telemetry["Distance"],
                        y = telemetry["Speed"],
                        mode = "lines",
                        name = driver
                    )
                )
            except:
                pass
        fig2.update_layout(
            xaxis_title = "Distance in m",
            yaxis_title = "Speed in km/h",
            title = "Fastest Lap Comparison<br>"
                    f"{session.event['EventName']} {session.event.year} {session_ftr}"
        )
        st.plotly_chart(fig2)
    for i in range(3):
        st.write("")
    with cols3[1]:
        st.subheader("Team pace comparison")
        laps = session.laps.pick_quicklaps()
        # Convert lap time from timedelta to seconds
        laps['LapTime (s)'] = laps['LapTime'].dt.total_seconds()
        # Group by team and calculate median lap time
        team_median_laptimes = laps.groupby('Team')['LapTime (s)'].median().reset_index()
        # Sort teams by median lap time
        team_median_laptimes = team_median_laptimes.sort_values('LapTime (s)')
        # Create a color palette for teams
        colors = px.colors.qualitative.Plotly
        team_colors = {team: color for team, color in zip(team_median_laptimes['Team'], colors)}
        # Create a box plot with Plotly
        fig = px.box(
            laps, 
            x = 'Team', 
            y = 'LapTime (s)', 
            category_orders = {'Team': team_median_laptimes['Team'].tolist()},
            color = 'Team',
            color_discrete_map = team_colors
        )
        fig.update_layout(
            title = f"{session.event['EventName']} {session.event.year} {session_ftr} - Team Pace Comparison",
            xaxis_title = '',
            yaxis_title = 'Lap Time (Seconds)',
            showlegend = False
        )
        st.plotly_chart(fig)
    for i in range(3):
        st.write("")
    cols4 = st.columns(2)
    with cols4[0]:
        st.subheader("Tyre strategies")
        laps = session.laps
        # Get driver abbreviations
        drivers = [session.get_driver(driver)["Abbreviation"] for driver in session.drivers]
        # Group and count laps for stint data
        stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
        stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
        stints = stints.rename(columns={"LapNumber": "StintLength"})
        fig = go.Figure()
        for driver in drivers:
            driver_stints = stints[stints["Driver"] == driver]
            previous_stint_end = 0
            for _, row in driver_stints.iterrows():
                fig.add_trace(
                    go.Bar(
                        y = [driver],
                        x = [row["StintLength"]],
                        name = row["Compound"],
                        orientation = 'h',
                        marker_color = fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                        base = previous_stint_end
                    )
                )
                previous_stint_end += row["StintLength"]
        fig.update_layout(
            barmode = 'stack',
            title = f"{session.event['EventName']} {session.event.year} {session_ftr} - Tyre Strategies",
            xaxis_title = "Lap Number",
            yaxis = {'categoryorder':'total ascending'},  # Sort drivers
            legend_title = "Tyre Compound",
            yaxis_tickmode = "linear"
        )
        st.plotly_chart(fig)
    with cols4[1]:
        st.subheader("Speed traces with corners (fastest lap)")
        # Select the fastest lap and get car telemetry data for this lap
        fastest_lap = session.laps.pick_fastest()
        car_data = fastest_lap.get_car_data().add_distance()
        # Load circuit info
        circuit_info = session.get_circuit_info()
        # Create a plotly figure
        fig = go.Figure()
        # Add speed trace
        team_color = fastf1.plotting.team_color(fastest_lap['Team'])
        fig.add_trace(
            go.Scatter(
                x = car_data['Distance'], 
                y = car_data['Speed'],
                mode = 'lines', 
                name = fastest_lap['Driver'],
                line = dict(color = team_color)
                ))
        # Get min and max speed for setting y-axis limits
        v_min = car_data['Speed'].min()
        v_max = car_data['Speed'].max()
        # Add annotations for each corner
        for _, corner in circuit_info.corners.iterrows():
            fig.add_shape(
                type = "line",
                x0 = corner['Distance'], 
                y0 = v_min - 20, 
                x1 = corner['Distance'], 
                y1 = v_max + 20,
                line = dict(
                    color = "grey", 
                    width = 1, 
                    dash = "dot"))
            fig.add_annotation(
                x = corner['Distance'], 
                y = v_min-30,
                text = f"{corner['Number']}{corner['Letter']}",
                showarrow = False, 
                yshift = 10)
        # Update layout
        fig.update_layout(
            title = "Speed Trace with Corner Annotations",
            xaxis_title = "Distance in m",
            yaxis_title = "Speed in km/h",
            yaxis_range = [v_min - 40, v_max + 20],
            showlegend = True
        )
        st.plotly_chart(fig)
    for i in range(3):
        st.write("")
    cols5 = st.columns(2)
    with cols5[0]:
        st.subheader("Qualifying results overview")
        # Get an array of all drivers and their fastest laps
        drivers = pd.unique(session.laps['Driver'])
        list_fastest_laps = [session.laps.pick_driver(drv).pick_fastest() for drv in drivers]
        fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        # Calculate time delta from the fastest lap
        pole_lap = fastest_laps.pick_fastest()
        fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
        # Create Plotly figure
        fig = go.Figure()
        # Add horizontal bars to the figure
        for i, lap in fastest_laps.iterrows():
            try:
                fig.add_trace(
                    go.Bar(
                        y = [lap['Driver']],
                        x = [lap['LapTimeDelta'].total_seconds()],
                        orientation = 'h',
                        #marker_color = team_colors[i],
                        name = lap['Driver']
                ))
            except:
                pass
        # Update layout
        lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
        fig.update_layout(
            title = f"{session.event['EventName']} {session.event.year} Qualifying<br>Fastest Lap: {lap_time_string} ({pole_lap['Driver']})",
            xaxis_title = "Lap Time Delta (seconds)",
            yaxis = dict(categoryorder='total ascending'),  # Sort drivers
            yaxis_tickmode = "linear",
            showlegend = False
        )
        fig.update_yaxes(autorange = "reversed")
        st.plotly_chart(fig)
    with cols5[1]:
        st.subheader("Driver laptimes distribution")
        # Get all the laps for the point finishers only and filter out slow laps
        point_finishers = session.drivers[:10]
        driver_laps = session.laps.pick_drivers(point_finishers).pick_quicklaps().reset_index()
        # Convert the lap times to seconds
        driver_laps["LapTime(s)"] = driver_laps["LapTime"].dt.total_seconds()
        # Get finishing order and modify the color palette
        finishing_order = [session.get_driver(i)["Abbreviation"] for i in point_finishers]
        # Create the violin plot
        fig = go.Figure()
        # Add traces for each driver
        for driver in finishing_order:
            fig.add_trace(
                go.Violin(
                    x = driver_laps[driver_laps['Driver'] == driver]['Driver'],
                    y = driver_laps[driver_laps['Driver'] == driver]['LapTime(s)'],
                    name = driver,
                ))
        # Map compounds to colors
        compound_colors = {'SOFT': 'red', 'MEDIUM': 'yellow', 'HARD': 'blue'}  # Example mapping
        driver_laps['CompoundColor'] = driver_laps['Compound'].map(compound_colors)
        # Add swarmplot (scatter plot)
        fig.add_trace(
            go.Scatter(
                x = driver_laps['Driver'],
                y = driver_laps['LapTime(s)'],
                mode = 'markers',
                marker = dict(
                    color = driver_laps['CompoundColor'], 
                    symbol = 'circle', 
                    size = 5),
            ))
        # Update layout
        fig.update_layout(
            title = f"{session.event['EventName']} {session.event.year} {session_ftr} - Lap Time Distributions",
            xaxis_title = "Driver",
            yaxis_title = "Lap Time (s)",
            yaxis = dict(
                categoryorder = 'array', 
                categoryarray = finishing_order),
            showlegend = False
        )
        st.plotly_chart(fig)
with tabs[1]: #DRIVERS
    race_drivers = results[results["year"] == season_ftr]
    drivers_id = race_drivers["driverId"].unique()
    drivers_options = drivers_df[drivers_df["driverId"].isin(drivers_id)]
    driver_name = st.selectbox(
        label = "Driver",
        options = drivers_options["name"],
        key = "driver_selectbox"
    )
    driver_code = drivers_options[drivers_options["name"] == driver_name]["code"].iloc[0]
    driver_image_url_surname = drivers_options[drivers_options["name"] == driver_name]["surname"].str.lower().str.replace(" ", "").iloc[0]
    driver_image_url = f"https://media.formula1.com/content/dam/fom-website/drivers/{season_ftr}Drivers/{driver_image_url_surname}.jpg"
    driver_constructor = session.results[
        session.results["Abbreviation"] == driver_code]["TeamName"].iloc[0]
    st.divider()
    driver_grid = grid([1, 8], vertical_align = True)
    container1 = driver_grid.container()
    try:
        container1.image(driver_image_url, width = 100)
    except:
        container1.write(" ")
    container2 = driver_grid.container()
    container2.write('')
    container2.header(f"*{driver_name} ({driver_code}) - {driver_constructor}*")
    st.divider()
    cols1 = st.columns(2)
    with cols1[0]:
        st.subheader("Driver laptimes / Tyre strategies")
        driver_laps = session.laps.pick_driver(driver_code).pick_quicklaps().reset_index()
        driver_laps["CompoundColor"] = driver_laps["Compound"].map(fastf1.plotting.COMPOUND_COLORS)
        def format_timedelta(td):
            minutes = td.seconds // 60
            seconds = td.seconds % 60
            milliseconds = td.microseconds // 1000
            return f"{minutes:02}:{seconds:02}.{milliseconds:03}"
        driver_laps["LapTimeDatetime"] = driver_laps["LapTime"].apply(format_timedelta).apply(str)
        fig3 = go.Figure()
        for key, value in fastf1.plotting.COMPOUND_COLORS.items():
            driver_laps_ = driver_laps[driver_laps["Compound"] == key]
            fig3.add_trace(
                go.Scatter(
                    x = driver_laps_["LapNumber"],
                    y = driver_laps_["LapTime"],
                    mode = "markers",
                    marker = {"size": 10},
                    marker_color = driver_laps_["CompoundColor"],
                    name = key
                )
            )
        fig3.update_layout(
            xaxis_title = "Lap Number",
            yaxis_title = "Lap Time",
            title = f"{driver_name} laptimes - {session.event['EventName']} {session.event.year} {session_ftr}",
        )
        fig3.update_yaxes(
            tickvals = driver_laps["LapTime"], ticktext = driver_laps["LapTimeDatetime"]
        )
        st.plotly_chart(fig3)
    with cols1[1]:
        st.subheader("Speed visualization on track map (fastest lap)")
        colormap = cm.plasma
        lap = session.laps.pick_driver(driver_code).pick_fastest()
        # Get telemetry data
        x = lap.telemetry['X']              # values for x-axis
        y = lap.telemetry['Y']              # values for y-axis
        color = lap.telemetry['Speed']      # value to base color gradient on
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # We create a plot with title and adjust some setting to make it look good.
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(f'{session.event["EventName"]} {session.event.year} {session_ftr} - {driver_code} - Speed', size=24, y=0.97)
        # Adjust margins and turn of axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')
        # After this, we plot the data itself.
        # Create background track line
        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)
        # Set the values used for colormapping
        lc.set_array(color)
        # Merge all line segments together
        line = ax.add_collection(lc)
        # Finally, we create a color bar as a legend.
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
        st.pyplot(ax.figure)