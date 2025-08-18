import streamlit as st
import uuid
import json
import time
from agent.router import SupportAgent
from pinecone import Pinecone
from openai import OpenAI
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY, PINECONE_FEEDBACK_NAMESPACE, STREAMLIT_PASSWORD, GMAIL_APP_PASSWORD
import smtplib
from email.message import EmailMessage
from voice.voice_recognition import VoiceHandler
import io

# --- Password Gate ---
def check_password():
    def password_entered():
        if st.session_state["password"] == STREAMLIT_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Optional: clear password after auth
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("Enter password:", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect password")
        st.stop()

check_password()  # 🛑 Prevent rest of the app from loading if password is wrong

def write_email(body):
    # Prepare email content
    sender = "francisco.pages2025@gmail.com"
    receiver = "francisco.pages@comfortside.com"
    subject = "Comfortside AI Agent Feedback"

    #create email message
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    return msg

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
st.title("Comfortside AI Support.\nType your question below.\n\n")

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

# audio_input = st.audio_input("🎤", label_visibility="collapsed")
# if audio_input:
#     voice = VoiceHandler()
#     audio_bytes = audio_input.read()  # get bytes
#     text_input = voice.transcribe_audio(audio_bytes)
#     with st.spinner("Thinking..."):
#         response = st.session_state.agent.handle_input(text_input)
#         st.session_state.chat_history.append({"user": text_input, "bot": response})
#         # Reset feedback state for new turn
#         st.session_state.feedback_mode = False
#         st.session_state.feedback_type = None
#         st.session_state.comment = ""
#         st.session_state.feedback_submitted = False

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
                st.text("Pretty good!")
            with col2:
                if st.button("👎", key="thumbs_down"):
                    st.session_state.feedback_mode = True
                    st.session_state.feedback_type = "thumbs_down"
                st.text("Needs work.")



# # --- Chat UI ---
# # Place text input and file uploader side by side
# col1, col2 = st.columns([4, 1])
# with col1:
#     text_input = st.chat_input("Ask a question about your unit...", key="chat_input")
# with col2:
#     audio_input = st.audio_input("🎤", label_visibility="collapsed")


# --- Feedback Box ---
if st.session_state.feedback_mode:
    with st.spinner("Please wait. Sending feedback..."):
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

        embedding_text = f"{st.session_state.feedback_type}: {latest.get('user')}"
        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[embedding_text]
        )
        vector = embedding_response.data[0].embedding

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
                "feedback_type": st.session_state.feedback_type
            },
        }

        result = index.upsert(
            vectors=[{
                "id": feedback_obj["id"],
                "values": feedback_obj["values"],
                "metadata": feedback_obj["metadata"]
            }],
            namespace=PINECONE_FEEDBACK_NAMESPACE 
        )

        msg = write_email(
            f"ID: {feedback_obj['id']}\nFeedback Type: {st.session_state.feedback_type}\n\nUser Prompt:\n{latest.get('user')}\n\nAssistant Response:\n{latest.get('bot')}"
        )
        sender = "francisco.pages2025@gmail.com"
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        st.success("✅ Feedback submitted!")
        st.session_state.feedback_submitted = True
        st.session_state.feedback_mode = False
        st.session_state.feedback_type = None
        st.session_state.comment = ""