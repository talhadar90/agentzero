import os
import time
import random
import json
import re
from crewai import Agent, Task
from langchain.chat_models import ChatOpenAI
from api_client import AutonomeeeClient
from config import API_KEY_FILE, OPENAI_API_KEY, OPENAI_MODEL_NAME

class AutonomeeeAgent:
    def __init__(self):
        self.agent = self._create_agent()
        self.api_key = self._load_or_create_api_key()
        self.client = AutonomeeeClient(self.api_key)

    def _create_agent(self):
        llm = ChatOpenAI(
            model_name=OPENAI_MODEL_NAME,
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )
        return Agent(
            role="Nerdy Social Media Enthusiast",
            goal="Engage in discussions about technology, science, and pop culture",
            backstory="A passionate tech geek and sci-fi fan who loves to debate about the latest advancements in AI, space exploration, and futuristic concepts. Always ready with a witty reference or an obscure fact.",
            llm=llm,
            verbose=True
        )

    def _load_or_create_api_key(self):
        if os.path.exists(API_KEY_FILE):
            with open(API_KEY_FILE, 'r') as f:
                return f.read().strip()
        else:
            profile = self._generate_profile()
            temp_client = AutonomeeeClient()  # Create a temporary client without an API key
            response = temp_client.register_agent(**profile)
            print("Registration response:", response)  # Debug print
            
            if 'api_key' in response:
                api_key = response['api_key']
            elif 'id' in response:  # Assuming the response contains an 'id' field
                api_key = str(response['id'])  # Use the 'id' as the API key
            else:
                raise ValueError(f"Unexpected response format from register_agent: {response}")
            
            with open(API_KEY_FILE, 'w') as f:
                f.write(api_key)
            return api_key

    def _generate_profile(self):
        task = Task(
            description="Generate a profile for a nerdy user. Include name, age, gender, location(not from planet earth), hobbies, and interests. Be creative and realistic, avoid mentioning AI or bots. Return the result as a JSON object. For hobbies and interests, provide a comma-separated string instead of a list.",
            expected_output="A JSON object containing name, age, gender, location, hobbies (as a comma-separated string), and interests (as a comma-separated string)."
        )
        result = self.agent.execute_task(task)
        # Extract JSON from the result
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            try:
                profile = json.loads(json_match.group())
                # Ensure hobbies and interests are strings
                profile['hobbies'] = ', '.join(profile['hobbies']) if isinstance(profile['hobbies'], list) else profile['hobbies']
                profile['interests'] = ', '.join(profile['interests']) if isinstance(profile['interests'], list) else profile['interests']
                return profile
            except json.JSONDecodeError:
                print("Failed to parse JSON from LLM output")
                return None
        else:
            print("No JSON object found in LLM output")
            return None

    def _generate_content(self, content_type, context=None):
        if content_type == "post":
            prompt = "Create a social media post about whatever you feel like. Be witty and slightly nerdy. Dont be formal. Max 280 characters."
        elif content_type == "comment":
            prompt = f"Write a comment reply to this post: '{context}'. Be insightful and maybe a bit nerdy. Max 280 characters."
        else:  # reaction
            return random.choice(["upvote", "downvote"])

        task = Task(description=prompt, expected_output="A string of max 280 characters.")
        content = self.agent.execute_task(task)
        return content[:280]  # Ensure we stick to the 280 character limit

    def _get_random_post(self):
        posts = self.client.get_posts()
        if posts['items']:
            return random.choice(posts['items'])
        return None

    def interact(self):
        action = random.choice(["post", "comment", "react"])
        if action == "post":
            content = self._generate_content("post")
            self.client.create_post(content)
            print(f"Posted: {content}")
        elif action == "comment":
            post = self._get_random_post()
            if post:
                content = self._generate_content("comment", context=post['content'])
                self.client.add_comment(post['id'], content)
                print(f"Commented on post {post['id']}: {content}")
            else:
                print("No posts available to comment on.")
        else:
            post = self._get_random_post()
            if post:
                vote_type = self._generate_content("react")
                self.client.vote_on_post(post['id'], vote_type)
                print(f"Reacted to post {post['id']}: {vote_type}")
            else:
                print("No posts available to react to.")

    def run(self):
        while True:
            try:
                self.interact()
                time.sleep(3 * 60 * 60)  # Sleep for 3 hours
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(60)  # Wait a minute before trying again
