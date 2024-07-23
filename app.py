import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.grid import grid
from functions import (
    option_menu, 
    image_border_radius,
    create_scrollable_section,
    image_carousel)

st.set_page_config(
    page_title = "Formula 1 Analytics",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

layout = grid([1, 0.2, 2], vertical_align = True)
first_column = layout.container()
layout.container()
second_column = layout.container()
#image_border_radius("assets/f1_home.jpg", 20, 100, 100, first_column)
cars_image_link = [
    "https://c4.wallpaperflare.com/wallpaper/247/332/980/car-formula-1-ferrari-f1-wallpaper-preview.jpg",
    "https://c4.wallpaperflare.com/wallpaper/410/494/431/racing-f1-car-formula-1-race-car-hd-wallpaper-preview.jpg",
    "https://e1.pxfuel.com/desktop-wallpaper/16/662/desktop-wallpaper-over-50-formula-one-cars-f1-in-for-mo3.jpg",
]
with first_column:
    image_carousel(["assets/f1_home.jpg"], cars_image_link)
first_column.latex("\\Huge{\\textbf{Formula 1 Analytics}}")
first_column.caption("Author: Rafael Silva Coelho")

OVERVIEW = first_column.button(
    label = "$$\\textbf{Overview}$$",
    use_container_width = True)
INSIGHTS = first_column.button(
    label = "$$\\textbf{Insights}$$",
    use_container_width = True)
SEASONS = first_column.button(
    label = "$$\\textbf{Seasons}$$",
    use_container_width = True)
AI_SPACE = first_column.button(
    label = "$$\\textbf{AI Space}$$",
    use_container_width = True)
ABOUT_US = first_column.button(
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

with first_column:
    image_carousel([
        f"assets/f1analytics{x:0>2}.png" for x in range(1, 11)
    ], [])

second_column.latex("\\Huge{\\textbf{Formula 1 Analytics}}")
# Define your content
overview_content = """
<i><h1>OVERVIEW</h1></i>
<div style='font-size:20px'>
Dive into the heart of Formula 1 racing with our comprehensive Overview section. 
Here, you'll find a rich collection of data covering every aspect of the sport's storied history. 
Explore detailed information about the iconic circuits where history was made, 
learn about the constructors who engineered cutting-edge racing machines, 
delve into the profiles of legendary drivers who have become household names, 
and revisit every race that has contributed to the legacy of Formula 1. 
This section is your gateway to understanding the evolution and grandeur of one of the 
most thrilling sports in the world.
</div>"""
insights_content = """
<i><h1>INSIGHTS</h1></i>
<div style='font-size:20px'>
The Insights section is a treasure trove for Formula 1 enthusiasts and statisticians alike. 
Here, we delve deeper into the analytics of the sport, offering specific and detailed data 
about circuits, constructors, drivers, and champions. Whether you're looking for intricate details 
about track performance, constructor strategies, driver skills, or championship journeys, 
this section provides a wealth of data, enabling a deeper understanding and appreciation of the 
finer nuances of Formula 1 racing. It's perfect for those who love to analyze and uncover patterns 
and stories behind the numbers.
</div>"""
seasons_content = """
<i><h1>SEASONS</h1></i>
<div style='font-size:20px'>
Our Seasons section offers a comprehensive look at the individual Formula 1 seasons, 
presenting an in-depth analysis of the finer details that define each racing year. 
From telemetry data that reveals the secrets behind car performance to lap-by-lap analyses 
showcasing driver skills, this section covers it all. Get insights into crucial aspects like 
gear shifts, lap times, and tire strategies, which often make the difference between victory 
and defeat. Whether you're revisiting a classic season or exploring recent races, 
this section brings you closer to the action, one season at a time.
</div>"""
ai_space_content = """
<i><h1>AI SPACE</h1></i>
<div style='font-size:20px'>
Welcome to the AI Space, a visionary section dedicated to the intersection of Formula 1 
and cutting-edge Machine Learning technology. Currently under construction, this space is poised 
to transform how we interact with and understand Formula 1 data. Here, we aim to apply advanced 
ML algorithms to the vast datasets of the sport, uncovering patterns, predictions, and insights 
that were previously unattainable. Whether it's forecasting race outcomes, 
optimizing team strategies, or analyzing driver performances, the AI Space is set to 
revolutionize the way fans, teams, and analysts engage with the world of Formula 1. 
Stay tuned for an exciting journey into the future of sports analytics.
</div>"""
# Combine all content
combined_content = "<hr>".join([
    overview_content, 
    insights_content, 
    seasons_content, 
    ai_space_content])# Create scrollable section
scrollable_section = create_scrollable_section(
    combined_content, 
    height = "850px")
# Display the scrollable section
second_column.markdown(scrollable_section, unsafe_allow_html=True)
st.divider()