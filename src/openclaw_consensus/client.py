"""HTTP client wrapper around the OpenClaw Consensus RapidAPI endpoint."""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_BASE_URL = os.environ.get(
    "OPENCLAW_BASE_URL",
    "https://openclaw-consensus.p.rapidapi.com",
)
DEFAULT_HOST = os.environ.get(
    "OPENCLAW_RAPIDAPI_HOST",
    "openclaw-consensus.p.rapidapi.com",
)
DEFAULT_TIMEOUT = float(os.environ.get("OPENCLAW_TIMEOUT", "60"))


class OpenClawError(RuntimeError):
    """Raised when the upstream OpenClaw API returns a non-2xx response."""


class OpenClawClient:
    """Tiny async wrapper around the OpenClaw Consensus REST API.

    Reads ``RAPIDAPI_KEY`` from the environment. The endpoints called here
    are the public RapidAPI listing for OpenClaw Consensus; if you self-host
    the gateway, set ``OPENCLAW_BASE_URL`` to your own URL and leave
    ``RAPIDAPI_KEY`` unset (the host header will still be sent but ignored).
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        host: str = DEFAULT_HOST,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.host = host
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        h = {
            "Content-Type": "application/json",
            "X-RapidAPI-Host": self.host,
        }
        if self.api_key:
            h["X-RapidAPI-Key"] = self.api_key
        return h

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout) as c:
            r = await c.post(url, json=payload, headers=self._headers())
        if r.status_code // 100 != 2:
            raise OpenClawError(
                f"OpenClaw {path} returned {r.status_code}: {r.text[:300]}"
            )
        return r.json()

    @staticmethod
    def _mode_to_models(mode: str) -> int:
        return {"fast": 3, "balanced": 5, "deep": 9}.get(mode.lower(), 5)

    async def consensus(self, prompt: str, mode: str = "balanced") -> dict[str, Any]:
        return await self._post(
            "/v1/consensus",
            {"question": prompt, "max_models": self._mode_to_models(mode)},
        )

    async def disagreement(self, prompt: str) -> dict[str, Any]:
        # Compute disagreement = 1 - confidence from a deep consensus call
        data = await self._post(
            "/v1/consensus", {"question": prompt, "max_models": 9}
        )
        confidence = float(data.get("confidence", 0.0))
        return {
            "disagreement": round(1.0 - confidence, 3),
            "confidence": confidence,
            "models_responded": data.get("models_responded", 0),
            "votes": data.get("votes", []),
        }

    async def cheapest_route(
        self, prompt: str, target_quality: float = 0.85
    ) -> dict[str, Any]:
        # Heuristic: try fast first, escalate to balanced/deep until confidence >= target
        for mode in ("fast", "balanced", "deep"):
            data = await self._post(
                "/v1/consensus",
                {"question": prompt, "max_models": self._mode_to_models(mode)},
            )
            if float(data.get("confidence", 0.0)) >= target_quality:
                return {
                    "selected_mode": mode,
                    "models_used": self._mode_to_models(mode),
                    "confidence": data.get("confidence"),
                    "answer": data.get("consensus") or data.get("answer"),
                }
        return {
            "selected_mode": "deep",
            "models_used": 9,
            "confidence": data.get("confidence"),
            "answer": data.get("consensus") or data.get("answer"),
            "note": f"target_quality {target_quality} not reached; deep returned",
        }
