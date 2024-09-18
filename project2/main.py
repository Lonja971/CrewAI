import os
from crewai import Crew
from agents import AllAgents
from tasks import AllTasks
from crewai.telemetry import Telemetry

#def noop(*args, **kwargs):
#    print("Telemetry method called and noop'd\n")
#    pass
#for attr in dir(Telemetry):
#    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
#        setattr(Telemetry, attr, noop)

# AI Topic Exploration

os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.1"
os.environ["OPENAI_API_KEY"] = "NA"

print("\n\n---PREPARATION---\n")

user_question = input("What do you want to know about?\n")
user_lang = input("Which language do you prefer?\n")

print("Create instances of AllAgents and AllTasks")
tasks = AllTasks()
agents = AllAgents()

print("Initialize agents")
info_agent = agents.info_agent()
analysis_agent = agents.analysis_agent()
innovation_agent = agents.innovation_agent()

print("Initialize tasks")
task1 = tasks.task1(info_agent, user_question, user_lang)
task2 = tasks.task2(analysis_agent, user_lang)
task3 = tasks.task3(innovation_agent, user_lang)

print("Create Crew and pass agents and tasks")
crew = Crew(
    agents=[info_agent, analysis_agent, innovation_agent],
    tasks=[task1, task2, task3],
    verbose=True
)

if user_question.strip():
    result = crew.kickoff()
else:
    result = "You must provide a valid question."

print("\n--RESPOND---\n")
print(result)
print("\n\n")
