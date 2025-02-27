from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")


model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)


@CrewBase
class DevCrew:
    """Dev Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def junior_developer(self) -> Agent:
        return Agent(config=self.agents_config.get("junior_developer", {}))

    @agent
    def senior_developer(self) -> Agent:
        return Agent(config=self.agents_config.get("senior_developer", {}))

    @task
    def write_code(self) -> Task:
        return Task(config=self.tasks_config.get("write_code", {}))

    @task
    def review_code(self) -> Task:
        return Task(config=self.tasks_config.get("review_code", {}))

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True,
        )
    



# from crewai.flow.flow import Flow,start,listen


# class MainFlow(Flow):
#     @start()
#     def development(self):
#         result = DevCrew().crew().kickoff(
#             inputs={"problem": "Develope a Game Using Object Orinted Programming with complete Error Handling"})
#         self.state['response'] = result
#         return result


#     @listen(development)
#     def save_as_file(self,res):
#         with open('response.py', 'w') as f:
#             f.write(str(self.state['response']))
#             print("File saved as response.py")
        
    





# def kickoff():
#     final = MainFlow()
#     final_result = final.kickoff()


   

st.title("Welcome to Hasnain's Agentic World")
st.title("Python Code Generator Agent")

user_input = st.text_input("Enter the problem statement:", "")

if st.button("Generate Code"):
    if user_input.strip():
        with st.spinner("Generating code Please Wait..."):
            response = DevCrew().crew().kickoff(inputs={"problem": user_input})

        if response:  # Move the check outside the spinner block
            st.code(response, language='python')

            # Save the response as a file
            file_name = "response.py"
            with open(file_name, "w") as f:
                f.write(str(response))

            # Provide download button
            with open(file_name, "rb") as f:
                st.download_button(label="Download Generated Code",
                                   data=f,
                                   file_name=file_name,
                                   mime="text/x-python")
        else:
            st.error("No response generated. Please try again.")
    else:
        st.warning("Please enter a problem statement before generating code.")
    agents_config = "src/python/config/agents.yaml"
    tasks_config = "src/python/config/tasks.yaml"