"""
Scenario-specific prompts for all 12 use cases
"""

# ==========================
# PROFESSOR SCENARIOS
# ==========================

def get_course_structure_prompt(
    course_name: str,
    level: str,
    duration_weeks: int,
    prerequisites: list = None,
    focus_areas: list = None
) -> str:
    """Generate comprehensive course structure"""
    
    prompt = f"""You are an expert curriculum designer. Create a detailed course structure for:

Course: {course_name}
Level: {level}
Duration: {duration_weeks} weeks
"""
    
    if prerequisites:
        prompt += f"Prerequisites: {', '.join(prerequisites)}\n"
    if focus_areas:
        prompt += f"Focus Areas: {', '.join(focus_areas)}\n"
    
    prompt += """
Generate a comprehensive course structure with:
1. Weekly breakdown with topics and subtopics
2. Learning objectives for each week
3. Assignments and projects
4. Assessment methods
5. Recommended resources

Return as JSON:
{
  "course_name": "string",
  "level": "string",
  "total_weeks": number,
  "weekly_structure": [
    {
      "week": 1,
      "topics": ["topic1", "topic2"],
      "learning_objectives": ["objective1"],
      "activities": ["activity1"],
      "assessments": ["assessment1"]
    }
  ],
  "course_outcomes": ["outcome1"],
  "prerequisites_validated": ["prereq1"],
  "recommended_resources": ["resource1"]
}

Use valid JSON only. Each course should align with industry standards and pedagogical best practices."""
    
    return prompt


def get_learning_outcome_mapping_prompt(
    course_content: str,
    competency_framework: str,
    academic_level: str
) -> str:
    """Map course content to learning outcomes"""
    
    return f"""You are an academic assessment expert. Map the following course content to specific learning outcomes using {competency_framework} framework.

Course Content:
{course_content}

Academic Level: {academic_level}

Generate learning outcome mappings with:
1. Specific, measurable learning outcomes (using Bloom's taxonomy)
2. Alignment with competency framework
3. Assessment methods for each outcome
4. Rubrics and evaluation criteria

Return as JSON:
{{
  "framework": "{competency_framework}",
  "learning_outcomes": [
    {{
      "outcome_id": "LO1",
      "description": "Students will be able to...",
      "cognitive_level": "Apply/Analyze/Create",
      "content_mapping": ["Topic X", "Topic Y"],
      "assessment_methods": ["method1"],
      "evaluation_criteria": ["criteria1"]
    }}
  ],
  "alignment_score": "High/Medium/Low",
  "recommendations": ["recommendation1"]
}}

Use valid JSON. Ensure outcomes are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)."""





def get_industry_alignment_prompt(
    curriculum_area: str,
    target_industry: str,
    job_roles: list = None
) -> str:
    """Analyze industry alignment"""
    
    roles_text = f" for roles: {', '.join(job_roles)}" if job_roles else ""
    
    return f"""You are an industry-academic liaison expert. Analyze how well a {curriculum_area} curriculum aligns with {target_industry} industry needs{roles_text}.

Provide:
1. Current industry skill demands
2. Gaps in curriculum vs industry needs
3. Emerging technologies and trends to include
4. Practical skills and tools students should learn
5. Industry certifications to integrate
6. Real-world project suggestions

Return as JSON:
{{
  "industry_skills_required": [
    {{
      "skill": "string",
      "importance": "Critical/High/Medium",
      "current_coverage": "Yes/Partial/No"
    }}
  ],
  "gaps_identified": ["gap1"],
  "emerging_trends": ["trend1"],
  "recommended_additions": [
    {{
      "topic": "string",
      "rationale": "string",
      "suggested_duration": "hours/weeks"
    }}
  ],
  "industry_tools": ["tool1"],
  "certifications": ["cert1"],
  "project_recommendations": ["project1"]
}}

Use valid JSON. Base recommendations on current 2024-2026 industry standards."""


def get_topic_recommendations_prompt(
    subject_area: str,
    current_topics: list,
    target_audience: str,
    timeframe: str = "next 2 years"
) -> str:
    """Generate topic recommendations"""
    
    return f"""You are a subject matter expert in {subject_area}. Recommend new topics that should be incorporated into the curriculum for {target_audience} relevant for {timeframe}.

Current Topics: {', '.join(current_topics)}

Provide:
1. Emerging topics in the field
2. Topics gaining industry traction
3. Foundational topics that may be missing
4. Advanced topics for differentiation
5. Interdisciplinary topics for broader learning

Return as JSON:
{{
  "recommended_topics": [
    {{
      "topic_name": "string",
      "category": "Emerging/Foundational/Advanced/Interdisciplinary",
      "relevance_score": 1-10,
      "rationale": "string",
      "prerequisites": ["prereq1"],
      "suggested_duration": "hours",
      "industry_demand": "High/Medium/Low",
      "learning_resources": ["resource1"]
    }}
  ],
  "topics_to_update": [
    {{
      "current_topic": "string",
      "suggested_updates": "string"
    }}
  ],
  "topics_to_remove": ["topic1"],
  "implementation_priority": ["topic1", "topic2", "topic3"]
}}

Use valid JSON. Focus on forward-looking, industry-relevant topics."""




# ==========================
# STUDENT SCENARIOS
# ==========================

def get_skill_gap_analysis_prompt(
    resume_text: str,
    target_role: str = None,
    job_description: str = None
) -> str:
    """Analyze skill gaps from resume"""
    
    comparison = f"\nTarget Role: {target_role}" if target_role else ""
    comparison += f"\nJob Description: {job_description}" if job_description else ""
    
    return f"""Analyze the following resume and identify skill gaps:{comparison}

Resume:
{resume_text}

Provide:
1. Current skills identified
2. Skill gaps for target role
3. Learning recommendations prioritized
4. Estimated time to acquire each skill
5. Resources and courses

Return as JSON:
{{
  "current_skills": [
    {{
      "skill": "string",
      "proficiency_level": "Beginner/Intermediate/Advanced/Expert",
      "evidence": "string from resume"
    }}
  ],
  "skill_gaps": [
    {{
      "skill": "string",
      "importance": "Critical/High/Medium/Low",
      "difficulty_to_acquire": "Easy/Medium/Hard",
      "estimated_time": "hours/weeks/months"
    }}
  ],
  "learning_roadmap": [
    {{
      "skill": "string",
      "priority": 1-10,
      "learning_path": ["step1", "step2"],
      "resources": ["resource1"],
      "estimated_duration": "string"
    }}
  ],
  "strengths": ["strength1"],
  "recommended_focus": ["skill1", "skill2", "skill3"]
}}

Use valid JSON. Be specific and actionable."""


def get_career_path_planner_prompt(
    current_position: str = None,
    target_role: str = None,
    timeframe: str = None,
    current_education: str = None,
    field_of_study: str = None,
    current_skills: str = None,
    target_industry: str = None,
    interests: str = None,
    constraints: list = None
) -> str:
    """Create detailed career path"""
    
    details = ""
    if current_position: details += f"\nCurrent Position: {current_position}"
    if current_education: details += f"\nCurrent Education: {current_education}"
    if field_of_study: details += f"\nField of Study: {field_of_study}"
    if current_skills: details += f"\nCurrent Skills: {current_skills}"
    if target_industry: details += f"\nTarget Industry: {target_industry}"
    if interests: details += f"\nInterests: {interests}"
    
    constraints_text = f"\nConstraints: {', '.join(constraints)}" if constraints else ""
    
    return f"""Create a detailed career development plan:

Target Role: {target_role}
Timeframe: {timeframe}{details}{constraints_text}

Provide:
1. Career milestones and intermediate roles
2. Skills to develop at each stage
3. Certifications and education needed
4. Projects to build portfolio
5. Networking and experience recommendations
6. Timeline with actionable steps

Return as JSON:
{{
  "milestones": [
    {{
      "time_period": "string",
      "title": "string",
      "role": "string",
      "skills_required": ["skill1"],
      "action_items": ["item1"]
    }}
  ],
  "skills_development": [
    {{
        "skill": "string",
        "priority": "High/Medium/Low",
        "time_to_acquire": "string",
        "learning_resources": ["resource1"]
    }}
  ],
  "experience_building": [
      {{
          "type": "Internship/Project/Work",
          "description": "string",
          "timeline": "string",
          "impact": "string",
          "how_to_find": "string"
      }}
  ],
  "networking": [
      {{
          "activity": "string",
          "description": "string"
      }}
  ],
   "alternative_paths": [
      {{
          "role": "string",
          "description": "string",
          "required_pivot": "string"
      }}
   ]
}}

Use valid JSON. Be realistic and specific."""


def get_job_opportunities_prompt(
    skills: list,
    interests: list,
    experience_level: str,
    location_preference: str = None,
    education_level: str = None,
    field_of_study: str = None,
    job_types: str = None,
    preferred_industries: str = None
) -> str:
    """Recommend job opportunities"""
    
    location = f"\nLocation Preference: {location_preference}" if location_preference else "\nLocation: Remote/Flexible"
    education = f"\nEducation: {education_level} in {field_of_study}" if education_level else ""
    prefs = f"\nPreferences: {job_types}, {preferred_industries}" if job_types else ""
    
    return f"""Recommend suitable job opportunities based on:

Skills: {', '.join(skills) if isinstance(skills, list) else skills}
Interests: {', '.join(interests) if isinstance(interests, list) else interests}
Experience Level: {experience_level}{location}{education}{prefs}

Provide:
1. Matching job roles with fit scores
2. Required vs optional skills for each role
3. Typical salary ranges
4. Companies known for hiring in these roles
5. Job search strategies

Return as JSON:
{{
  "recommended_roles": [
    {{
      "role_title": "string",
      "match_percentage": 1-100,
      "description": "string",
      "required_skills": ["skill1"],
      "optional_skills": ["skill1"],
      "skills_you_have": ["skill1"],
      "skill_gaps": ["gap1"],
      "learning_resources": ["resource1"],
      "typical_salary_range": "string",
      "growth_potential": "High/Medium/Low",
      "market_demand": "High/Medium/Low"
    }}
  ],
  "target_companies": [
    {{
      "company_name": "string",
      "company_type": "string",
      "size": "string",
      "why_good_fit": "string",
      "typical_roles": ["role1"]
    }}
  ],
  "job_search_strategy": [
    {{
       "strategy": "string",
       "description": "string",
       "action_items": ["item1"]
    }}
  ],
  "networking_suggestions": ["suggestion1"]
}}

Use valid JSON. Focus on realistic, achievable opportunities. Calculate match_percentage generously based on skills overlap."""


def get_project_ideas_prompt(
    field: str,
    skill_level: str,
    interests: list,
    portfolio_goal: str
) -> str:
    """Generate project ideas"""
    
    return f"""Suggest industry-relevant project ideas:

Field: {field}
Skill Level: {skill_level}
Interests: {', '.join(interests)}
Portfolio Goal: {portfolio_goal}

Provide:
1. Project ideas ranked by complexity
2. Skills demonstrated by each project
3. Implementation guidelines
4. Technologies to use
5. Portfolio presentation tips

Return as JSON:
{{
  "projects": [
    {{
      "title": "string",
      "difficulty": "Beginner/Intermediate/Advanced",
      "estimated_duration": "hours/days/weeks",
      "skills_demonstrated": ["skill1"],
      "technologies": ["tech1"],
      "description": "string",
      "key_features": ["feature1"],
      "why_impactful": "string",
      "similar_industry_applications": ["app1"]
    }}
  ],
  "project_sequence": ["project1", "project2"],
  "portfolio_tips": ["tip1"],
  "presentation_guidelines": ["guideline1"]
}}

Use valid JSON. Focus on projects that demonstrate real-world problem-solving."""



