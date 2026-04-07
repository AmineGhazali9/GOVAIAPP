# tests/test_ui_smoke.py â€” tests smoke UI Streamlit GOVAIAPP
import importlib
import sys
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest


def _mock_streamlit() -> MagicMock:
    mock_st = MagicMock()

    # form() doit fonctionner comme context manager
    mock_st.form.return_value.__enter__ = MagicMock(return_value=None)
    mock_st.form.return_value.__exit__ = MagicMock(return_value=False)

    # Important: Ã©viter l'appel API pendant l'import
    mock_st.form_submit_button.return_value = False

    # Valeurs UI "propres" (JSON-serializable)
    mock_st.text_input.return_value = ""
    mock_st.text_area.return_value = ""
    mock_st.selectbox.return_value = "debutant"

    # spinner context manager (optionnel)
    mock_st.spinner.return_value.__enter__ = MagicMock(return_value=None)
    mock_st.spinner.return_value.__exit__ = MagicMock(return_value=False)

    return mock_st


@pytest.fixture(autouse=True)
def patch_streamlit():
    """Patch streamlit pour tous les tests de ce fichier."""
    mock_st = _mock_streamlit()
    with patch.dict("sys.modules", {"streamlit": mock_st}):
        sys.modules.pop("app.ui.app", None)
        yield mock_st
    sys.modules.pop("app.ui.app", None)


# â”€â”€ Import â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_ui_module_imports() -> None:
    """Le module app.ui.app doit s'importer sans erreur (sans Streamlit runtime)."""
    importlib.import_module("app.ui.app")


# â”€â”€ parse_principes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def test_parse_principes_normal() -> None:
    """parse_principes doit splitter les lignes non vides."""
    mod = importlib.import_module("app.ui.app")
    result = mod.parse_principes("Transparence\nResponsabilitÃ©\n\nÃ‰quitÃ©\n")
    assert result == ["Transparence", "ResponsabilitÃ©", "Ã‰quitÃ©"]


def test_parse_principes_empty() -> None:
    """parse_principes sur chaÃ®ne vide doit retourner une liste vide."""
    mod = importlib.import_module("app.ui.app")
    assert mod.parse_principes("") == []
    assert mod.parse_principes("   \n  \n") == []


def test_parse_principes_strips_whitespace() -> None:
    """parse_principes doit ignorer les espaces en dÃ©but/fin de ligne."""
    mod = importlib.import_module("app.ui.app")
    result = mod.parse_principes("  Ã‰quitÃ©  \n  Inclusion ")
    assert result == ["Ã‰quitÃ©", "Inclusion"]


# â”€â”€ call_generate_policy â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _make_mock_response(json_data: dict[str, Any], status_code: int = 200) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = json_data
    mock_resp.status_code = status_code
    return mock_resp


def test_call_generate_policy_success() -> None:
    """call_generate_policy retourne le JSON en cas de succÃ¨s."""
    mod = importlib.import_module("app.ui.app")
    expected = {"policy_markdown": "# Test", "sources": []}
    mock_resp = _make_mock_response(expected)

    with patch("httpx.post", return_value=mock_resp) as mock_post:
        result = mod.call_generate_policy({"nom": "X"}, base_url="http://testserver")
        mock_post.assert_called_once_with(
            "http://testserver/generate-policy", json={"nom": "X"}, timeout=60
        )
        mock_resp.raise_for_status.assert_called_once()

    assert result == expected


def test_call_generate_policy_propagates_connect_error() -> None:
    """call_generate_policy propage ConnectError sans la swallow."""
    mod = importlib.import_module("app.ui.app")
    with patch("httpx.post", side_effect=httpx.ConnectError("refused")):
        with pytest.raises(httpx.ConnectError):
            mod.call_generate_policy({"nom": "X"}, base_url="http://testserver")


def test_call_generate_policy_propagates_timeout() -> None:
    """call_generate_policy propage TimeoutException."""
    mod = importlib.import_module("app.ui.app")
    with patch("httpx.post", side_effect=httpx.TimeoutException("timeout")):
        with pytest.raises(httpx.TimeoutException):
            mod.call_generate_policy({"nom": "X"}, base_url="http://testserver")


def test_call_generate_policy_propagates_http_status_error() -> None:
    """call_generate_policy propage HTTPStatusError via raise_for_status."""
    mod = importlib.import_module("app.ui.app")
    mock_resp = _make_mock_response({}, status_code=500)
    mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500", request=MagicMock(), response=MagicMock(status_code=500)
    )
    with patch("httpx.post", return_value=mock_resp):
        with pytest.raises(httpx.HTTPStatusError):
            mod.call_generate_policy({"nom": "X"}, base_url="http://testserver")
