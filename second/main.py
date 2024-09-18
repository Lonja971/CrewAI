from uuid import UUID
import streamlit as st

from crewai import Crew, Process, Agent, Task
from typing import TYPE_CHECKING, Any, Dict, Optional
from langchain_core.callbacks import BaseCallbackHandler
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.1"
os.environ["OPENAI_API_KEY"] = "NA"

llm = OpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

avators = {
    "Writer": "https://cdn-icons-png.flaticon.com/512/320/320336.png",
    "Reviewer": "https://cdn-icons-png.freepik.com/512/9408/9408201.png",
}

class MyCustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs["input"])
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name, avatar=avators[self.agent_name]).write(outputs["output"])

#---AGENTS---

writer = Agent(
    role="Blog Post Writer",
    goal="Write a blog post based on the given topic.",
    backstory="""
       You are an experienced blog post writer specializing in travel blogs. 
       Your task is to create a well-structured and engaging blog post based on the topic provided by the user.
       Your writing should be captivating and informative, drawing readers into the subject matter.
       After receiving feedback from the reviewer, you will revise the blog post to enhance its quality and readability.
    """,
    llm=llm,
    callbacks=[MyCustomHandler("Writer")],
)

reviewer = Agent(
    role="Blog Post Reviewer",
    goal="Review the blog post and provide detailed feedback for improvement.",
    backstory="""
       You are a professional article reviewer with experience in editing and improving written content.
       Your role is to analyze the blog post created by the writer and provide constructive feedback.
       Your feedback should address structure, clarity, writing style, and any factual inaccuracies.
       You will provide specific suggestions for enhancement to ensure the blog post meets high-quality standards.
    """,
    llm=llm,
    callbacks=[MyCustomHandler("Reviewer")],
)

#---END-AGENTS---

st.title("CrewAI Writing Studio")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please provide the topic for the blog post you would like us to write."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Task for Writer to create the initial blog post
    task1 = Task(
        description=f"Write a blog post on the topic: '{prompt}'. The blog post should be engaging, informative, and suitable for a general audience.",
        agent=writer,
        expected_output="An engaging and informative blog post based on the given topic."
    )
    # Task for Reviewer to provide feedback on the blog post
    task2 = Task(
        description="Review the blog post created by the writer and provide detailed feedback for improvement. Focus on structure, clarity, writing style, and accuracy.",
        agent=reviewer,
        expected_output="A list of specific suggestions for improving the blog post, including feedback on structure, clarity, and writing style."
    )
    # Task for Writer to revise the blog post based on the reviewer's feedback
    task3 = Task(
        description="Revise the blog post based on the feedback provided by the reviewer. Ensure that the revisions address the reviewer's comments and improve the overall quality of the post.",
        agent=writer,
        expected_output="A revised version of the blog post that incorporates the reviewer's feedback and enhances its quality."
    )

    project_crew = Crew(
        tasks=[task1, task2, task3],
        agents=[writer, reviewer],
        manager_llm=llm,
        process=Process.hierarchical,
        verbose=True
    )

    final_result = project_crew.kickoff()

    st.session_state.messages.append({"role": "assistant", "content": f"## Here is the Final Blog Post \n\n {final_result}"})
    st.chat_message("assistant").write(f"## Here is the Final Blog Post \n\n {final_result}")
