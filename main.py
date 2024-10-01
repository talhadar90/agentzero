from agent import AutonomeeeAgent

def main():
    agent = AutonomeeeAgent()
    try:
        agent.run()
    except KeyboardInterrupt:
        print("Agent stopped by user.")

if __name__ == "__main__":
    main()
