from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI


@dataclass
class LLMResponse:
    text: str
    mode: str


class BaseLLMProvider:
    def generate(self, question: str, prompt: str, context_chunks: list[dict]) -> LLMResponse:
        raise NotImplementedError


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question: str, prompt: str, context_chunks: list[dict]) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Answer only from the provided context. If the context is insufficient, say the answer was not found in the documents.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        text = response.choices[0].message.content or "The answer was not found in the documents."
        return LLMResponse(text=text.strip(), mode="openai")


class MockLLMProvider(BaseLLMProvider):
    def generate(self, question: str, prompt: str, context_chunks: list[dict]) -> LLMResponse:
        if not context_chunks:
            return LLMResponse(
                text="Demo mode: the answer was not found in the uploaded documents.",
                mode="mock",
            )

        snippets = []
        for chunk in context_chunks[:3]:
            snippets.append(f"[{chunk['source']}] {chunk['text'][:220].strip()}")

        response = (
            "Demo mode response based only on retrieved document context.\n\n"
            f"Question: {question}\n\n"
            "Relevant evidence summary:\n"
            + "\n".join(f"- {snippet}" for snippet in snippets)
        )
        return LLMResponse(text=response, mode="mock")


def create_llm_provider(api_key: str, model: str) -> BaseLLMProvider:
    if api_key:
        return OpenAIProvider(api_key=api_key, model=model)
    return MockLLMProvider()

