import streamlit as st
from crewai import Agent, Task, Crew, Process
from groq import Groq
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    raise ValueError("GROQ API key not found. Please check your .env file.")



st.set_page_config(page_title="Personalized Learning Path", page_icon=":books:")


def custom_css():
    st.markdown("""
        <style>
            /* Main Background and Text Colors */
            .main-container {
                background-color: #f5f5f5; /* Light gray background */
                color: #333333; /* Dark gray text */
            }
            /* Header Styling */
            h1, h2, h3 {
                color: #333333;
                font-family: Arial, sans-serif;
            }
            /* Metric Display Styling */
            .stMetricValue {
                color: #4CAF50; /* Light green metric values */
                font-weight: bold;
            }
            /* Form Field Styling */
            input, textarea {
                background-color: #ffffff; /* White background for inputs */
                color: #333333;
                border-radius: 8px;
                padding: 10px;
                border: 1px solid #d3d3d3; /* Light border */
            }
            /* Submit Button Styling */
            .stButton button {
                background-color: #4CAF50; /* Green button color */
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            .stButton button:hover {
                background-color: #45a049; /* Darker green on hover */
            }
            /* Expanders Styling */
            .streamlit-expanderHeader {
                background-color: #e0e0e0; /* Light grey background for expanders */
                color: #333333;
                border-radius: 8px;
                padding: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

# Apply CSS styles
custom_css()
class LearningPathGenerator:
    def __init__(self):
        self.groq_client = Groq(api_key=api_key)
    
    def create_curriculum_expert(self):
        return Agent(
            role='Curriculum Expert',
            goal='Design personalized learning paths and schedules',
            backstory='Expert in curriculum development with focus on personalized learning',
            verbose=True
        )
    
    def create_curriculum_process(self, user_inputs: Dict):
        curriculum_agent = self.create_curriculum_expert()
        curriculum_process = Process(
            name="Curriculum Design Process",
            tasks=[
                Task(
                    name=f"Generate content for Week {week}",
                    agent=curriculum_agent,
                    action=lambda week=week: self._generate_weekly_focus(user_inputs, week)
                ) for week in range(1, user_inputs['duration'] + 1)
            ]
        )
        Crew().run_process(curriculum_process)
        return curriculum_process

    def generate_learning_path(self, user_inputs: Dict) -> Dict:
        total_hours = user_inputs['duration'] * user_inputs['hours_per_week']
        weeks = []

        # Generate weekly schedule with in-depth content
        for week in range(1, user_inputs['duration'] + 1):
            week_content = {
                'week': week,
                'content_focus': self._generate_weekly_focus(user_inputs, week),
                'hours': user_inputs['hours_per_week'],
                'activities': self._generate_activities(user_inputs, week)
            }
            weeks.append(week_content)

        return {
            'total_weeks': user_inputs['duration'],
            'hours_per_week': user_inputs['hours_per_week'],
            'total_hours': total_hours,
            'schedule': weeks,
            'topic': user_inputs['topic'],
            'specific_focus': user_inputs['specific_thing']
        }
    
    def _generate_weekly_focus(self, user_inputs: Dict, week: int) -> str:
        prompt = f"""
        Generate a detailed weekly curriculum for week {week} of {user_inputs['duration']} weeks 
        on {user_inputs['topic']} focusing specifically on {user_inputs['specific_thing']}. 
        The response should include a 1500-word breakdown covering:
        
        1. Latest research insights or breakthroughs in this area.
        2. Key concepts or subtopics to focus on this week.
        3. Recommended resources (articles, books, papers).
        4. Practical applications and exercises related to the week’s focus.
        
        Format the content as a well-structured, research-backed weekly guide.
        """
        response = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=4096  # Increased to allow for a more extended response
        )
        return response.choices[0].message.content
    
    def _generate_activities(self, user_inputs: Dict, week: int) -> list:
        hours_per_week = user_inputs['hours_per_week']
        return [
            f"Theory and Concepts ({hours_per_week * 0.3:.1f} hours)",
            f"Practical Exercises ({hours_per_week * 0.4:.1f} hours)",
            f"Projects and Applications ({hours_per_week * 0.3:.1f} hours)"
        ]

def customize_learning_path(user_inputs: Dict) -> Dict:
    generator = LearningPathGenerator()
    return generator.generate_learning_path(user_inputs)

def create_streamlit_ui() -> Dict:
    
    st.title("🎓 AI-Powered Personal Learning Path")
    st.subheader("👩🏽‍🏫 Developed by Tushar Aggarwal")
    
    with st.form("learning_path_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("What topic would you like to learn?", 
                                  placeholder="e.g., Python Programming, Data Science")
            specific_thing = st.text_input("Any specific aspect to focus on?", 
                                           placeholder="e.g., Web Development, Machine Learning")
            
        with col2:
            duration = st.number_input("Duration (weeks)", 
                                       min_value=1, max_value=52, value=4)
            hours_per_week = st.number_input("Hours per week", 
                                             min_value=1, max_value=40, value=5)
        
        submit_button = st.form_submit_button("Generate Learning Path")
        
    return {
        "topic": topic,
        "specific_thing": specific_thing,
        "duration": duration,
        "hours_per_week": hours_per_week
    } if submit_button else None

def display_learning_path(learning_path):
    st.subheader("📚 Your Customized Learning Path")
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Weeks", learning_path['total_weeks'])
    col2.metric("Hours per Week", learning_path['hours_per_week'])
    col3.metric("Total Hours", learning_path['total_hours'])
    
    # Weekly breakdown with expanded in-depth content
    st.subheader("📅 Weekly Schedule")
    for week in learning_path['schedule']:
        with st.expander(f"Week {week['week']}"):
            st.markdown(f"**Focus:** {week['content_focus']}")
            st.markdown("**Activities:**")
            for activity in week['activities']:
                st.markdown(f"- {activity}")
    
    # Learning recommendations
    st.subheader("🎯 Learning Recommendations")
    st.info(f"""
        Based on your commitment of {learning_path['hours_per_week']} hours per week:
        - Break down your study sessions into {learning_path['hours_per_week']/5:.1f} hour blocks
        - Balance between {learning_path['topic']} fundamentals and {learning_path['specific_focus']}
        - Include regular practice and project work
    """)

def main():
    user_inputs = create_streamlit_ui()
    
    if user_inputs:
        with st.spinner("🤖 Creating your personalized learning path..."):
            learning_path = customize_learning_path(user_inputs)
            display_learning_path(learning_path)

if __name__ == "__main__":
    main()
