# Autonomeee Agent Setup Guide

This guide will help you set up and run your own Autonomeee Agent.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- A GitHub account
- An OpenAI API key

## Step 1: Clone the Repository

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to store the project.
3. Run the following command:

    ```git clone https://github.com/your-username/autonomeee-agent.git ```

    ```cd autonomeee-agent ```

## Step 2: Set Up a Virtual Environment

1. Create a virtual environment:

    ```python3 -m venv venv```

2. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

## Step 3: Install Dependencies

Install the required packages:

    pip install -r requirements.txt

## Step 4: Configure the Agent

1. Create a `.env` file in the project root directory.
2. Add your OpenAI API key to the `.env` file:

    `OPENAI_API_KEY=your_api_key_here`

    `OPENAI_MODEL_NAME=gpt-4o-mini`

Replace `your_api_key_here` with your actual OpenAI API key.

## Step 5: Run the Agent

You can run the agent directly using Python:

    python3 main.py

## Step 6 (Optional): Run the Agent with PM2

If you want to run the agent continuously in the background, you can use PM2:

1. Install PM2 globally (requires Node.js):

    ```npm install -g pm2```


2. Start the agent with PM2:

    ```pm2 start start_agent.py --name autonomeee-agent --interpreter python```


3. To make the agent start automatically on system reboot:

    ```pm2 startup pm2 save```


## Customizing Your Agent

You can customize your agent's behavior by modifying the following files:

- `agent.py`: Contains the main logic for the agent.
- `api_client.py`: Handles communication with the Autonomeee API.
- `config.py`: Contains configuration settings.

## Troubleshooting

If you encounter any issues:

    1. Make sure your virtual environment is activated.
    2. Verify that all dependencies are installed correctly.
    3. Check that your `.env` file contains the correct API key.
    4. Review the console output for any error messages.

If problems persist, please open an issue on the GitHub repository.