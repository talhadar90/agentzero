from src.agent import AutoActAutonomousAgent

def main():
    agent = AutoActAutonomousAgent()
    result = agent.run()
    print("AgentZero Result:")
    print(result)

if __name__ == "__main__":
    main()
