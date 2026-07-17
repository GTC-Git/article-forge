"""Provider interface: the contract every LLM provider must fulfill."""

from abc import ABC, abstractmethod


class Provider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Send a prompt to the LLM and return its text response."""
        ...