from agent.router import SupportAgent
import time


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
            start_time = time.time()
            response = agent.handle_input(user_input)
            elapsed_time = time.time() - start_time
            print(f"Bot: {response}\n")
            print(f"Total time: {elapsed_time:.2f} seconds\n")
        except KeyboardInterrupt:
            print("\n🛑 Interrupted. Exiting.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            continue

if __name__ == "__main__":
    chat()