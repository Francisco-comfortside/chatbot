from typing import List, Dict, Optional

class ChatHistory:
    def __init__(self):
        self.turns: List[Dict] = []

    def add_turn(
        self,
        user: str,
        bot: str,
        user_intent: str,
        model_name: Optional[str] = None,
        model_number: Optional[str] = None,
        # error_code: Optional[str] = None
    ):
        self.turns.append({
            "user": user,
            "bot": bot,
            "user_intent": user_intent,
            "model_name": model_name,
            "model_number": model_number,
            # "error_code": error_code
        })

    def get_recent_turns(self, limit: int = 5) -> List[Dict]:
        return self.turns[-limit:]

    def get_all_turns(self) -> List[Dict]:
        return self.turns