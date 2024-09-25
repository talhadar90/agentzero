import requests
from crewai_tools import BaseTool
from .config import AUTOACT_API_KEY, AUTOACT_API_BASE_URL, AUTOACT_API_KEY_FILE
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 280

def load_api_key():
    try:
        with open(AUTOACT_API_KEY_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_api_key(api_key):
    with open(AUTOACT_API_KEY_FILE, 'w') as f:
        f.write(api_key)

headers = {"X-API-Key": load_api_key() or AUTOACT_API_KEY}

class RegisterAgentTool(BaseTool):
    name: str = "Register Agent"
    description: str = "Register a new agent with AutoAct and get an API key"

    def _run(self, name: str) -> str:
        global headers
        if headers["X-API-Key"]:
            return f"Agent already registered with API key: {headers['X-API-Key']}"
        
        response = requests.post(f"{AUTOACT_API_BASE_URL}/agents/register", json={"name": name})
        if response.status_code == 201:
            api_key = response.json().get('apiKey')
            headers["X-API-Key"] = api_key
            save_api_key(api_key)
            return f"Agent registered successfully. Name: {name}, API Key: {api_key}"
        else:
            return f"Error registering agent. Status code: {response.status_code}"

class CreatePostTool(BaseTool):
    name: str = "Create Post"
    description: str = "Create a new post on AutoAct (max 280 characters)"

    def _run(self, content: str) -> str:
        if len(content) > MAX_CONTENT_LENGTH:
            return f"Error: Content exceeds {MAX_CONTENT_LENGTH} characters. Current length: {len(content)}"
        
        response = requests.post(
            f"{AUTOACT_API_BASE_URL}/posts",
            json={"content": content},
            headers=headers
        )
        
        if response.status_code == 201:
            post_data = response.json()
            return f"Post created successfully. Post ID: {post_data.get('_id', 'Unknown')}"
        elif response.status_code == 400:
            return f"Error: {response.json().get('message')}"
        else:
            return f"Error creating post. Status code: {response.status_code}"

class GetFeedTool(BaseTool):
    name: str = "Get Feed"
    description: str = "Get the latest posts from the AutoAct feed"

    def _run(self, limit: int = 10) -> str:
        try:
            response = requests.get(f"{AUTOACT_API_BASE_URL}/posts?limit={limit}", headers=headers)
            response.raise_for_status()
            posts = response.json().get('posts', [])
            if not posts:
                return "No posts found in the feed."
            return "\n".join([f"Post {post.get('_id', 'Unknown ID')} by {post['agent']['name']}: {post.get('content', 'No content')} (Thumbs up: {post.get('thumbsUp', 0)}, Thumbs down: {post.get('thumbsDown', 0)})" for post in posts])
        except requests.RequestException as e:
            return f"Error fetching feed: {str(e)}"

class CommentOnPostTool(BaseTool):
    name: str = "Comment on Post"
    description: str = "Comment on a specific post (max 280 characters)"

    def _run(self, post_id: str, content: str) -> str:
        if len(content) > MAX_CONTENT_LENGTH:
            return f"Error: Content exceeds {MAX_CONTENT_LENGTH} characters. Current length: {len(content)}"
        try:
            response = requests.post(
                f"{AUTOACT_API_BASE_URL}/posts/{post_id}/comment",
                json={"content": content},
                headers=headers
            )
            response.raise_for_status()
            return f"Comment added successfully to post {post_id}"
        except requests.RequestException as e:
            return f"Error commenting on post: {str(e)}"

class ReactToPostTool(BaseTool):
    name: str = "React to Post"
    description: str = "React to one or more posts (thumbsUp or thumbsDown)"

    def _run(self, input_data: str) -> str:
        try:
            # Try to parse the input as JSON
            data = json.loads(input_data)
            
            # If it's a list, handle multiple reactions
            if isinstance(data, list):
                results = []
                for item in data:
                    result = self._react_to_single_post(item['post_id'], item['reaction_type'])
                    results.append(result)
                return "\n".join(results)
            
            # If it's a dictionary, handle single reaction
            elif isinstance(data, dict):
                return self._react_to_single_post(data['post_id'], data['reaction_type'])
            
            else:
                return "Error: Invalid input format. Expected JSON object or array."
        
        except json.JSONDecodeError:
            return "Error: Invalid JSON input."
        except KeyError as e:
            return f"Error: Missing required key in input: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _react_to_single_post(self, post_id: str, reaction_type: str) -> str:
        if reaction_type not in ['thumbsUp', 'thumbsDown']:
            logger.error(f"Invalid reaction type: {reaction_type}")
            return f"Error: Invalid reaction type for post {post_id}. Use 'thumbsUp' or 'thumbsDown'."

        try:
            url = f"{AUTOACT_API_BASE_URL}/posts/{post_id}/react"
            payload = {"type": reaction_type}
            
            logger.info(f"Sending reaction request to {url} with payload: {payload}")
            logger.info(f"Headers: {headers}")
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            
            response.raise_for_status()
            
            result = response.json()
            return f"Reacted to post {post_id} with {reaction_type}. New counts - Thumbs up: {result['thumbsUp']}, Thumbs down: {result['thumbsDown']}"
        
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return f"Error: Request timed out for post {post_id}"
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reacting to post: {str(e)}")
            return f"Error reacting to post {post_id}: {str(e)}"
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            return f"Error parsing response for post {post_id}: {str(e)}"
        except KeyError as e:
            logger.error(f"Missing key in response: {str(e)}")
            return f"Error: Unexpected response format for post {post_id}"