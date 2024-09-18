from dotenv import load_dotenv
from crewai import Crew
from tasks import MeetingprepTasks
from agents import MeetingPrepAgents
def main():
    load_dotenv()

    print("\n\n## Welcome to the Meeting Prep Crew")
    print("-----------------------------------")
    meeting_participants = input("What are the emails for the participants (other that you) in the meeting?\n")
    meeting_context = input("What is the context of the meeting?\n")
    meeting_objective = input("What is your objective for this meeting?\n")

    tasks = MeetingprepTasks()
    agents = MeetingPrepAgents()

    print("Initializing agents...")
    research_agent = agents.research_agent()
    industry_analysis_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()

    print("Creating tasks...")
    research_task = tasks.research_task(research_agent, meeting_participants, meeting_context)
    industry_analysis_task = tasks.industry_analysis_task(industry_analysis_agent, meeting_participants, meeting_context)
    meeting_strategy_task = tasks.meeting_strategy_task(meeting_strategy_agent, meeting_context, meeting_objective)
    summary_and_briefing_task = tasks.summary_and_briefing_task(summary_and_briefing_agent, meeting_context, meeting_objective)

    print("Setting task contexts...")
    meeting_strategy_task.context = [research_task, industry_analysis_task]
    summary_and_briefing_task.context = [research_task, industry_analysis_task, meeting_strategy_task]

    print("Initializing Crew...")
    crew = Crew(
        agents=[
            research_agent,
            industry_analysis_agent,
            meeting_strategy_agent,
            summary_and_briefing_agent
        ],
        tasks=[
            research_task,
            industry_analysis_task,
            meeting_strategy_task,
            summary_and_briefing_task
        ],
        process="sequential",
        iteration_limit=100,
        time_limit=300 
    )

    result = crew.kickoff()
    print("Crew result:", result)



if __name__ == "__main__":
    main()