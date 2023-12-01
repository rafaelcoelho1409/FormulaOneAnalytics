import streamlit as st
import pandas as pd
import base64
import fastf1
from fastf1.ergast import Ergast
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages, Page, Section, add_indentation


@st.cache_data
def read_data(filename):
    return pd.read_csv(filename).drop("Unnamed: 0", axis = 1)

def option_menu():
    show_pages([
        Page("app.py", "Home"),
        Page("pages/overview.py", "Overview"),
        Page("pages/insights.py", "Insights"),
        Page("pages/seasons.py", "Seasons"),
        Page("pages/ai_space.py", "AI Space"),
        Page("pages/about.py", "About")
    ])
    add_indentation()

def image_border_radius(image_path, border_radius, width, height, page_object = None, is_html = False):
    if is_html == False:
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        # Create HTML string with the image
        img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="border-radius: {border_radius}px; width: {width}px; height: {height}px">'
        # Display the HTML string in Streamlit
        if page_object == None:
            st.markdown(img_html, unsafe_allow_html=True)
        else:
            page_object.markdown(img_html, unsafe_allow_html=True)
    else:
        # Create HTML string with the image
        img_html = f'<img src="{image_path}" style="border-radius: {border_radius}px; width: 300px;">'
        # Display the HTML string in Streamlit
        if page_object == None:
            st.markdown(img_html, unsafe_allow_html=True)
        else:
            page_object.markdown(img_html, unsafe_allow_html=True)

@st.cache_resource
def load_f1_session(season, race, event):
    try:
        session = fastf1.get_session(season, race, event)
        session.load()
        return session
    except ValueError:
        st.error(f"This Grand Prix does not have the event {event}. Choose another session type")
        st.stop()

@st.cache_resource
def ergast_get_race_schedule(_ergast, season_ftr):
    return _ergast.get_race_schedule(season_ftr)

@st.cache_resource
def ergast_get_race_results(_ergast, season, round):
    return _ergast.get_race_results(season, round)

@st.cache_resource
def ergast_get_sprint_results(_ergast, season, round):
    return _ergast.get_sprint_results(season, round)

@st.cache_resource
def season_results(_ergast, season_ftr):
    try:
        races = ergast_get_race_schedule(_ergast, season_ftr)
        results = []
        # For each race in the season
        for rnd, race in races['raceName'].items():
            # Get results. Note that we use the round no. + 1, because the round no.
            # starts from one (1) instead of zero (0)
            temp = ergast_get_race_results(_ergast, season = season_ftr, round = rnd + 1)
            temp = temp.content[0]
            # If there is a sprint, get the results as well
            sprint = ergast_get_sprint_results(_ergast, season = season_ftr, round = rnd + 1)
            if sprint.content and sprint.description['round'][0] == rnd + 1:
                temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
                # Add sprint points and race points to get the total
                temp['points'] = temp['points_x'] + temp['points_y']
                temp.drop(columns=['points_x', 'points_y'], inplace=True)
            # Add round no. and grand prix name
            temp['round'] = rnd + 1
            temp['race'] = race.removesuffix(' Grand Prix')
            temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
            results.append(temp)
        # Append all races into a single dataframe
        results = pd.concat(results)
        races = results['race'].drop_duplicates()
        results = results.pivot(index='driverCode', columns='round', values='points')
        # Rank the drivers by their total points
        results['total_points'] = results.sum(axis=1)
        results = results.sort_values(by='total_points', ascending=False)
        results.drop(columns='total_points', inplace=True)
        # Use race name, instead of round no., as column names
        results.columns = races
        fig = px.imshow(
            results,
            text_auto=True,
            aspect='auto',  # Automatically adjust the aspect ratio
            color_continuous_scale=[[0,    'rgb(198, 219, 239)'],  # Blue scale
                                    [0.25, 'rgb(107, 174, 214)'],
                                    [0.5,  'rgb(33,  113, 181)'],
                                    [0.75, 'rgb(8,   81,  156)'],
                                    [1,    'rgb(8,   48,  107)']],
            labels={'x': 'Race',
                    'y': 'Driver',
                    'color': 'Points'}       # Change hover texts
        )
        fig.update_xaxes(title_text='')      # Remove axis titles
        fig.update_yaxes(title_text='')
        fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                         showline=False,
                         tickson='boundaries')              # Show horizontal grid only
        fig.update_xaxes(showgrid=False, showline=False)    # And remove vertical grid
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')     # White background
        fig.update_layout(coloraxis_showscale=False)        # Remove legend
        fig.update_layout(xaxis=dict(side='top'))           # x-axis on top
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
        st.plotly_chart(fig)
    except fastf1.req.RateLimitExceededError:
        st.warning("Error - ergast.com: 200 calls/h. Try in another moment.")

def page_buttons():
    st.write(" ")
    cols_ = st.columns(6)
    with cols_[0]:
        HOME = st.button(
            label = "$$\\textbf{Home}$$",
            use_container_width = True)
    with cols_[1]:
        OVERVIEW = st.button(
            label = "$$\\textbf{Overview}$$",
            use_container_width = True)
    with cols_[2]:
        INSIGHTS = st.button(
            label = "$$\\textbf{Insights}$$",
            use_container_width = True)
    with cols_[3]:
        SEASONS = st.button(
            label = "$$\\textbf{Seasons}$$",
            use_container_width = True)
    with cols_[4]:
        AI_SPACE = st.button(
            label = "$$\\textbf{AI Space}$$",
            use_container_width = True)
    with cols_[5]:
        ABOUT_US = st.button(
            label = "$$\\textbf{About Us}$$",
            use_container_width = True)
    if HOME:
        switch_page("home")
    if OVERVIEW:
        switch_page("overview")
    if INSIGHTS:
        switch_page("insights")
    if SEASONS:
        switch_page("seasons")
    if AI_SPACE:
        switch_page("ai space")
    if ABOUT_US:
        switch_page("about")
