from typing import Optional
from utils.query_analysis import analyze_query
from retriever.pinecone_retriever import retrieve_relevant_chunks
from llm.openai_chain import generate_response
from utils.schema import build_filters
from agent.history import ChatHistory
import time

class SupportAgent:
    def __init__(self):
        self.history = ChatHistory()

    def handle_input(self, user_input: str) -> str:
        # Step 1: Analyze the query and memory
        query_info = analyze_query(user_input, self.history.get_recent_turns())
        
        intent = query_info["intent"]
        model_name = query_info["model_name"]
        model_number = query_info["model_number"]
        # Step 2: Decide if RAG is required
        use_rag = intent in {"follow_up_question", "support_question"} and bool(model_name or model_number)        
        
        if intent == "social_interaction":
            context_chunks = "Respond as a friendly assistant. This is a social message, not a support question."
            response = generate_response(user_input, context_chunks)
        elif intent == "unknown":
            context_chunks = "The user provided no or insufficient information to query the database. Tell the user to provide a detailed request."
            if model_name:
                context_chunks += f" The user mentioned the model: {model_name}."
            if model_number:
                context_chunks += f" The user mentioned the model number: {model_number}."
            response = generate_response(user_input, context_chunks)
        elif use_rag:
            # Step 3: Build filters
            filters = build_filters(
                model_name=model_name,
                model_number=model_number,
            )
            # Step 4: Retrieve documents if needed
            context_chunks = retrieve_relevant_chunks(user_input, filters)
            contents = [chunk.metadata.get("content", "") for chunk in context_chunks]

            # Step 5: Generate response
            response = generate_response(user_input, contents)
            print(f"Search parameters:\nIntent: {intent}\nFilters: {filters}\nContext Chunks: {context_chunks}\n")
        else:
            # Fallback if intent is known but RAG isn't applicable (e.g., missing model info)
            context_chunks = "The request could not be answered due to missing model name or number. Please specify one."
            response = generate_response(user_input, context_chunks)
            print("elsed.")
        # Step 6: Save turn to memory
        self.history.add_turn(
            user=user_input,
            bot=response,
            context_chunks=context_chunks,
            user_intent=intent,
            model_name=model_name,
            model_number=model_number,
        )

        return response

    def export_conversation(self):
        """
        You could use this to push the session to Pinecone as a long-term memory,
        or save it to disk if you prefer.
        """
        return self.history.get_all_turns()
    