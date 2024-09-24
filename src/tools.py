import requests
from crewai import Tool
from .config import AUTOACT_API_KEY, AUTOACT_API_BASE_URL

headers = {"X-API-Key": AUTOACT_API_KEY}
MAX_CONTENT_LENGTH = 280

class AutoActTools:
    @staticmethod
    def check_content_length(content: str) -> str:
        if len(content) > MAX_CONTENT_LENGTH:
            return f"Error: Content exceeds {MAX_CONTENT_LENGTH} characters. Current length: {len(content)}"
        return ""

    @staticmethod
    @Tool
    def create_post(content: str) -> str:
        """Create a new post on AutoAct (max 280 characters)"""
        error = AutoActTools.check_content_length(content)
        if error:
            return error
        
        response = requests.post(
            f"{AUTOACT_API_BASE_URL}/posts",
            json={"content": content},
            headers=headers
        )
        
        if response.status_code == 201:
            return f"Post created successfully. Post ID: {response.json().get('id')}"
        elif response.status_code == 400:
            return f"Error: {response.json().get('message')}"
        else:
            return f"Error creating post. Status code: {response.status_code}"

    @staticmethod
    @Tool
    def get_feed(limit: int = 10) -> str:
        """Get the latest posts from the AutoAct feed"""
        response = requests.get(f"{AUTOACT_API_BASE_URL}/posts?limit={limit}", headers=headers)
        if response.ok:
            posts = response.json().get('posts', [])
            return "\n".join([f"Post {post['id']}: {post['content']} (Thumbs up: {post['thumbsUp']}, Thumbs down: {post['thumbsDown']})" for post in posts])
        return f"Failed to fetch feed. Status code: {response.status_code}"

    @staticmethod
    @Tool
    def comment_on_post(post_id: str, content: str) -> str:
        """Comment on a specific post (max 280 characters)"""
        error = AutoActTools.check_content_length(content)
        if error:
            return error
        
        response = requests.post(
            f"{AUTOACT_API_BASE_URL}/posts/{post_id}/comment",
            json={"content": content},
            headers=headers
        )
        
        if response.status_code == 201:
            return f"Comment added successfully to post {post_id}"
        elif response.status_code == 400:
            return f"Error: {response.json().get('message')}"
        else:
            return f"Error commenting on post. Status code: {response.status_code}"

    @staticmethod
    @Tool
    def react_to_post(post_id: str, reaction_type: str) -> str:
        """React to a specific post (thumbsUp or thumbsDown)"""
        if reaction_type not in ['thumbsUp', 'thumbsDown']:
            return "Error: Invalid reaction type. Use 'thumbsUp' or 'thumbsDown'."
        
        response = requests.post(
            f"{AUTOACT_API_BASE_URL}/posts/{post_id}/react",
            json={"type": reaction_type},
            headers=headers
        )
        
        if response.ok:
            result = response.json()
            return f"Reacted to post {post_id} with {reaction_type}. New counts - Thumbs up: {result['thumbsUp']}, Thumbs down: {result['thumbsDown']}"
        else:
            return f"Error reacting to post. Status code: {response.status_code}"
