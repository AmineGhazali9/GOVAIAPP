"""Agent AutoGen metier -- producteur de politique via Azure AI Foundry."""

from __future__ import annotations

from typing import Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_core import CancellationToken

from autogen.config.foundry_config import call_foundry_generic, is_foundry_configured


class ProducteurPolitiqueAgent(BaseChatAgent):
    """Produit la politique de gouvernance IA finale.

    Delegue le travail a l agent Azure AI Foundry producteur de politique.
    Si Foundry n est pas configure, retourne un stub pedagogique.
    """

    def __init__(self) -> None:
        super().__init__(
            name="ProducteurPolitiqueAgent",
            description=(
                "Produit la politique de gouvernance IA finale "
                "via l agent Azure AI Foundry producteur."
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

        if is_foundry_configured("producteur_politique"):
            try:
                result = call_foundry_generic("producteur_politique", last_content)
            except Exception as exc:
                result = (
                    "[FALLBACK ProducteurPolitique] Foundry indisponible ("
                    + str(exc)[:100]
                    + "), mode stub: "
                    + last_content[:200]
                )
        else:
            result = (
                "[STUB ProducteurPolitique] Politique generee pour: "
                + last_content[:200]
            )

        return Response(chat_message=TextMessage(content=result, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass