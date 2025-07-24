from fastapi import FastAPI
from pydantic import BaseModel
from agent.fastapi_router import SupportAgent

app = FastAPI()
agent = SupportAgent()

class ChatRequest(BaseModel):
    user_input: str
    session_id: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    reply = agent.handle_input(req.user_input, session_id=req.session_id)
    return {"response": reply}