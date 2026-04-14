"""API endpoint for Monopoly WhatsApp command parsing."""

import rest_framework as drf
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from core.services.monopoly_bot import parse_whatsapp_command


class MonopolyCommandView(drf.views.APIView):
    """Execute a Monopoly WhatsApp-like command and return the bot reply."""

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["monopoly"],
        request=inline_serializer(
            name="MonopolyCommandRequest",
            fields={
                "text": serializers.CharField(
                    required=True,
                    help_text="Commande texte Monopoly (ex: RUES, RUE paix, MULTI STATUS).",
                ),
            },
        ),
        responses={
            200: inline_serializer(
                name="MonopolyCommandResponse",
                fields={
                    "response": serializers.CharField(),
                },
            ),
            400: inline_serializer(
                name="MonopolyCommandErrorResponse",
                fields={
                    "detail": serializers.CharField(),
                },
            ),
        },
        description="Parse et exécute une commande Monopoly pour intégration WhatsApp/API.",
    )
    def post(self, request):
        """POST /api/v1.0/monopoly/command/ -> {'response': '...'}"""
        text = request.data.get("text")
        if text is None:
            return drf.response.Response(
                {"detail": "Le champ 'text' est requis."},
                status=drf.status.HTTP_400_BAD_REQUEST,
            )

        return drf.response.Response({"response": parse_whatsapp_command(str(text))})
