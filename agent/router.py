
import json
from agent.history import ChatHistory
from utils.query_analysis import analyze_query
from config import SYSTEM_PROMPT
from llm.openai_chain import call_openai_with_tools, followup_with_tool_response
from agent.tools.product_info import query_product_info
from agent.tools.warranty_info import query_warranty_info
from agent.tools.troubleshooting_info import query_errorcode_info

class SupportAgent:
    def __init__(self):
        self.history = ChatHistory()

    def handle_input(self, user_input: str) -> str:
        analysis = analyze_query(user_input, self.history.get_all_turns())

        system_prompt = {"role": "system", "content": SYSTEM_PROMPT}
        messages = [system_prompt] + self.history.get_as_openai_format()
        messages.append({"role": "user", "content": user_input})

        # Call the model with tools enabled, get initial response with tool_calls
        message = call_openai_with_tools(messages)

        tool_calls = getattr(message, "tool_calls", None) 
        print(f"Tool calls detected: {tool_calls}")

        final_message = message.content
        response_type = "text"
        context_chunks = []

        if tool_calls:
            tool_messages = []
            tool_results_combined = ""

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                if tool_name == "query_product_info":
                    tool_result = query_product_info(**tool_args)
                elif tool_name == "query_warranty_info":
                    tool_result = query_warranty_info(**tool_args)
                elif tool_name == "query_errorcode_info":
                    tool_result = query_errorcode_info(**tool_args)
                else:
                    tool_result = {
                        "final_answer": f"Tool '{tool_name}' is not implemented.",
                        "context_chunks": []
                    }

                chunks = tool_result.get("context_chunks", [])
                answer = tool_result.get("final_answer", "")

                context_chunks.extend(chunks)

                tool_messages.append({
                    "role": "tool",
                    "name": tool_name,             # <-- IMPORTANT: include "name"
                    "tool_call_id": tool_call.id,  # <-- IMPORTANT: include tool_call_id
                    "content": answer
                })

                tool_results_combined += f"\n\n{answer}"

            # Build the assistant message with tool_calls explicitly
            tool_call_message = {
                "role": "assistant",
                "content": None,
                "tool_calls": tool_calls  # must be full list or single tool_call object
            }

            # Compose messages for follow-up completion call
            followup_prior = messages + [tool_call_message]

            # Call follow-up with tool responses appended
            final_response = followup_with_tool_response(
                prior_messages=followup_prior,
                tool_messages=tool_messages
            )

            final_message = final_response
            response_type = "tool_call"

        # Save conversation history with all relevant info
        self.history.add_turn(
            user=user_input,
            bot=final_message,
            user_intent=analysis["intent"],
            model_name=analysis["model_name"],
            model_number=analysis["model_number"],
            response_type=response_type,
            tool_call=tool_calls,
            context_chunks=context_chunks
        )

        return final_message

    def export_conversation(self):
        return self.history.get_all_turns()




