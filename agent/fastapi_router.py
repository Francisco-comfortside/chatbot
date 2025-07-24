from typing import Optional
from utils.query_analysis import analyze_query
from retriever.pinecone_retriever import retrieve_relevant_chunks
from llm.openai_chain import generate_response
from utils.schema import build_filters
from agent.history import ChatHistory

class SupportAgent:
    def __init__(self):
        self.sessions = {}  # session_id: ChatHistory

    def handle_input(self, user_input: str, session_id: str = "default") -> str:
        # Step 0: Get or create chat history for this session
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatHistory()
        history = self.sessions[session_id]

        # Step 1: Analyze the query and memory
        query_info = analyze_query(user_input, history.get_recent_turns())

        intent = query_info["intent"]
        model_name = query_info["model_name"]
        model_number = query_info["model_number"]
        error_code = query_info["error_code"]

        # Step 2: Decide if RAG is required
        use_rag = intent == "support_question" and (
            error_code or model_name or model_number
        )

        if intent == "greeting":
            response = "Hi there! How can I assist you today?"
        elif intent == "unknown" or (not use_rag and not error_code):
            response = "Could you please tell me the model name or number so I can help you better?"
        else:
            # Step 3: Build filters
            filters = build_filters(
                model_name=model_name,
                model_number=model_number,
                error_code_only=bool(error_code and not model_name and not model_number)
            )

            # Step 4: Retrieve documents if needed
            context_chunks = retrieve_relevant_chunks(user_input, filters)

            # Step 5: Generate response
            response = generate_response(user_input, context_chunks)

        # Step 6: Save turn to session history
        history.add_turn(
            user=user_input,
            bot=response,
            model_name=model_name,
            model_number=model_number
        )

        return response

    def export_conversation(self, session_id: str = "default"):
        return self.sessions.get(session_id, ChatHistory()).get_all_turns()