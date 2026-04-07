"""Agent AutoGen metier -- veille externe via Azure AI Foundry."""

from __future__ import annotations

from typing import Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response
from autogen_agentchat.messages import BaseChatMessage, TextMessage
from autogen_core import CancellationToken

from autogen.config.foundry_config import call_foundry_generic, is_foundry_configured


class VeilleExterneAgent(BaseChatAgent):
    """Collecte les signaux reglementaires et normatifs externes.

    Delegue le travail a l agent Azure AI Foundry de veille externe.
    Si Foundry n est pas configure, retourne un stub pedagogique.
    """

    def __init__(self) -> None:
        super().__init__(
            name="VeilleExterneAgent",
            description=(
                "Collecte les signaux reglementaires et normatifs externes "
                "via l agent Azure AI Foundry de veille."
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

        if is_foundry_configured("veille_externe"):
            try:
                result = call_foundry_generic("veille_externe", last_content)
            except Exception as exc:
                result = (
                    "[FALLBACK VeilleExterne] Foundry indisponible ("
                    + str(exc)[:100]
                    + "), mode stub: "
                    + last_content[:200]
                )
        else:
            result = (
                "[STUB VeilleExterne] Signaux reglementaires identifies pour: "
                + last_content[:200]
            )

        return Response(chat_message=TextMessage(content=result, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass