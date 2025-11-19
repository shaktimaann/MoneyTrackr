"""Lightweight CrewAI local package implementing agents and a Crew binding.

This small package provides:
- LLMAgent: wrapper around Google Gemini (using `google-genai` style import)
- NumericAgent: performs numeric analysis without LLM
- Crew: register and run tasks by name

It is implemented locally so the project is self-contained and ready to wire into the Streamlit app.
"""
from .agents import LLMAgent, NumericAgent, Crew

__all__ = ["LLMAgent", "NumericAgent", "Crew"]
