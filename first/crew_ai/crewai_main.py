import os
from crewai import Crew, Process, Agent, Task
from crew_ai.agents import AllAgents
from crew_ai.tasks import AllTasks
from langchain.llms import OpenAI

def process_user_blog(user_text):
    os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
    os.environ["OPENAI_MODEL_NAME"] = "llama3.1"
    os.environ["OPENAI_API_KEY"] = "NA"

    tasks = AllTasks()  # Створення об'єкта з усіма завданнями
    agents = AllAgents()  # Створення об'єкта з агентами

    info_agent = agents.get_info_agent()  # Одержання агента для інформації
    analysis_agent = agents.get_analyst_agent()  # Одержання агента-аналітика
    writer_agent = agents.get_writer_agent()  # Одержання агента-письменника

    # Створюємо завдання для аналізу та написання блогу
    analyze_task = tasks.create_analysis_task(analysis_agent, user_text)  # Завдання на аналіз
    write_task = tasks.create_write_task(writer_agent)  # Завдання на покращення блогу

    # Створюємо модель LLM для управління процесом
    manager_llm = OpenAI(
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

    # Створюємо екземпляр Crew з агентами та завданнями
    crew = Crew(
        agents=[info_agent, analysis_agent, writer_agent],
        tasks=[analyze_task, write_task],  # Передаємо завдання під час створення
        manager_llm=manager_llm,  # Додаємо менеджера процесу
        process=Process.hierarchical,  # Використовуємо ієрархічний процес
        verbose=True
    )

    if user_text.strip():
        result = crew.kickoff()  # Запуск процесу агентів
    else:
        result = "You must provide a valid text."

    return result
