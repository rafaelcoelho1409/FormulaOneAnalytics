import plotly.express as px
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
import os
import fastf1
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.grid import grid
from functions import (
    option_menu,
    page_buttons,
    image_border_radius,
    get_scaler_data,
    get_cluster_data,
    get_umap_data
    )
#MACHINE LEARNING
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score
)

px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

st.set_page_config(
    page_title = "Formula 1 Analytics | AI Space",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

grid_title = grid([5, 1], vertical_align = True)
container1 = grid_title.container()
container1.title("$$\\large{\\textbf{Formula 1 Analytics | AI Space}}$$")
container1.caption("Author: Rafael Silva Coelho")

page_buttons()

st.divider()
image_border_radius("./assets/formula_one_logo.jpg", 20, 100, 100, grid_title)

data = pd.read_pickle("./data/data_prep1.pkl")
data_original_columns = data.columns
results = pd.read_pickle("./data/results.pkl")
results_original_columns = results.columns
data_original_columns = data_original_columns[
    data_original_columns.isin(
        results_original_columns)]
data = data.fillna(0)

#tabs = st.tabs([
#    "$$\\textbf{Clustering}$$",
#    "$$\\textbf{LLM}$$",
#])


#with tabs[0]: #CLUSTERING
st.markdown("<i><h1 style='text-align:center'>Clustering</h1></i>", unsafe_allow_html = True)
grid_ftr = grid(2, vertical_align = True)
scaler_grid = grid_ftr.container()
cluster_grid = grid_ftr.container()
dim_reduction_grid = grid_ftr.container()
scaler_ftr = scaler_grid.selectbox(
    label = "Scaler",
    options = [
        "Standard Scaler", #mean 0 and std 1
        "Minimum-Maximum Scaler", #min -1 and max 1
        "Robust Scaler", #For many outliers,
        "Normalizer" #norm 1
    ],
    index = 1
)
cluster_ftr = cluster_grid.selectbox(
    label = "Clustering Model",
    options = [
        "KMeans",
        "Mean Shift",
        "Agglomerative Clustering",
        "Bisecting KMeans",
        "OPTICS"
    ]
)
data_scaled = get_scaler_data(
    scaler_ftr, 
    data)
data_umap_2d, data_umap_3d = get_umap_data(data_scaled)
data_umap_2d_ = pd.DataFrame(data_umap_2d, columns = ["x", "y"])
data_umap_3d_ = pd.DataFrame(data_umap_3d, columns = ["x", "y", "z"])
data["umap_2d_x"] = data_umap_2d_["x"]
data["umap_2d_y"] = data_umap_2d_["y"]
data["umap_3d_x"] = data_umap_3d_["x"]
data["umap_3d_y"] = data_umap_3d_["y"]
data["umap_3d_z"] = data_umap_3d_["z"]
custom_data = [
    "driver_name",
    "driver_nationality",
    "constructor_name",
    "year",
    "name_race",
    "circuit_name",
    "position",
    "fastestLap",
    "fastestLapSpeed",
    "fastestLapTime",
    "clustering_pred_3d"
]
markers = [
    'circle', 
    'circle-open', 
    'cross', 
    'diamond', 
    'diamond-open', 
    'square', 
    'square-open', 
    'x']
hovertemplate = "".join(
    [
        "Cluster: %{customdata[10]}<br>",
        "Driver: %{customdata[0]}<br>",
        "Nationality: %{customdata[1]}<br>",
        "Constructor: %{customdata[2]}<br>",
        "Season: %{customdata[3]}<br>",
        "%{customdata[4]}<br>",
        "Circuit: %{customdata[5]}<br>",
        "Position: %{customdata[6]}<br>",
        "Fastest Lap: %{customdata[7]}<br>",
        "Fastest Lap Speed (km/h): %{customdata[8]}<br>",
        "Fastest Lap Time: %{customdata[9]}<br>"
    ])
if cluster_ftr in ["KMeans", "Bisecting KMeans"]:
    n_clusters = cluster_grid.number_input(
        label = "Number of clusters",
        min_value = 2,
        value = 2,
        step = 1
    )
    cluster_model_2d, cluster_model_3d = get_cluster_data(
        cluster_ftr, 
        data_umap_2d,
        data_umap_3d, 
        n_clusters = n_clusters)
    y_pred_2d = cluster_model_2d.predict(data_umap_2d)
    y_pred_3d = cluster_model_3d.predict(data_umap_3d)
    data["clustering_pred_2d"] = y_pred_2d.astype(int)
    data["clustering_pred_3d"] = y_pred_3d.astype(int)
    data_comp = results.drop(data_original_columns, axis = 1)
    data = pd.concat([data, data_comp], axis = 1)
    data["fastestLapTime"] = data["fastestLapTime"].fillna("No time")
    fig_2d = px.scatter(
        data,
        x = "umap_2d_x",
        y = "umap_2d_y",
        color = "clustering_pred_2d",
        color_continuous_scale = px.colors.sequential.Rainbow,
        title = "Dimensionality Reduction (2D)",
        custom_data = custom_data
    )
    fig_2d.update_traces(
        hovertemplate = hovertemplate
    )
    fig_3d = px.scatter_3d(
        data,
        x = "umap_3d_x",
        y = "umap_3d_y",
        z = "umap_3d_z",
        color = "clustering_pred_3d",
        color_continuous_scale = px.colors.sequential.Rainbow,
        title = "Dimensionality Reduction (3D)",
        custom_data = custom_data
    )
    fig_3d.update_traces(
        hovertemplate = hovertemplate
    )
elif cluster_ftr == "Mean Shift":
    cluster_model_2d, cluster_model_3d = get_cluster_data(
        cluster_ftr, 
        data_umap_2d,
        data_umap_3d)
    y_pred_2d = cluster_model_2d.predict(data_umap_2d)
    y_pred_3d = cluster_model_3d.predict(data_umap_3d)
    data["clustering_pred_2d"] = y_pred_2d.astype(int)
    data["clustering_pred_3d"] = y_pred_3d.astype(int)
    data_comp = results.drop(data_original_columns, axis = 1)
    data = pd.concat([data, data_comp], axis = 1)
    data["fastestLapTime"] = data["fastestLapTime"].fillna("No time")
    cluster_centers_2d = cluster_model_2d.cluster_centers_
    labels_unique_2d = np.unique(y_pred_2d)
    n_clusters_2d = len(labels_unique_2d)
    cluster_centers_3d = cluster_model_3d.cluster_centers_
    labels_unique_3d = np.unique(y_pred_3d)
    n_clusters_3d = len(labels_unique_3d)
    fig_2d = go.Figure()
    fig_3d = go.Figure()
    for k, col in zip(range(n_clusters_2d), px.colors.qualitative.Plotly):
        my_members_2d = y_pred_2d == k
        cluster_center_2d = cluster_centers_2d[k]
        # Plot cluster members
        fig_2d.add_trace(
            go.Scatter(
                x = data["umap_2d_x"][my_members_2d], 
                y = data["umap_2d_y"][my_members_2d],
                customdata = data[custom_data][my_members_2d],
                hovertemplate = hovertemplate,
                mode = 'markers', 
                marker_symbol = markers[k],
                marker_color = col, 
                name = f'Cluster {k}'))
        # Plot cluster centers
        fig_2d.add_trace(
            go.Scatter(
                x = [cluster_center_2d[0]], 
                y = [cluster_center_2d[1]],
                mode = 'markers', 
                marker_symbol = markers[k],
                marker_color = col, 
                marker_size = 14,
                marker_line_color = "black", 
                name = f'Center {k}'))
    # Finalizing the plot
    fig_2d.update_layout(
        title = "Dimensionality Reduction (2D)<br>"
                f"Estimated number of clusters: {n_clusters_2d}",
        xaxis_title = "Feature 1",
        yaxis_title = "Feature 2",
        showlegend = True)
    ########################
    for k, col in zip(range(n_clusters_3d), px.colors.qualitative.Plotly):
        my_members_3d = y_pred_3d == k
        cluster_center_3d = cluster_centers_3d[k]
        # Plot cluster members
        fig_3d.add_trace(
            go.Scatter3d(
                x = data["umap_3d_x"][my_members_3d], 
                y = data["umap_3d_y"][my_members_3d],
                z = data["umap_3d_z"][my_members_3d],
                customdata = data[custom_data][my_members_3d],
                hovertemplate = hovertemplate,
                mode = 'markers', 
                marker_symbol = markers[k],
                marker_color = col, 
                name = f'Cluster {k}'))
        # Plot cluster centers
        fig_3d.add_trace(
            go.Scatter3d(
                x = [cluster_center_3d[0]], 
                y = [cluster_center_3d[1]],
                z = [cluster_center_3d[2]],
                mode = 'markers', 
                marker_symbol = markers[k],
                marker_color = col, 
                marker_size = 14,
                marker_line_color = "black", 
                name = f'Center {k}'))
    # Finalizing the plot
    fig_3d.update_layout(
        title = "Dimensionality Reduction (3D)<br>"
                f"Estimated number of clusters: {n_clusters_3d}",
        xaxis_title = "Feature 1",
        yaxis_title = "Feature 2",
        #zaxis_title = "Feature 3",
        showlegend = True)
elif cluster_ftr == "Agglomerative Clustering":
    agg_clust_cols = cluster_grid.columns(3)
    connectivity_ftr = agg_clust_cols[0].selectbox(
        label = "Connectivity",
        options = [
            "K-Nearest Neighbors Graph",
            None
        ]
    )
    linkage_ftr = agg_clust_cols[1].selectbox(
        label = "Linkage",
        options = [
            "average",
            "complete",
            "ward",
            "single"
        ]
    )
    n_clusters = agg_clust_cols[2].number_input(
        label = "Number of clusters",
        min_value = 2,
        value = 2,
        step = 1
    )
    cluster_model_2d, cluster_model_3d = get_cluster_data(
        cluster_ftr, 
        data_umap_2d,
        data_umap_3d,
        n_clusters = n_clusters,
        connectivity_ftr = connectivity_ftr,
        linkage_ftr = linkage_ftr)
    y_pred_2d = cluster_model_2d.labels_
    y_pred_3d = cluster_model_3d.labels_
    data["clustering_pred_2d"] = y_pred_2d.astype(int)
    data["clustering_pred_3d"] = y_pred_3d.astype(int)
    data_comp = results.drop(data_original_columns, axis = 1)
    data = pd.concat([data, data_comp], axis = 1)
    data["fastestLapTime"] = data["fastestLapTime"].fillna("No time")
    fig_2d = px.scatter(
        data,
        x = "umap_2d_x",
        y = "umap_2d_y",
        color = "clustering_pred_2d",
        color_continuous_scale = px.colors.sequential.Rainbow,
        title = "Dimensionality Reduction (2D)",
        custom_data = custom_data
    )
    fig_2d.update_traces(
        hovertemplate = hovertemplate
    )
    fig_3d = px.scatter_3d(
        data,
        x = "umap_3d_x",
        y = "umap_3d_y",
        z = "umap_3d_z",
        color = "clustering_pred_3d",
        color_continuous_scale = px.colors.sequential.Rainbow,
        title = "Dimensionality Reduction (3D)",
        custom_data = custom_data
    )
    fig_3d.update_traces(
        hovertemplate = hovertemplate
    )
elif cluster_ftr == "OPTICS":
    n_clusters = cluster_grid.number_input(
        label = "Number of clusters",
        min_value = 2,
        value = 2,
        step = 1
    )
    cluster_model_2d, cluster_model_3d = get_cluster_data(
        cluster_ftr,
        data_umap_2d,
        data_umap_3d
    )
    y_pred_2d = cluster_model_2d.labels_
    y_pred_3d = cluster_model_3d.labels_
    data["clustering_pred_2d"] = y_pred_2d.astype(int)
    data["clustering_pred_3d"] = y_pred_3d.astype(int)
    data_comp = results.drop(data_original_columns, axis = 1)
    data = pd.concat([data, data_comp], axis = 1)
    data["fastestLapTime"] = data["fastestLapTime"].fillna("No time")
    fig_2d = go.Figure()
    fig_3d = go.Figure()
    for klass, color in zip(range(n_clusters), px.colors.qualitative.Plotly[:n_clusters]):
        data_k_2d = data[cluster_model_2d.labels_ == klass]
        data_k_3d = data[cluster_model_3d.labels_ == klass]
        fig_2d.add_trace(
            go.Scatter(
                x = data_k_2d["umap_2d_x"], 
                y = data_k_2d["umap_2d_y"],
                customdata = data_k_2d[custom_data],
                hovertemplate = hovertemplate,
                mode = 'markers', 
                marker_color = color, 
                name = f'Cluster {klass}'))
        fig_3d.add_trace(
            go.Scatter3d(
                x = data_k_3d["umap_3d_x"], 
                y = data_k_3d["umap_3d_y"],
                z = data_k_3d["umap_3d_z"],
                customdata = data_k_3d[custom_data],
                hovertemplate = hovertemplate,
                mode = 'markers', 
                marker_color = color, 
                name = f'Cluster {klass}'))
st.divider()
links_dict = {
    "KMeans": "https://scikit-learn.org/stable/modules/clustering.html#k-means",
    "Mean Shift": "https://scikit-learn.org/stable/modules/clustering.html#mean-shift",
    "Agglomerative Clustering": "https://scikit-learn.org/stable/modules/clustering.html#different-linkage-type-ward-complete-average-and-single-linkage",
    "Bisecting KMeans": "https://scikit-learn.org/stable/modules/clustering.html#bisecting-k-means",
    "OPTICS": "https://scikit-learn.org/stable/modules/clustering.html#optics",
    "Uniform Manifold Approximation and Projection (UMAP)": "https://umap-learn.readthedocs.io/en/latest/index.html"
}
st.markdown(
    f"<i><h3 style='text-align:center'>Dimensionality Reduction</h3></i>", 
    unsafe_allow_html = True)
st.markdown(
    f"<a href='{links_dict[cluster_ftr]}'><h4 style='text-align:center'>{cluster_ftr}</h4>", 
    unsafe_allow_html = True)
umap_link = links_dict["Uniform Manifold Approximation and Projection (UMAP)"]
st.markdown(
    f"<a href='{umap_link}'><h4 style='text-align:center'>Uniform Manifold Approximation and Projection (UMAP)</h4>", 
    unsafe_allow_html = True)
fig_cols = st.columns(2)
with fig_cols[0]:
    st.plotly_chart(fig_2d)
with fig_cols[1]:
    st.plotly_chart(fig_3d)
metrics_grid = grid(3, vertical_align = True)
metrics_grid1 = metrics_grid.container()
metrics_grid2 = metrics_grid.container()
metrics_grid3 = metrics_grid.container()
metrics_grid1.metric(
    label = "Silhouette Score (2D)",
    value = f"{silhouette_score(data_umap_2d, y_pred_2d)*100:.2f}%"
)
metrics_grid1.metric(
    label = "Silhouette Score (3D)",
    value = f"{silhouette_score(data_umap_3d, y_pred_3d)*100:.2f}%"
)
metrics_grid2.metric(
    label = "Calinski-Harabasz Index (2D)",
    value = f"{calinski_harabasz_score(data_umap_2d, y_pred_2d):.2f}"
)
metrics_grid2.metric(
    label = "Calinski-Harabasz Index (3D)",
    value = f"{calinski_harabasz_score(data_umap_3d, y_pred_3d):.2f}"
)
metrics_grid3.metric(
    label = "Davies-Bouldin Index (2D)",
    value = f"{davies_bouldin_score(data_umap_2d, y_pred_2d)*100:.2f}%"
)
metrics_grid3.metric(
    label = "Davies-Bouldin Index (3D)",
    value = f"{davies_bouldin_score(data_umap_3d, y_pred_3d)*100:.2f}%"
)
st.markdown("<hr style='border:4px solid white'>", unsafe_allow_html = True)
#############################################################################