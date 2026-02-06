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
    course_name: str,
    program_type: str,
    course_level: str,
    credit_hours: int,
    topics_covered: str,
    accreditation_framework: str,
    existing_outcomes: str = None
) -> str:
    """Map course content to learning outcomes"""
    
    existing_text = f"\nExisting Outcomes: {existing_outcomes}" if existing_outcomes else ""
    
    return f"""You are an academic assessment expert. Map following course content to learning outcomes using {accreditation_framework}.

Course: {course_name}
Program: {program_type}
Level: {course_level} ({credit_hours} credits)

Topics Covered:
{topics_covered}{existing_text}

Generate learning outcome mappings with:
1. Specific, measurable learning outcomes (CLOs)
2. Alignment with {accreditation_framework}
3. Assessment methods for each outcome
4. Teaching strategies to achieve outcomes

Return as JSON:
{{
  "learning_outcomes": [
    {{
      "clo_number": 1,
      "outcome_statement": "string",
      "blooms_level": "Apply/Analyze/Create",
      "assessment_method": "string"
    }}
  ],
  "topic_outcome_mapping": [
    {{
       "topic": "string",
       "clos": [1, 2],
       "teaching_strategies": ["strategy1"]
    }}
  ],
  "program_outcome_mapping": [
     {{
        "po_code": "PO1",
        "po_description": "string",
        "mapped_clos": [1],
        "mapping_strength": "High/Medium/Low"
     }}
  ],
  "assessment_strategy": [
     {{
        "assessment_type": "string",
        "weightage": 20,
        "evaluates_clos": [1, 2],
        "description": "string"
     }}
  ],
  "accreditation_alignment": [
     {{
        "framework": "{accreditation_framework}",
        "standards_met": ["standard1"],
        "gaps": ["gap1"]
     }}
  ]
}}

Use valid JSON. Ensure outcomes are SMART."""





def get_industry_alignment_prompt(
    program_name: str,
    specialization: str,
    core_courses: str,
    target_industries: str,
    geographic_region: str,
    elective_courses: str = None
) -> str:
    """Analyze industry alignment"""
    
    electives_text = f"\nElective Courses: {elective_courses}" if elective_courses else ""
    
    return f"""You are an industry-academic liaison expert. Analyze how well a {program_name} ({specialization}) aligns with {target_industries} industry needs in {geographic_region}.

Core Courses:
{core_courses}{electives_text}

Provide:
1. Current industry skill demands
2. Gaps in curriculum vs industry needs
3. Emerging technologies and trends to include
4. Practical skills and tools students should learn
5. Industry certifications to integrate
6. Real-world project suggestions

Return as JSON:
{{
  "overall_alignment_score": 85,
  "technical_alignment": 80,
  "tools_alignment": 70,
  "industry_skill_demands": [
    {{
      "skill": "string",
      "demand_level": "High/Medium/Low",
      "trend": "Rising/Stable/Declining",
      "salary_impact": "High/Medium/Low"
    }}
  ],
  "curriculum_coverage": [
    {{
       "skill_area": "string",
       "coverage_status": "Covered/Partially Covered/Missing",
       "courses_covering": ["course1"],
       "gaps": "string"
    }}
  ],
  "missing_critical_skills": [
    {{
       "skill": "string",
       "importance": "Critical/High",
       "recommendation": "string"
    }}
  ],
  "emerging_technologies": [
    {{
       "technology": "string",
       "adoption_stage": "Early/Growth/Mature",
       "relevance": "High/Medium",
       "suggested_action": "Integrate/Workshop/Elective"
    }}
  ],
  "recommendations": [
    {{
      "recommendation": "string",
      "priority": "High/Medium/Low",
      "implementation_effort": "Low/Medium/High",
      "expected_impact": "string"
    }}
  ]
}}

Use valid JSON. Base recommendations on current 2024-2026 industry standards."""


def get_topic_recommendations_prompt(
    course_name: str,
    course_level: str,
    current_topics: str,
    field: str,
    update_goals: str,
    student_background: str = None
) -> str:
    """Generate topic recommendations"""
    
    background = f"\nStudent Background: {student_background}" if student_background else ""
    
    return f"""You are a subject matter expert in {field}. Recommend changes to the curriculum for:

Course: {course_name}
Level: {course_level}
Current Topics: {current_topics}
Goals: {update_goals}{background}

Provide:
1. Emerging topics in the field
2. Topics that can be removed or updated
3. Foundational topics that may be missing
4. Suggested sequence for topics
5. Alignment with latest industry trends

Return as JSON:
{{
  "topics_to_add": [
    {{
      "topic": "string",
      "rationale": "string",
      "priority": "High/Medium/Low",
      "suggested_duration": "string",
      "learning_outcomes": ["outcome1"],
      "teaching_resources": ["resource1"]
    }}
  ],
  "topics_to_update": [
    {{
      "topic": "string",
      "current_status": "string",
      "suggested_update": "string",
      "reason": "string"
    }}
  ],
  "topics_to_remove": [
      {{
          "topic": "string",
          "reason": "string",
          "alternative": "string"
      }}
  ],
  "topic_sequence": [
      {{
          "topic": "string",
          "duration": "string",
          "builds_on": "string"
      }}
  ],
  "emerging_trends": [
      {{
          "trend": "string",
          "relevance": "High/Medium",
          "maturity_level": "Early/Growth/Mature",
          "recommendation": "string"
      }}
  ]
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
    current_education: str,
    field_of_study: str,
    target_role: str,
    target_industry: str,
    timeline: str,
    current_skills: str = "None specified",
    interests: str = None
) -> str:
    """Create detailed career path"""
    
    return f"""Create a detailed career development plan:

Target Role: {target_role}
Target Industry: {target_industry}
Timeline: {timeline}

Current Context:
- Education: {current_education} in {field_of_study}
- Skills: {current_skills}
- Interests: {interests if interests else "Not specified"}

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
      "timeline": "string (e.g., 0-6 months)",
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
    skill_level: str,
    current_skills: str,
    interests: str,
    project_type: str,
    complexity: str,
    timeline: str,
    skills_to_learn: str = None
) -> str:
    """Generate project ideas"""

    skills_learn_text = f"\nSkills to Learn: {skills_to_learn}" if skills_to_learn else ""
    
    return f"""Suggest industry-relevant project ideas:

Skill Level: {skill_level}
Current Skills: {current_skills}
Interests: {interests}
Project Type: {project_type}
Desired Complexity: {complexity}
Timeline: {timeline}{skills_learn_text}

Provide:
1. Project ideas matching these criteria
2. Skills demonstrated by each project
3. Implementation guidelines
4. Technologies to use
5. Portfolio presentation tips

Return as JSON:
{{
  "project_ideas": [
    {{
      "title": "string",
      "complexity": "{complexity}",
      "estimated_duration": "{timeline}",
      "description": "string",
      "learning_outcomes": ["outcome1"],
      "tech_stack": ["tech1"],
      "key_features": ["feature1"],
      "implementation_steps": ["step1"],
      "resources": ["resource1"],
      "portfolio_value": "string"
    }}
  ],
  "skill_progression_path": [
    {{
       "project": "string",
       "skill_focus": "string"
    }}
  ],
   "open_source_opportunities": [
      {{
         "project": "string",
         "description": "string",
         "good_for": "string"
      }}
   ]
}}

Use valid JSON. Focus on projects that demonstrate real-world problem-solving."""
