import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class AIAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-6-luna"
        )

    def analyze(self, code: str, language: str):
        prompt = f"""
        You are an expert software code reviewer.

        Analyze the following {language} code.

        Look for:
        - Security vulnerabilities
        - Bugs and correctness problems
        - Code quality problems
        - Maintainability problems
        - Performance problems
        - Bad practices

        Return ONLY valid JSON in this exact structure:

        {{
        "score": 0,
        "summary": "short overall assessment",
        "issues": [
            {{
            "severity": "HIGH",
            "category": "Security",
            "line": 1,
            "message": "What is wrong",
            "suggestion": "How to improve it"
            }}
        ]
        }}

        Rules:
        - score must be an integer from 0 to 10
        - severity must be HIGH, MEDIUM, or LOW
        - line must be the relevant line number or null
        - category should be concise
        - Do not invent issues
        - If there are no issues, return an empty issues array
        - Keep the summary concise

        CODE:

        ```{language}
        {code}"""
        response = self.client.responses.create(
        model=self.model,
        input=prompt
    )

        text = response.output_text

        try:
            result = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "AI returned invalid JSON."
            ) from exc

        return result