from textwrap import dedent
from crewai import Task

class MeetingprepTasks():
    def research_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description = dedent(f"""
                Conduct comprehensive research on each of the individuals and companies
                involved in the upcoming meeting. Gather information on recent
                news, achievements, professional background, and any relevant
                budiness activities.
                               
                participants: {meeting_participants}
                Meeting Context; {meeting_context} """), 
            expected_output = dedent(f"""
                A detailed repost summarizing key findings about each particiant
                and company, highlighting information that could be relevant for the meeting.  """),
            agent = agent,
        )
    
    def industry_analysis_task(self, agent, meeting_participants, meeting_context):
        return Task(
            description=dedent(f"""
                Analyze the current industry trends, challenges, and opportunities
                relevant to the meeting's context. Consider market reports, recent
                developments, and expect options to provide a comprehensive
                overview of the industry landscape.
                            
                Participants: {meeting_participants}
                Meeting Context: {meeting_context} """), 
            expected_output=dedent(f"""
                An insightful analysis that identifies major trends, potential
                challenges, and strategic opportunities."""),
            async_execution=False,
            agent=agent,
        )

    
    def meeting_strategy_task(self, agent, meeting_context, meeting_objective):
        return Task(
            description = dedent(f"""
                Develop strategic talking points, questions, and discussion angles
                for the meeting based on the research and industry analysis conducted.
                               
                Meeting Context: {meeting_context}
                Meeting objective; {meeting_objective} """), 
            expected_output = dedent(f"""
                Complate repor with a list of key talking points, strategic questions
                to ask to help achieve the meetings objective during the meeting """),
            agent = agent,
        )
    
    def summary_and_briefing_task(self, agent, meeting_context, meeting_objective):
        return Task(
            description = dedent(f"""
                Compile all the research findings, industry analysis, and strategic
                talking points into a concise, comprehensive briefing document for
                the meeting.
                Ensure the briefing is easy to digest and equips the meeting
                participants with all necessary information and strategies.
                               
                Meeting Context: {meeting_context}
                Meeting objective; {meeting_objective} """), 
            expected_output = dedent(f"""
                A well-structured briefing document that includes sections for
                particiant bios, industry overview, talking points, and
                strategic recomemendations. """),
            agent = agent,
        )