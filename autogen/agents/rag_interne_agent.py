"""Agent AutoGen metier -- RAG interne via Azure AI Foundry."""

from __future__ import annotations

from typing import Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_core import CancellationToken

from autogen.config.foundry_config import call_foundry_generic, is_foundry_configured


class RagInterneAgent(BaseChatAgent):
    """Enrichit le contexte avec les documents internes via RAG.

    Delegue le travail a l agent Azure AI Foundry de RAG interne.
    Si Foundry n est pas configure, retourne un stub pedagogique.
    """

    def __init__(self) -> None:
        super().__init__(
            name="RagInterneAgent",
            description=(
                "Enrichit le contexte avec les documents internes "
                "via l agent Azure AI Foundry de RAG."
            ),
        )

    @property
    def produced_message_types(self) -> list[type]:
        return [TextMessage]

    async def on_messages(
        self,
        messages: Sequence[BaseChatMessage],
        cancellation_token: CancellationToken,
    ) -> Response:
        last_content = messages[-1].content if messages else ""

        if is_foundry_configured("rag_interne"):
            try:
                result = call_foundry_generic("rag_interne", last_content)
            except Exception as exc:
                result = (
                    "[FALLBACK RagInterne] Foundry indisponible ("
                    + str(exc)[:100]
                    + "), mode stub: "
                    + last_content[:200]
                )
        else:
            result = (
                "[STUB RagInterne] Documents internes pertinents pour: "
                + last_content[:200]
            )

        return Response(chat_message=TextMessage(content=result, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass