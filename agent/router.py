import json
from typing import Optional
from openai import OpenAI
from utils.schema import build_filters
from retriever.pinecone_retriever import retrieve_relevant_chunks
from utils.query_analysis import analyze_query
from agent.history import ChatHistory
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

# Tool function definition
def query_product_info(question: str, model_name: Optional[str] = None, model_number: Optional[str] = None) -> dict:
    filters = build_filters(model_name=model_name, model_number=model_number)
    chunks = retrieve_relevant_chunks(question, filters)

    contents = [chunk.metadata.get("content", "") for chunk in chunks]
    final_answer = "\n\n".join(contents)

    return {
        "final_answer": final_answer,
        "context_chunks": [chunk for chunk in chunks]  # For logging or auditing
    }

# OpenAI tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_product_info",
            "description": "Search technical documentation and manuals for the given question",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The user's support question"},
                    "model_name": {"type": "string", "description": "The name of the product model"},
                    "model_number": {"type": "string", "description": "The number of the product model"}
                },
                "required": ["question"]
            }
        }
    }
]

class SupportAgent:
    def __init__(self):
        self.history = ChatHistory()

    def handle_input(self, user_input: str) -> str:
        # Step 1: Analyze the query and memory
        analysis = analyze_query(user_input, self.history.get_all_turns())
        intent = analysis["intent"]
        model_name = analysis["model_name"]
        model_number = analysis["model_number"]

        # Step 2: Get conversation so far (OpenAI format)
        messages = self.history.get_as_openai_format()
        messages.append({"role": "user", "content": user_input})

        # Step 3: Run OpenAI model with tool calling
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Defaults
        final_message = message.content
        response_type = "text"
        tool_call = None
        context_chunks = None

        # Step 4: Check if tool was called
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            if tool_call.function.name == "query_product_info":
                args = json.loads(tool_call.function.arguments)
                tool_result = query_product_info(**args)
                context_chunks = tool_result.get("context_chunks", [])
                final_answer = tool_result.get("final_answer", None)
                
                # Step 5: Use tool output to continue conversation
                followup_response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages + [
                        message,
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": "query_product_info",
                            "content": final_answer
                        }
                    ]
                )
                final_message = followup_response.choices[0].message.content
                response_type = "tool_call"
            else:
                final_message = "Sorry, I couldn't handle that request."

        # Step 6: Save turn to history
        self.history.add_turn(
            user=user_input,
            bot=final_message,
            user_intent=intent,
            model_name=model_name,
            model_number=model_number,
            response_type=response_type,
            tool_call=tool_call,
            context_chunks=context_chunks
        )

        return final_message

    def export_conversation(self):
        return self.history.get_all_turns()