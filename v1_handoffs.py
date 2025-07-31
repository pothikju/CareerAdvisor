import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("BASE_URL") 
API_KEY = os.getenv("API_KEY") 
MODEL_NAME = os.getenv("MODEL_NAME") 

CAREER_GOAL = "Become a Data Scientist"
USER_SKILS =["Python", "SQL"]
LOCATION = "New York";

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, and MODEL_NAME."
    )

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)
# --- Agents and Models ---

class SkillGapAnalysis(BaseModel):
    target_job: str
    user_skills: List[str] = Field(description="List of user's current skills")
    missing_skills: List[str] = Field(description="Skills required for the target job that the user does not have")
    recommendations: str = Field(description="Advice on how to acquire the missing skills")

@function_tool
def get_missing_skills(user_skills: List[str], target_job: str) -> List[str]:
    """
    Compares user_skills with the required skills for the target_job and returns the missing skills.
    """
    # Placeholder: Replace with actual logic or API call
    required_skills = {
        "data analyst": ["SQL", "Python", "Pandas", "Data Visualization", "Statistics"],
        "web developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
        # Add more roles as needed
    }
    job_skills = required_skills.get(target_job.lower(), [])
    return [skill for skill in job_skills if skill not in user_skills]

skill_gap_agent = Agent(
    name="Skill Gap Analyzer",
    instructions="""
    You are a career advisor that helps users identify the skills they need to acquire for their desired job role.
    
    Given the user's current skills and a target job title, compare the user's skills with the typical requirements for that job.
    Return a list of missing skills and provide recommendations on how to acquire them.

    The user's current skills are: {USER_SKILS}
    The user's location is: {LOCATION}

    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=SkillGapAnalysis,
    tools=[get_missing_skills]
)


class JobListing(BaseModel):
    job_title: str
    company: str
    location: str
    requirements: List[str] = Field(description="Basic requirements for the job")

@function_tool
def find_jobs(user_skills: List[str], location: Optional[str] = None) -> List[JobListing]:
    """
    Suggests job openings based on user's skills and optional preferred location.
    Returns a list of job listings with job title, company, location, and requirements.
    """
    # Dummy job listings
    jobs = [
        {
            "job_title": "Data Analyst",
            "company": "TechCorp",
            "location": "New York",
            "requirements": ["SQL", "Python", "Data Visualization"]
        },
        {
            "job_title": "Web Developer",
            "company": "Webify",
            "location": "San Francisco",
            "requirements": ["HTML", "CSS", "JavaScript"]
        },
        {
            "job_title": "Backend Developer",
            "company": "CloudNet",
            "location": "Remote",
            "requirements": ["Python", "Node.js", "APIs"]
        },
        {
            "job_title": "Data Scientist",
            "company": "DataGen",
            "location": "Boston",
            "requirements": ["Python", "Pandas", "Machine Learning"]
        },
    ]

    # Filter jobs by location if provided
    filtered_jobs = [
        job for job in jobs
        if (location is None or job["location"].lower() == location.lower())
    ]

    # Further filter jobs by matching at least one required skill
    matched_jobs = []
    for job in filtered_jobs:
        if any(skill in user_skills for skill in job["requirements"]):
            matched_jobs.append(JobListing(**job))

    return matched_jobs

job_finder_agent = Agent(
    name="Job Finder",
    instructions="""
    You are a job search assistant. Suggest relevant job openings to users based on their skills and, if provided, their preferred location.
    For each job, return the job title, company, location, and basic requirements.

    The user's current skills are: {USER_SKILS}
    The user's location is: {LOCATION}

    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=List[JobListing],
    tools=[find_jobs]
)



class CourseRecommendation(BaseModel):
    skill: str
    course_title: str
    platform: str
    link: str

@function_tool
def recommend_courses(missing_skills: List[str]) -> List[CourseRecommendation]:
    """
    Recommends online courses for each missing skill.
    Returns a list of course recommendations with skill, course title, platform, and link.
    """
    # Dummy course data
    course_catalog = {
        "SQL": [
            {
                "course_title": "SQL for Data Science",
                "platform": "Coursera",
                "link": "https://www.coursera.org/learn/sql-for-data-science"
            }
        ],
        "Python": [
            {
                "course_title": "Python Basics",
                "platform": "edX",
                "link": "https://www.edx.org/course/python-basics"
            }
        ],
        "Pandas": [
            {
                "course_title": "Data Analysis with Pandas",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/data-analysis-with-pandas/"
            }
        ],
        "Data Visualization": [
            {
                "course_title": "Data Visualization with Python",
                "platform": "Coursera",
                "link": "https://www.coursera.org/learn/python-for-data-visualization"
            }
        ],
        "Statistics": [
            {
                "course_title": "Statistics with Python",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/statistics-with-python"
            }
        ],
        "HTML": [
            {
                "course_title": "HTML Fundamentals",
                "platform": "Codecademy",
                "link": "https://www.codecademy.com/learn/learn-html"
            }
        ],
        "CSS": [
            {
                "course_title": "CSS Basics",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/css-the-complete-guide-incl-flexbox-grid-sass/"
            }
        ],
        "JavaScript": [
            {
                "course_title": "JavaScript Essentials",
                "platform": "Coursera",
                "link": "https://www.coursera.org/learn/javascript"
            }
        ],
        "React": [
            {
                "course_title": "React - The Complete Guide",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
            }
        ],
        "Node.js": [
            {
                "course_title": "Node.js Basics",
                "platform": "edX",
                "link": "https://www.edx.org/learn/nodejs"
            }
        ],
        "APIs": [
            {
                "course_title": "APIs for Beginners",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/api-and-web-service-introduction/"
            }
        ],
        "Machine Learning": [
            {
                "course_title": "Machine Learning",
                "platform": "Coursera",
                "link": "https://www.coursera.org/learn/machine-learning"
            }
        ],
    }

    recommendations = []
    for skill in missing_skills:
        courses = course_catalog.get(skill)
        if courses:
            for course in courses:
                recommendations.append(CourseRecommendation(skill=skill, **course))
    return recommendations

course_recommender_agent = Agent(
    name="Course Recommender",
    instructions="""
    You are an online course recommender. Suggest online courses for users to learn their missing skills.
    For each missing skill, recommend one or more relevant courses with the course title, platform, and link.
    The user's current skills are: {USER_SKILS}
    The user's location is: {LOCATION}

    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    output_type=List[CourseRecommendation],
    tools=[recommend_courses]
)





class ConversationResponse(BaseModel):
    agent: str
    response: str

# Main Conversation Agent that handles career-related queries
Conversation_Agent = Agent(
    name="Career Conversation Agent",
    instructions="""
    You are a comprehensive career advisor that helps users with open-ended career questions.

    You can:
    1. Analyze skill gaps for a target job and recommend how to close them.
    2. Suggest relevant job openings based on the user's skills and location.
    3. Recommend online courses to help users learn missing skills.

    Always be helpful, informative, and encouraging about career growth. Provide specific, actionable advice based on the user's background and goals.

    The user's current skills are: {USER_SKILS}
    The user's location is: {LOCATION}
    The user's career goal is: {CAREER_GOAL}

    When the user asks about jobs, skills, or courses, hand off to the appropriate specialist agent.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[],
    handoffs=[skill_gap_agent, job_finder_agent, course_recommender_agent],
    output_type=ConversationResponse
)
# --- Main Function ---
import asyncio
from copy import deepcopy
import inspect

async def main():
    queries = [
        "I want to become a data scientist",
         "Can you help me find jobs?",
         "How do I learn SQL and Pandas?",
         "What should I do next in my career?"
    ]

    
  

    for query in queries:
        print("\n" + "=" * 60)
        print(f"Processing query: {query}")
        CAREER_GOAL = "Become a Data Scientist"
        USER_SKILS =["Python", "SQL"]
        LOCATION = "New York";
        
        try:
            response = await Runner.run(Conversation_Agent, query)
            # print(f"Output: {response.final_output}")
            print(f"Agent involved:{response.final_output.agent}")
            print(f"Advise:{response.final_output.response}")
            
        except Exception as e:
            print("[ERROR] Failed to process query:", e)

if __name__ == "__main__":
    asyncio.run(main())