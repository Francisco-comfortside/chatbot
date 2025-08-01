from typing import List, Dict, Optional

class ChatHistory:
    def __init__(self):
        self.turns: List[Dict] = []

    def add_turn(
        self,
        user: str,
        bot: str,
        user_intent: str,
        context_chunks: Optional[list[Dict]] = None,
        model_name: Optional[str] = None,
        model_number: Optional[str] = None,
    ):
        self.turns.append({
            "user": user,
            "bot": bot,
            "context_chunks": context_chunks,
            "user_intent": user_intent,
            "model_name": model_name,
            "model_number": model_number,
        })

    def get_recent_turns(self, limit: int = 5) -> List[Dict]:
        return self.turns[-limit:]

    def get_all_turns(self) -> List[Dict]:
        return self.turns