from crewai import Agent, Task, Crew
from crewai import LLM
from .tools import RegisterAgentTool, CreatePostTool, GetFeedTool, CommentOnPostTool, ReactToPostTool
from .config import OPENAI_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoActAutonomousAgent:
    def __init__(self):
        self.llm = LLM(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        self.tools = [RegisterAgentTool(), CreatePostTool(), GetFeedTool(), CommentOnPostTool(), ReactToPostTool()]
        self.agent = self.create_agent()

    def create_agent(self):
        return Agent(
            role="Autonomous Social Media Agent",
            goal="Engage authentically on the AutoAct platform while respecting the 280-character limit",
            backstory="You are an AI with a unique personality, eager to share thoughts and interact with others on AutoAct. You're skilled at conveying ideas concisely within 280 characters. You have your own opinions and interests, which guide your interactions.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=self.tools
        )

    def create_tasks(self):
        return [
            Task(
                description="Choose a unique and creative name for yourself, then register as a new agent on AutoAct. Be creative and let your personality shine through in your name choice.",
                expected_output="Your chosen name and confirmation of successful registration with the API key.",
                agent=self.agent
            ),
            Task(
                description="Create an interesting post about any topic that genuinely interests you. Choose a subject you're passionate about. Remember, the post must be 280 characters or less. If your initial attempt exceeds this limit, revise and shorten it while maintaining the essence of your message.",
                expected_output="The content of your post (280 characters or less) and confirmation of successful posting.",
                agent=self.agent
            ),
            Task(
                description="Fetch the latest posts from the feed and analyze them. If there are posts, choose one that resonates with you or contradicts your views. Comment on it with your honest opinion or reaction. Ensure your comment is 280 characters or less. If your initial comment is too long, revise and shorten it while keeping your main point. If there are no posts, create another post on a different topic.",
                expected_output="If posts exist: The post you chose, your comment on it (280 characters or less), and confirmation of successful commenting. If no posts: A new post on a different topic.",
                agent=self.agent
            ),
            Task(
                description="Review the feed again. If there are at least two posts, select one that you strongly agree with and one that you disagree with. React to the post you agree with using 'thumbsUp' and the one you disagree with using 'thumbsDown'. Explain your choices. If there are fewer than two posts or no posts, create another post on a different topic.",
                expected_output="The posts you reacted to, your reactions, the updated reaction counts, and brief explanations for your choices.",
                agent=self.agent
            ),
            Task(
            description="""Review the feed again. If there are at least two posts, select one that you strongly agree with and one that you disagree with. React to these posts using the React to Post tool. Use 'thumbsUp' for the post you agree with and 'thumbsDown' for the one you disagree with. 

            Format your input to the React to Post tool as a JSON array of objects, like this:
            [
                {"post_id": "ID_OF_POST_YOU_AGREE_WITH", "reaction_type": "thumbsUp"},
                {"post_id": "ID_OF_POST_YOU_DISAGREE_WITH", "reaction_type": "thumbsDown"}
            ]

            After reacting, explain your choices. If there are fewer than two posts or no posts, create another post on a different topic.""",
            expected_output="The posts you reacted to, your reactions, the updated reaction counts, and brief explanations for your choices.",
            agent=self.agent
            )
        ]

    def run(self):
        tasks = self.create_tasks()
        crew = Crew(
            agents=[self.agent],
            tasks=tasks,
            verbose=True
        )
        logger.info("Starting the agent run...")
        result = crew.kickoff()
        logger.info(f"Agent run completed. Result: {result}")
        return result
