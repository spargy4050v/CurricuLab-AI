"""
Career Path Planner - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_career_path_planner_prompt
from src.pdf.simple_generator import generate_pdf

st.set_page_config(page_title="Career Path Planner", layout="centered", initial_sidebar_state="collapsed")

# Remove Streamlit branding
from src.utils.theme import apply_theme

# Apply custom theme
apply_theme()

if st.button("Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("Career Path Planner")
st.caption("Get a personalized roadmap from your current position to your career goals")

# Form
with st.form("career_path_form"):
    st.markdown("### Current Status")
    
    current_education = st.selectbox(
        "Current Education Level",
        ["High School", "Undergraduate (Year 1)", "Undergraduate (Year 2)", 
         "Undergraduate (Year 3)", "Undergraduate (Year 4)", "Bachelor's Degree", 
         "Master's Student", "Master's Degree", "Ph.D Student", "Ph.D"]
    )
    
    field_of_study = st.text_input("Field of Study", placeholder="e.g., Computer Science, Mechanical Engineering")
    
    current_skills = st.text_area(
        "Current Skills & Experience",
        placeholder="List your current technical skills, projects, internships, research experience...",
        height=120
    )
    
    st.markdown("### Career Goals")
    
    target_role = st.text_input("Target Job Role", placeholder="e.g., Machine Learning Engineer, Product Manager")
    
    target_industry = st.multiselect(
        "Target Industries",
        ["Technology/IT", "Finance", "Healthcare", "Education", "Manufacturing", 
         "Consulting", "Research", "Government", "Startup", "Other"],
        default=["Technology/IT"]
    )
    
    timeline = st.selectbox(
        "Timeline to Reach Goal",
        ["6 months", "1 year", "2 years", "3 years", "5 years"]
    )
    
    interests = st.text_area(
        "Interests & Preferences",
        placeholder="e.g., Love working with data, prefer remote work, interested in AI/ML...",
        height=80
    )
    
    submitted = st.form_submit_button("Generate Career Path", use_container_width=True)

if submitted and target_role and field_of_study:
    prompt = get_career_path_planner_prompt(
        current_education=current_education,
        field_of_study=field_of_study,
        current_skills=current_skills if current_skills else "None specified",
        target_role=target_role,
        target_industry=", ".join(target_industry),
        timeline=timeline,
        interests=interests if interests else None
    )
    
    with st.spinner("Creating your personalized career roadmap..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.5)
            
            # Parse JSON
            json_str = response.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                parts = json_str.split("```")
                if len(parts) >= 2:
                    json_str = parts[1].strip()
            
            if "{" in json_str and "}" in json_str:
                start = json_str.find("{")
                end = json_str.rfind("}") + 1
                json_str = json_str[start:end]
            
            career_path = json.loads(json_str)
            st.session_state['career_path'] = career_path
            st.success("Career path generated!")
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")

# Display Results
if 'career_path' in st.session_state:
    career_path = st.session_state['career_path']
    
    st.markdown("---")
    st.markdown("## Your Career Roadmap")
    
    # Milestones
    if 'milestones' in career_path:
        with st.expander("Career Milestones", expanded=True):
            for milestone in career_path['milestones']:
                st.markdown(f"### {milestone.get('timeline', '')} - {milestone.get('title', '')}")
                st.markdown(f"**Role:** {milestone.get('role', '')}")
                st.markdown(f"**Skills Required:** {', '.join(milestone.get('skills_required', []))}")
                
                if milestone.get('action_items'):
                    st.markdown("**Action Items:**")
                    for item in milestone['action_items']:
                        st.markdown(f"  - {item}")
                st.markdown("---")
    
    # Skills Development Plan
    if 'skills_development' in career_path:
        with st.expander("Skills Development Plan"):
            for skill_plan in career_path['skills_development']:
                st.markdown(f"**{skill_plan.get('skill', '')}**")
                st.caption(f"Priority: {skill_plan.get('priority', '')} | Time: {skill_plan.get('time_to_acquire', '')}")
                
                if skill_plan.get('learning_resources'):
                    st.markdown("Resources:")
                    for resource in skill_plan['learning_resources']:
                        st.markdown(f"  - {resource}")
                st.markdown("")
    
    # Experience Building
    if 'experience_building' in career_path:
        with st.expander("Experience Building Strategy"):
            for exp in career_path['experience_building']:
                st.markdown(f"**{exp.get('type', '')}:** {exp.get('description', '')}")
                st.caption(f"Timeline: {exp.get('timeline', '')} | Impact: {exp.get('impact', '')}")
                
                if exp.get('how_to_find'):
                    st.markdown(f"*How to find:* {exp['how_to_find']}")
                st.markdown("")
    
    # Networking Recommendations
    if 'networking' in career_path:
        with st.expander("Networking Recommendations"):
            for network in career_path['networking']:
                st.markdown(f"- **{network.get('activity', '')}:** {network.get('description', '')}")
    
    # Alternative Paths
    if 'alternative_paths' in career_path:
        with st.expander("Alternative Career Paths"):
            for alt in career_path['alternative_paths']:
                st.markdown(f"**{alt.get('role', '')}**")
                st.markdown(f"{alt.get('description', '')}")
                st.caption(f"Required pivot: {alt.get('required_pivot', '')}")
                st.markdown("")
    
    # Download
    st.markdown("---")
    pdf_buffer = generate_pdf(career_path, f"Career Path Roadmap: {target_role}")
    st.download_button(
        label="Download Career Path (PDF)",
        data=pdf_buffer,
        file_name=f"{target_role.replace(' ', '_')}_career_path.pdf",
        mime="application/pdf",
        use_container_width=True
    )
