import streamlit as st
from streamlit_extras.grid import grid
from streamlit_card import card
from streamlit_extras.switch_page_button import switch_page
from functions import option_menu, image_border_radius

st.set_page_config(
    page_title = "COELHO Finance - About Us",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

option_menu()

st.title("$$\\large{\\textbf{About Us}}$$")

cols_ = st.columns(5)
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

with st.expander(
    label = "Author",
    expanded = True
):
    st.write("$$\\underline{\\Large{\\textbf{Author}}}$$")
    grid1 = grid([1, 0.1, 4], vertical_align = True)
    image_border_radius("assets/rafael_coelho_1.jpeg", 20, 80, 80, grid1)
    grid1.container()
    container1 = grid1.container()
    container1.markdown("""<div style='font-size:25px'>
    Rafael Coelho is a Brazilian Mathematics student 
    who is passionated for Data Science and Artificial Intelligence
    and works in both areas for over three years, with solid knowledge in
    technologic areas such as Machine Learning, Deep Learning, Data Science,
    Computer Vision, Reinforcement Learning, NLP and others.<br><br>
    Recently, he worked in one of the Big Four companies for over a year.</div>
    """, unsafe_allow_html = True)
    #test = container1.columns(3)
    #with test[0]:
    buttons = container1.columns(3)
    buttons[0].markdown("""
    <div>
    <h1>
    <a 
        style='text-align:center;'
        href='https://rafaelcoelho.streamlit.app/'>
    Portfolio
    </a>
    </h1>
    </div>""", unsafe_allow_html = True)
    #with test[1]:
    buttons[1].markdown("""
    <div>
    <h1>
    <a 
        style='text-align:center;'
        href='https://www.linkedin.com/in/rafaelcoelho1409/'>
    LinkedIn
    </a>
    </h1>
    </div>""", unsafe_allow_html = True)
    #with test[2]:
    buttons[2].markdown("""
    <div>
    <h1>
    <a
        style='text-align:center;'
        href='https://github.com/rafaelcoelho1409/'>
    GitHub
    </a>
    </h1>
    </div>""", unsafe_allow_html = True)
####################################


