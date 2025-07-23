from agent.router import SupportAgent

def chat():
    agent = SupportAgent()
    print("🔧 Comfortside Support Bot is online. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("\n💾 Saving conversation and exiting.")
                conversation = agent.export_conversation()
                # Optional: save to Pinecone or local file
                break

            response = agent.handle_input(user_input)
            print(f"Bot: {response}\n")

        except KeyboardInterrupt:
            print("\n🛑 Interrupted. Exiting.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue

if __name__ == "__main__":
    chat()