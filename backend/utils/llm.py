"""
Thin wrapper around Groq so every agent calls one place.
Swap this file later if you move to Azure OpenAI / OpenAI — nothing else changes.
"""
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def call_llm(system_prompt: str, user_prompt: str, json_mode: bool = False, temperature: float = 0.3) -> str:
    """Single LLM call. Returns raw text (or JSON string if json_mode=True)."""
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = _client.chat.completions.create(
        model=_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )
    return response.choices[0].message.content


def call_llm_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict:
    """Call LLM and parse JSON output safely, with one retry on failure."""
    raw = call_llm(system_prompt, user_prompt, json_mode=True, temperature=temperature)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # strip markdown fences if the model added them anyway
        cleaned = raw.strip().strip("`").replace("json\n", "", 1)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"error": "failed_to_parse", "raw": raw}
