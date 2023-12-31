import streamlit as st
import pandas as pd
import numpy as np
import base64
import fastf1
from fastf1.ergast import Ergast
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page
from st_pages import show_pages, Page, Section, add_indentation
#MACHINE LEARNING
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    Normalizer
)
from sklearn.cluster import (
    KMeans,
    MeanShift,
    estimate_bandwidth,
    AgglomerativeClustering,
    BisectingKMeans,
    OPTICS
)
from sklearn.neighbors import kneighbors_graph
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP

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
        img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="border-radius: {border_radius}px; width: {width}%; height: {height}%">'
        # Display the HTML string in Streamlit
        if page_object == None:
            st.markdown(img_html, unsafe_allow_html=True)
        else:
            page_object.markdown(img_html, unsafe_allow_html=True)
    else:
        # Create HTML string with the image
        img_html = f'<img src="{image_path}" style="border-radius: {border_radius}px; width: {width}%; height: {height}%">'
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
        switch_page("app")
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

@st.cache_resource
def get_scaler_data(scaler_ftr, data):
    scaler_dict = {
            "Standard Scaler": StandardScaler(), #mean 0 and std 1
            "Minimum-Maximum Scaler": MinMaxScaler(), #min -1 and max 1
            "Robust Scaler": RobustScaler(), #For many outliers,
            "Normalizer": Normalizer()
        }
    scaler = scaler_dict[scaler_ftr].fit(data)
    data_scaled = scaler.transform(data)
    return data_scaled

@st.cache_resource
def get_umap_data(
    data_scaled
):
    umap_2d = UMAP(n_components = 2)
    umap_3d = UMAP(n_components = 3)
    data_umap_2d = umap_2d.fit_transform(data_scaled)
    data_umap_3d = umap_3d.fit_transform(data_scaled)
    return data_umap_2d, data_umap_3d

@st.cache_resource
def get_cluster_data(
    cluster_ftr, 
    data_umap_2d,
    data_umap_3d,
    n_clusters = None,
    connectivity_ftr = None,
    linkage_ftr = None):
    if cluster_ftr == "KMeans":
        cluster_model_2d = KMeans(n_clusters = n_clusters)
        cluster_model_3d = KMeans(n_clusters = n_clusters)
        cluster_model_2d.fit(data_umap_2d)
        cluster_model_3d.fit(data_umap_3d)
    elif cluster_ftr == "Mean Shift":
        bandwidth_2d = estimate_bandwidth(
            data_umap_2d, 
            quantile = 0.2, 
            n_samples = 500)
        cluster_model_2d = MeanShift(
            bandwidth = bandwidth_2d, 
            bin_seeding = True)
        bandwidth_3d = estimate_bandwidth(
            data_umap_3d, 
            quantile = 0.2, 
            n_samples = 500)
        cluster_model_3d = MeanShift(
            bandwidth = bandwidth_3d, 
            bin_seeding = True)
        cluster_model_2d.fit(data_umap_2d)
        cluster_model_3d.fit(data_umap_3d)
    elif cluster_ftr == "Agglomerative Clustering":
        if connectivity_ftr == "K-Nearest Neighbors Graph":
            connectivity_2d = kneighbors_graph(
                data_umap_2d,
                n_clusters,
                include_self = False
            )
            connectivity_3d = kneighbors_graph(
                data_umap_3d,
                n_clusters,
                include_self = False
            )
        else:
            connectivity_2d, connectivity_3d = None, None
        cluster_model_2d = AgglomerativeClustering(
            linkage = linkage_ftr,
            connectivity = connectivity_2d,
            n_clusters = n_clusters
        )
        cluster_model_2d.fit(data_umap_2d)
        cluster_model_3d = AgglomerativeClustering(
            linkage = linkage_ftr,
            connectivity = connectivity_3d,
            n_clusters = n_clusters
        )
        cluster_model_3d.fit(data_umap_3d)
    elif cluster_ftr == "Bisecting KMeans":
        cluster_model_2d = BisectingKMeans(n_clusters = n_clusters)
        cluster_model_3d = BisectingKMeans(n_clusters = n_clusters)
        cluster_model_2d.fit(data_umap_2d)
        cluster_model_3d.fit(data_umap_3d)
    elif cluster_ftr == "OPTICS":
        cluster_model_2d = OPTICS(
            min_samples = 50, 
            xi = 0.05, 
            min_cluster_size = 0.05)
        cluster_model_3d = OPTICS(
            min_samples = 50, 
            xi = 0.05, 
            min_cluster_size = 0.05)
        cluster_model_2d.fit(data_umap_2d)
        cluster_model_3d.fit(data_umap_3d)
    return cluster_model_2d, cluster_model_3d

def create_scrollable_section(content, height="400px"):
    # Defining the HTML and CSS
    scrollable_section_html = f"""
    <div style="
        overflow-y: scroll;
        height: {height};
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px 0;
        ">
        {content}
    </div>
    """
    return scrollable_section_html        

