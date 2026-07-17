"""Mock provider: returns canned responses for pipeline validation at zero cost."""

from forge.providers.base import Provider


class MockProvider(Provider):
    """Fake LLM that echoes a deterministic response."""

    def complete(self, prompt: str) -> str:
        return f"[MOCK RESPONSE] prompt received ({len(prompt)} chars)"