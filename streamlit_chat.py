import streamlit as st
import uuid
import json
from agent.router import SupportAgent

# Initialize agent and session state
if "agent" not in st.session_state:
    st.session_state.agent = SupportAgent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "feedback_mode" not in st.session_state:
    st.session_state.feedback_mode = False
    st.session_state.feedback_type = None
    st.session_state.comment = ""

if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False

# --- Streamlit App Title ---
st.title("🔧 Comfortside Support Bot")

# --- Chat UI ---
user_input = st.chat_input("Ask a question about your unit...")
if user_input:
    with st.spinner("Thinking..."):
        response = st.session_state.agent.handle_input(user_input)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        # Reset feedback state for new turn
        st.session_state.feedback_mode = False
        st.session_state.feedback_type = None
        st.session_state.comment = ""
        st.session_state.feedback_submitted = False
# --- Display Chat History ---
for i, turn in enumerate(st.session_state.chat_history):
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn["bot"])
        # Only show feedback buttons for the most recent bot response
        if i == len(st.session_state.chat_history) - 1 and not st.session_state.feedback_mode:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key="thumbs_up"):
                    st.session_state.feedback_mode = True
                    st.session_state.feedback_type = "thumbs_up"
            with col2:
                if st.button("👎", key="thumbs_down"):
                    st.session_state.feedback_mode = True
                    st.session_state.feedback_type = "thumbs_down"

# --- Feedback Box ---
# --- Feedback Box ---
if st.session_state.feedback_mode and not st.session_state.feedback_submitted:
    with st.form("feedback_form", clear_on_submit=True):
        st.write("**Leave a comment about this response:**")
        comment = st.text_area("Comment", value=st.session_state.comment)
        submitted = st.form_submit_button("SEND")
        if submitted:
            if comment.strip() == "":
                st.warning("Comment cannot be empty.")
            else:
                recent_turns = st.session_state.agent.history.get_recent_turns()
                latest = recent_turns[-1] if recent_turns else {}

                def serialize_context_chunks(chunks):
                    context_dict = {}
                    for i, chunk in enumerate(chunks):
                        context_dict[f"chunk{i+1}"] = {
                            "id": chunk["id"],
                            "score": float(chunk.get("score", 0)),
                            "metadata": chunk.get("metadata", {}),
                            "values": list(chunk.get("values", []))
                        }
                    return context_dict

                raw_chunks = latest.get("context_chunks", [])
                context_dict = serialize_context_chunks(raw_chunks) if isinstance(raw_chunks, list) else {"empty": "chunks not searched or not found."}

                feedback_obj = {
                    "id": str(uuid.uuid4()),
                    "embedding": f"{st.session_state.feedback_type} | {comment.strip()}",
                    "metadata": {
                        "user_prompt": latest.get("user"),
                        "assistant_response": latest.get("bot"),
                        "user_intent": latest.get("user_intent"),
                        "model_name": latest.get("model_name"),
                        "model_number": latest.get("model_number"),
                        "context_chunks": context_dict,
                    },
                }

                with open("feedback_log.jsonl", "a") as f:
                    f.write(json.dumps(feedback_obj) + "\n")

                st.success("✅ Feedback submitted!")
                st.session_state.feedback_submitted = True
                st.session_state.feedback_mode = False
                st.session_state.feedback_type = None
                st.session_state.comment = ""