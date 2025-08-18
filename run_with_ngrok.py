import time
import threading
import uvicorn
from pyngrok import ngrok
from config import NGROK_API_KEY
# Import your FastAPI app
from fastapi_app.main import app  # Adjust if your FastAPI app is in a different file
 
# Config
LOCAL_PORT = 8000
NGROK_AUTH_TOKEN = NGROK_API_KEY  # Optional, for persistent tunnels

# -----------------------------
# Start FastAPI server in thread
# -----------------------------
def run_server():
    uvicorn.run("fastapi_app.main:app", host="0.0.0.0", port=LOCAL_PORT, reload=False)

# -----------------------------
# Start ngrok tunnel
# -----------------------------
def start_ngrok():
    if NGROK_AUTH_TOKEN:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    public_url = ngrok.connect(LOCAL_PORT, bind_tls=True)
    print(f"Public ngrok URL: {public_url}")
    return public_url

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    # Start FastAPI in a background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait a moment to let FastAPI start
    time.sleep(2)

    # Start ngrok tunnel
    public_url = start_ngrok()

    # Print instructions for your webhook provider
    print("\n🔔 Set this as your webhook URL:")
    print(f"{public_url}/webhook\n")  # Adjust path to your endpoint

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.kill()