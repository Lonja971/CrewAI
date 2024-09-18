from crewai import Task

class AllTasks():
    def task1(self, agent, user_question, user_lang):
        return Task(
            description=f"Tell me all about {user_question}.",
            expected_output=f"Give me in {user_lang if user_lang not in [None, ''] else 'English'} language a quick summary of the current state of {user_question}.",
            agent=agent
        )

    def task2(self, agent, user_lang):
        return Task(
            description="Analyze the impact of AI on various sectors, including healthcare, finance, and education.",
            expected_output=f"Provide an analysis of how AI is currently transforming these industries. Output should be in {user_lang if user_lang not in [None, ''] else 'English'}.",
            agent=agent
        )

    def task3(self, agent, user_lang):
        return Task(
            description="Imagine and describe innovative future applications of AI in 10 years from now.",
            expected_output=f"Provide forward-looking scenarios for AI development. Output should be in {user_lang if user_lang not in [None, ''] else 'English'}.",
            agent=agent
        )
