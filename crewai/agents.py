import os
import json
from typing import Callable, Any, Dict
from dataclasses import dataclass

import pandas as pd

# Try to import Google's GenAI client in a permissive way.
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    load_dotenv()

    def _configure_genai():
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise EnvironmentError('GEMINI_API_KEY not set in environment')
        genai.configure(api_key=api_key)

    _configure_genai()
    GENAI_AVAILABLE = True
except Exception as e:
    genai = None
    GENAI_AVAILABLE = False


@dataclass
class LLMAgent:
    """Agent powered by Gemini LLM."""

    model: str = 'gemini-pro'

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if not GENAI_AVAILABLE:
            raise RuntimeError('google-genai (Gemini) client not available or GEMINI_API_KEY missing')

        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f'Gemini API error: {str(e)}')


class NumericAgent:
    """Agent that performs pure numeric analysis without an LLM."""

    def __init__(self, analysis_fn: Callable[[pd.DataFrame, float], Dict]):
        self.analysis_fn = analysis_fn

    def run(self, df: pd.DataFrame, balance: float) -> Dict:
        return self.analysis_fn(df, balance)


class Crew:
    """Simple crew orchestration: register tasks and run them."""

    def __init__(self):
        self._tasks = {}

    def register_task(self, name: str, func: Callable[..., Any]):
        self._tasks[name] = func

    def run_task(self, name: str, payload: Any = None) -> Any:
        if name not in self._tasks:
            raise KeyError(f'Task {name} not registered')
        fn = self._tasks[name]
        if payload is None:
            return fn()
        return fn(payload)
