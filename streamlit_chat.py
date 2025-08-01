import streamlit as st
import uuid
import json
import time
from agent.router import SupportAgent
from pinecone import Pinecone
from openai import OpenAI
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY, PINECONE_FEEDBACK_NAMESPACE


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

if "openai_client" not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)

if "pinecone_index" not in st.session_state:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        from pinecone import ServerlessSpec, CloudProvider, AwsRegion, VectorType
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud=CloudProvider.AWS, region=AwsRegion.US_EAST_1),
            vector_type=VectorType.DENSE,
        )
    st.session_state.pinecone_index = pc.Index(PINECONE_INDEX_NAME)

# --- Streamlit App Title ---
st.set_page_config(page_title="Comfortside AI Agent", page_icon="🤖", layout="centered")
st.title("Comfortside AI Support.\nType your question below.")

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
                            "score": float(chunk.get("score", 0))
                        }
                    return context_dict

                raw_chunks = latest.get("context_chunks", [])
                context_dict = serialize_context_chunks(raw_chunks) if isinstance(raw_chunks, list) else {"empty": "chunks not searched or not found."}
                
                client = st.session_state.openai_client
                index = st.session_state.pinecone_index
                print("Pinecone index initialized")  # Debugging line
                # Generate embedding from feedback text
                embedding_text = f"{st.session_state.feedback_type}: {comment.strip()}"
                embedding_response = client.embeddings.create(
                    model="text-embedding-3-small",  # or any embedding model you prefer
                    input=[embedding_text]
                )
                vector = embedding_response.data[0].embedding
                print("Embedding generated")  # Debugging line
                # Create vector for Pinecone
                vector_id = str(uuid.uuid4())
                feedback_obj = {
                    "id": vector_id,
                    "values": vector,
                    "metadata": {
                        "user_prompt": latest.get("user"),
                        "assistant_response": latest.get("bot"),
                        "user_intent": latest.get("user_intent"),
                        "model_name": str(latest.get("model_name")),
                        "model_number": str(latest.get("model_number")),
                        "context_chunks": json.dumps(context_dict),
                        "comment": comment.strip(),
                        "feedback_type": st.session_state.feedback_type
                    },
                }
                print("Feedback object created")
                print(feedback_obj)
                # Upsert to Pinecone
                result = index.upsert(
                    vectors=[{
                        "id": feedback_obj["id"],
                        "values": feedback_obj["values"],
                        "metadata": feedback_obj["metadata"]
                    }],
                    namespace=PINECONE_FEEDBACK_NAMESPACE 
                )
                print("Upsert result:", result)
                print("Feedback upserted to Pinecone")
                st.success("✅ Feedback submitted!")
                st.session_state.feedback_submitted = True
                st.session_state.feedback_mode = False
                st.session_state.feedback_type = None
                st.session_state.comment = ""