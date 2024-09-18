from crewai import Task

class AllTasks():
    # Завдання для аналізу блогу
    def create_analysis_task(self, agent, blog_text):
        return Task(
            description="Analyze the given blog for structure, tone, clarity, and grammar improvements.",
            expected_output="Provide detailed feedback on the areas that need improvement.",
            input_data={"blog_text": blog_text},  # Передача тексту блогу на аналіз
            agent=agent
        )

    # Завдання для написання покращеного блогу
    def create_write_task(self, agent):
        return Task(
            description="Rewrite the blog based on the feedback provided by the analyst.",
            expected_output="Provide a more engaging, clearer, and well-structured blog post.",
            input_data=None,  # Вхідні дані будуть надані пізніше після аналізу
            agent=agent
        )
