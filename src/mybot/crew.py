
## pip install "crewai[tools]"

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool
from mybot.tools.requester import HttpRequesterTool
from mybot.tools.jwt_manipulater import JwtManipullationTool
import litellm
from langchain.chat_models import ChatOpenAI
from langchain_google genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()


# Configure litellm
os.environ["OPENAI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
litellm.api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatOpenAI(  ##i can use chatgpt reaper on. use gemini
model_name="gemini/gemini-1.5-flash",
temperature=0.5,
openai_api_key=os.getenv("GOOGLE_API_KEY"),
max_tokens=1000
)

@CrewBase
class MyBotCrew():
	"""mybot crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def mybot(self) -> Agent:
		return Agent(
			config=self.agents_config['mybot'],
			tools=[FileReadTool(),FileWriterTool(),DirectoryReadTool(),HttpRequesterTool(),JwtManipullationTool()],
			verbose=True,
			llm=llm,
		)

	@task
	def create_jwt_none_attack_vector_task(self) -> Task:
		return Task(
			config=self.tasks_config['create_jwt_none_attack_vector'],
			tools=[FileReadTool(),FileWriterTool(),DirectoryReadTool(),JwtManipullationTool()],
			chunk_size=512, # Process data in smaller chunks(optimission)
			output_file='output/jwt_none_attack_vector_task.txt',
			create_directory=True,
		)
	
	@task
	def execute_jwt_none_attack_vector_task(self) -> Task:
		return Task(
			config=self.tasks_config['execute_jwt_none_attack_vector_task'],
			tools=[FileReadTool(),FileWriterTool(),DirectoryReadTool(),HttpRequesterTool()],
			chunk_size=512,
			output_file='output/execute_jwt_none_attack_vector_task.txt',
			create_directory=True,
			context=[self.create_jwt_none_attack_vector_task()]
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Mybot crew"""
		return Crew(
			agents=self.agents, #Automatically created by the @agent decorator
			tasks=self.tasks, #Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			output_log_file="mybot.log"
		)