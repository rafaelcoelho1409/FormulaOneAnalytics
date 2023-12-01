import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
from functions import (
    option_menu, 
    image_border_radius)

st.set_page_config(
    page_title = "Formula 1 Analytics",
    layout = "centered",
    initial_sidebar_state = "collapsed"
)
#st.image("assets/f1_home.jpg", use_column_width = True)
image_border_radius("assets/f1_home.jpg", 20, 700, 400)
st.latex("\\Huge{\\textbf{Formula 1 Analytics}}")
cols = st.columns(4)
with cols[1]:
    st.caption("Author: Rafael Silva Coelho")
OVERVIEW = st.button(
    label = "$$\\textbf{Overview}$$",
    use_container_width = True)
INSIGHTS = st.button(
    label = "$$\\textbf{Insights}$$",
    use_container_width = True)
SEASONS = st.button(
    label = "$$\\textbf{Seasons}$$",
    use_container_width = True)
AI_SPACE = st.button(
    label = "$$\\textbf{AI Space}$$",
    use_container_width = True)
ABOUT_US = st.button(
    label = "$$\\textbf{About Us}$$",
    use_container_width = True)
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

option_menu()

