from fastapi import FastAPI, Request
from agent.router import SupportAgent

app = FastAPI()
agent = SupportAgent()

from fastapi import FastAPI, Request
from agent.router import SupportAgent

app = FastAPI()
agent = SupportAgent()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()  # Entire incoming JSON
    payload = data.get("payload", {})

    # Choose which field to pass to handle_input
    user_input = payload.get("query")  # or "user_message" depending on your workflow

    if not user_input:
        return {
            "result": {
                "success": False,
                "context": ""
            },
            "agent_message": "No query found in payload."
        }


    # Pass input to your agent
    response = agent.handle_input(user_input)

    # Return the agent's response
    return {
        "result": {
            "success": True,
            "context": response
        },
        "agent_message": ""
    }