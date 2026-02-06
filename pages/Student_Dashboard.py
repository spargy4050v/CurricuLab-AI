"""
Student Dashboard - All Tools
"""
import streamlit as st

st.set_page_config(
    page_title="Student Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from src.utils.theme import apply_theme

# Apply custom theme
apply_theme()

# Header
st.markdown('''<div class="dashboard-header">
<h1 class="header-title">Student Dashboard</h1>
<p class="header-subtitle">Your personalized career and learning hub</p>
</div>''', unsafe_allow_html=True)

if st.button("Back to Home"):
    st.switch_page("app.py")

st.markdown("### Select a Tool")

# Tools grid
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    if st.button("Skill Gap Analysis", key="skill_gap", use_container_width=True, help="Identify skill gaps and get recommendations"):
        st.switch_page("pages/Student_Skill_Gap_Analysis.py")

with col2:
    if st.button("Job Opportunities", key="jobs", use_container_width=True, help="Discover relevant job opportunities"):
        st.switch_page("pages/Student_Job_Opportunities.py")
    
    if st.button("Project Ideas", key="projects", use_container_width=True, help="Get industry-relevant project ideas"):
        st.switch_page("pages/Student_Project_Ideas.py")

with col3:
    if st.button("Career Path Planner", key="career", use_container_width=True, help="Map out your career trajectory"):
        st.switch_page("pages/Student_Career_Path_Planner.py")
