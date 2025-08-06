
import json
from typing import Optional
from agent.history import ChatHistory
from utils.query_analysis import analyze_query
from utils.schema import build_filters
from retriever.pinecone_retriever import retrieve_relevant_chunks
from config import SYSTEM_PROMPT
from llm.openai_chain import call_openai_with_tools, followup_with_tool_response
from agent.tools.product_info import query_product_info


class SupportAgent:
    def __init__(self):
        self.history = ChatHistory()

    def handle_input(self, user_input: str) -> str:
        analysis = analyze_query(user_input, self.history.get_all_turns())
        intent = analysis["intent"]
        model_name = analysis["model_name"]
        model_number = analysis["model_number"]

        system_prompt = {"role": "system", "content": SYSTEM_PROMPT}
        messages = [system_prompt] + self.history.get_as_openai_format()
        messages.append({"role": "user", "content": user_input})

        message = call_openai_with_tools(messages)
        response_type = "text"
        context_chunks = []
        final_message = message.content
        tool_calls = message.tool_calls
        print(f"Tool calls detected: {tool_calls}")
        if tool_calls:
            tool_messages = []
            tool_results_combined = ""

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                if tool_name == "query_product_info":
                    tool_result = query_product_info(**tool_args)
                    chunks = tool_result.get("context_chunks", [])
                    answer = tool_result.get("final_answer", "")

                    # Track all chunks for this turn
                    context_chunks.extend(chunks)

                    # Save tool output message
                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": answer
                    })

                    tool_results_combined += f"\n\n{answer}"
                else:
                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Tool '{tool_name}' is not implemented."
                    })

            # Add assistant message that triggered tool(s)
            messages.append(message)

            # Add all tool responses
            messages.extend(tool_messages)

            # Get final assistant message using tool outputs
            final_response = followup_with_tool_response(
                prior_messages=messages[:-len(tool_messages)],
                tool_messages=tool_messages
            )
            final_message = final_response
            response_type = "tool_call"

        # Save conversation history
        self.history.add_turn(
            user=user_input,
            bot=final_message,
            user_intent=intent,
            model_name=model_name,
            model_number=model_number,
            response_type=response_type,
            tool_call=tool_calls,  # this is now a list
            context_chunks=context_chunks
        )

        return final_message

    def export_conversation(self):
        return self.history.get_all_turns()




