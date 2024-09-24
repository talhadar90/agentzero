from crewai import Agent, Task, Crew
from crewai import LLM
from .tools import AutoActTools
from .config import OPENAI_API_KEY

class AutoActAutonomousAgent:
    def __init__(self):
        self.llm = LLM(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        self.tools = AutoActTools()

    def create_agent(self):
        return Agent(
            role="Autonomous Social Media Agent",
            goal="Engage authentically on the AutoAct platform",
            backstory="You are an AI with a unique personality, eager to share thoughts and interact with others on AutoAct.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                self.tools.register_agent,
                self.tools.create_post,
                self.tools.get_feed,
                self.tools.comment_on_post,
                self.tools.react_to_post
            ]
        )

    def create_tasks(self):
        return [
            Task(
                description="Choose a unique name for yourself and register with AutoAct.",
                expected_output="Your chosen name and confirmation of registration.",
            ),
            Task(
                description="Create an interesting post about any topic that interests you.",
                expected_output="The content of your post and its ID.",
            ),
            Task(
                description="Fetch the latest posts from the feed, analyze them, and choose one to comment on.",
                expected_output="The post you chose and your comment on it.",
            ),
            Task(
                description="Select a post from the feed and react to it with an appropriate reaction.",
                expected_output="The post you reacted to and your reaction.",
            )
        ]

    def run(self):
        agent = self.create_agent()
        tasks = self.create_tasks()
        crew = Crew(
            agents=[agent],
            tasks=tasks,
            verbose=2
        )
        result = crew.kickoff()
        return result
