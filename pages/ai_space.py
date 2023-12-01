import plotly.express as px
import os
import fastf1
import streamlit as st
from streamlit_extras.grid import grid
from functions import (
    option_menu,
    page_buttons,
    image_border_radius)

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
image_border_radius("./assets/formula_one_logo.jpg", 20, 270, 150, grid_title)