"""
Professor Dashboard - All Tools
"""
import streamlit as st

st.set_page_config(
    page_title="Professor Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from src.utils.theme import apply_theme

# Apply custom theme
apply_theme()

# Header
st.markdown('''<div class="dashboard-header">
<h1 class="header-title">Professor Dashboard</h1>
<p class="header-subtitle">Design and optimize academic curricula</p>
</div>''', unsafe_allow_html=True)

if st.button("Back to Home"):
    st.switch_page("app.py")

st.markdown("### Select a Tool")

# Tools grid
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    if st.button("Course Structure Generator", key="course_structure", use_container_width=True, help="Generate comprehensive course structures"):
        st.switch_page("pages/Professor_Course_Structure_Generator.py")

with col2:
    if st.button("Learning Outcome Mapping", key="outcome_mapping", use_container_width=True, help="Map content to learning outcomes"):
        st.switch_page("pages/Professor_Learning_Outcome_Mapping.py")
    
    if st.button("Topic Recommendations", key="topic_rec", use_container_width=True, help="Get AI-powered topic suggestions"):
        st.switch_page("pages/Professor_Topic_Recommendations.py")

with col3:
    if st.button("Industry Alignment Analysis", key="industry_align", use_container_width=True, help="Align with industry demands"):
        st.switch_page("pages/Professor_Industry_Alignment_Analysis.py")
