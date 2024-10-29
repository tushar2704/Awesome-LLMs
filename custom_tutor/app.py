import streamlit as st
from crewai import Agent, Task, Crew, Process
from groq import Groq
from typing import Dict
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

class LearningPathGenerator:
    def __init__(self):
        self.groq_client = Groq(api_key=api_key)
        
    def create_agents(self):
        # Curriculum Designer Agent
        curriculum_designer = Agent(
            role='Curriculum Designer',
            goal='Design comprehensive learning paths tailored to user needs',
            backstory="""Expert curriculum designer with years of experience in 
            educational planning and instructional design. Skilled at breaking down 
            complex topics into manageable learning modules.""",
            verbose=True
        )
        
        # Content Strategist Agent
        content_strategist = Agent(
            role='Content Strategist',
            goal='Develop engaging content and activities for each learning module',
            backstory="""Experienced content strategist specialized in creating 
            interactive and effective learning materials. Expert in balancing 
            theoretical knowledge with practical applications.""",
            verbose=True
        )
        
        # Progress Tracker Agent
        progress_tracker = Agent(
            role='Progress Tracker',
            goal='Design assessment methods and track learning milestones',
            backstory="""Learning analytics specialist focused on creating 
            measurable outcomes and progress tracking systems. Expert in 
            identifying key performance indicators in learning journeys.""",
            verbose=True
        )
        
        return curriculum_designer, content_strategist, progress_tracker

    def create_tasks(self, agents, user_inputs):
        curriculum_designer, content_strategist, progress_tracker = agents
        
        # Task 1: Design Curriculum Structure
        design_curriculum = Task(
            description=f"""Create a structured curriculum for {user_inputs['topic']} 
            focusing on {user_inputs['specific_thing']} over {user_inputs['duration']} weeks 
            with {user_inputs['hours_per_week']} hours per week commitment.""",
            agent=curriculum_designer,
            expected_output="Detailed curriculum structure with weekly objectives"
        )
        
        # Task 2: Create Content Plan
        create_content = Task(
            description="""Based on the curriculum structure, develop detailed 
            content and activities for each week, including practical exercises 
            and projects.""",
            agent=content_strategist,
            expected_output="Weekly content plan with specific activities"
        )
        
        # Task 3: Develop Progress Metrics
        develop_metrics = Task(
            description="""Create progress tracking metrics and assessment methods 
            for the learning path, including milestones and success indicators.""",
            agent=progress_tracker,
            expected_output="Progress tracking system with clear metrics"
        )
        
        return [design_curriculum, create_content, develop_metrics]

    def generate_learning_path(self, user_inputs: Dict) -> Dict:
        # Create agents and tasks
        agents = self.create_agents()
        tasks = self.create_tasks(agents, user_inputs)
        
        # Create and run the crew
        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            verbose=2,
            process=Process.sequential
        )
        
        # Execute the crew's tasks
        result = crew.kickoff()
        
        # Process the results into a structured format
        learning_path = self._process_crew_results(result, user_inputs)
        return learning_path

    def _process_crew_results(self, crew_result: str, user_inputs: Dict) -> Dict:
        total_hours = user_inputs['duration'] * user_inputs['hours_per_week']
        weeks = []
        
        # Parse crew results and generate weekly schedule
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

    # Rest of the methods remain the same
    def _generate_weekly_focus(self, user_inputs: Dict, week: int) -> str:
        # Existing implementation
        pass

    def _generate_activities(self, user_inputs: Dict, week: int) -> list:
        # Existing implementation
        pass

# Rest of the code (customize_learning_path, create_streamlit_ui, 
# display_learning_path, and main functions) remains the same