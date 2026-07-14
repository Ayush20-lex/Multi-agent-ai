# agents/agent_base.py

from groq import Groq
from abc import ABC, abstractmethod
from loguru import logger
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AgentBase(ABC):
    def __init__(self, name, max_retries=3, verbose=True):
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_gemini(self, messages, temperature=0.7, max_tokens=150):
        """Call Groq API (method name kept as call_gemini for compatibility)."""
        retries = 0
        last_error = None
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Sending messages to Groq:")
                    for msg in messages:
                        logger.debug(f"  {msg['role']}: {msg['content']}")

                # Normalize messages: Groq expects string content, not list format
                normalized_messages = []
                for msg in messages:
                    role = msg["role"]
                    content = msg["content"]
                    if isinstance(content, list):
                        # Convert list format to plain string
                        text = " ".join(
                            part["text"] for part in content if part.get("type") == "text"
                        )
                    else:
                        text = content
                    normalized_messages.append({"role": role, "content": text})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=normalized_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                reply = response.choices[0].message.content
                if self.verbose:
                    logger.info(f"[{self.name}] Received response: {reply}")
                return reply
            except Exception as e:
                last_error = e
                retries += 1
                error_str = str(e)
                if "429" in error_str or "rate_limit" in error_str.lower():
                    wait_time = 30
                    logger.warning(f"[{self.name}] Rate limited. Waiting {wait_time}s before retry {retries}/{self.max_retries}...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"[{self.name}] Error during Groq call: {e}. Retry {retries}/{self.max_retries}")
                    time.sleep(2)

        raise Exception(f"[{self.name}] Failed to get response from Groq after {self.max_retries} retries. Last error: {last_error}")
