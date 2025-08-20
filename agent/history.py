from typing import List, Dict, Optional, Any

class ChatHistory:
    def __init__(self):
        self.turns: List[Dict] = []

    def add_turn(
        self,
        user: str,
        bot: str,
        # user_intent: str,
        context_chunks: Optional[List[Dict]] = None,
        model_name: Optional[str] = None,
        model_number: Optional[str] = None,
        tool_call: Optional[Dict[str, Any]] = None,  # New: Tool name + args + output
        response_type: str = "direct",  # e.g., "direct", "tool_call", "fallback"
    ):
        self.turns.append({
            "user": user,
            "bot": bot,
            # "user_intent": user_intent,
            "context_chunks": context_chunks,
            "model_name": model_name,
            "model_number": model_number,
            "tool_call": tool_call,
            "response_type": response_type,
        })

    def get_recent_turns(self, limit: int = 3) -> List[Dict]:
        return self.turns[-limit:]

    def get_all_turns(self) -> List[Dict]:
        return self.turns
    
    def get_as_openai_format(self, limit: int = 3) -> List[Dict[str, str]]:
        """
        Returns the last `limit` turns in OpenAI chat format.
        """
        messages = []
        for turn in self.turns[-limit:]:
            if turn["user"]:
                messages.append({"role": "user", "content": turn["user"]})
            if turn["bot"]:
                messages.append({"role": "assistant", "content": turn["bot"]})
        return messages