"""
Project Ideas - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_project_ideas_prompt
from src.pdf.simple_generator import generate_pdf

st.set_page_config(page_title="Project Ideas", layout="centered", initial_sidebar_state="collapsed")

# Remove Streamlit branding
from src.utils.theme import apply_theme

# Apply custom theme
apply_theme()

if st.button("Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("Project Ideas")
st.caption("Get personalized project ideas to build your portfolio and learn new skills")

with st.form("project_ideas_form"):
    st.markdown("### Your Background")
    
    skill_level = st.selectbox(
        "Your Skill Level",
        ["Beginner", "Intermediate", "Advanced", "Expert"]
    )
    
    current_skills = st.text_area(
        "Current Skills",
        placeholder="List programming languages, frameworks, tools you know...",
        height=100
    )
    
    st.markdown("### Project Preferences")
    
    interests = st.text_area(
        "Areas of Interest",
        placeholder="e.g., Machine Learning, Web Development, Mobile Apps, IoT, Game Development...",
        height=80
    )
    
    project_type = st.multiselect(
        "Project Type",
        ["Academic Project", "Portfolio Project", "Open Source Contribution", 
         "Hackathon", "Capstone Project", "Personal Learning", "Startup Idea"],
        default=["Portfolio Project"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        complexity = st.selectbox("Desired Complexity", ["Simple", "Moderate", "Complex", "Any"])
    with col2:
        timeline = st.selectbox("Timeline", ["1-2 weeks", "1 month", "2-3 months", "3+ months"])
    
    skills_to_learn = st.text_input(
        "Skills You Want to Learn (Optional)",
        placeholder="e.g., React, Docker, TensorFlow"
    )
    
    submitted = st.form_submit_button("Generate Project Ideas", use_container_width=True)

if submitted and current_skills and interests:
    prompt = get_project_ideas_prompt(
        skill_level=skill_level,
        current_skills=current_skills,
        interests=interests,
        project_type=", ".join(project_type),
        complexity=complexity,
        timeline=timeline,
        skills_to_learn=skills_to_learn if skills_to_learn else None
    )
    
    with st.spinner("Generating personalized project ideas..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.6)
            
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
            
            projects = json.loads(json_str)
            st.session_state['project_ideas'] = projects
            st.success("Project ideas generated!")
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")

if 'project_ideas' in st.session_state:
    projects = st.session_state['project_ideas']
    
    st.markdown("---")
    st.markdown("## Your Project Ideas")
    
    if 'project_ideas' in projects:
        for idx, project in enumerate(projects['project_ideas'], 1):
            with st.expander(f"Project {idx}: {project.get('title', '')}", expanded=(idx==1)):
                st.markdown(f"**{project.get('title', '')}**")
                st.caption(f"Complexity: {project.get('complexity', '')} | Duration: {project.get('estimated_duration', '')}")
                
                st.markdown(f"**Description:**")
                st.markdown(project.get('description', ''))
                
                if project.get('learning_outcomes'):
                    st.markdown("**What You'll Learn:**")
                    for outcome in project['learning_outcomes']:
                        st.markdown(f"  - {outcome}")
                
                if project.get('tech_stack'):
                    st.markdown(f"**Tech Stack:** {', '.join(project['tech_stack'])}")
                
                if project.get('key_features'):
                    st.markdown("**Key Features to Implement:**")
                    for feature in project['key_features']:
                        st.markdown(f"  - {feature}")
                
                if project.get('implementation_steps'):
                    st.markdown("**Implementation Steps:**")
                    for step in project['implementation_steps']:
                        st.markdown(f"  {step}")
                
                if project.get('resources'):
                    st.markdown("**Helpful Resources:**")
                    for resource in project['resources']:
                        st.markdown(f"  - {resource}")
                
                if project.get('portfolio_value'):
                    st.success(f"Portfolio Value: {project['portfolio_value']}")
    
    if 'skill_progression_path' in projects:
        with st.expander("Skill Progression Path"):
            st.markdown("*Recommended order to build these projects for maximum learning:*")
            for idx, step in enumerate(projects['skill_progression_path'], 1):
                st.markdown(f"{idx}. **{step.get('project', '')}**")
                st.caption(f"Focus: {step.get('skill_focus', '')}")
    
    if 'open_source_opportunities' in projects:
        with st.expander("Open Source Opportunities"):
            for opp in projects['open_source_opportunities']:
                st.markdown(f"**{opp.get('project', '')}**")
                st.markdown(f"{opp.get('description', '')}")
                st.caption(f"Good for: {opp.get('good_for', '')}")
                st.markdown("")
    
    st.markdown("---")
    pdf_buffer = generate_pdf(projects, f"Project Ideas for {skill_level} Level")
    st.download_button(
        label="Download Project Ideas (PDF)",
        data=pdf_buffer,
        file_name="project_ideas.pdf",
        mime="application/pdf",
        use_container_width=True
    )
