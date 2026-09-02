from typing import Any
from unittest.mock import AsyncMock

import pytest

from src.api.v1.vk.service import vk_service
from src.core.exceptions import ResourceNotFound


class FakeVKResponse:
    """Minimal stand-in for httpx.Response: VKService.gather only calls .json()."""

    def __init__(self, content: dict[str, Any]) -> None:
        self._content = content

    def json(self) -> dict[str, Any]:
        return self._content


def stub_vk_request(
    monkeypatch: pytest.MonkeyPatch, content: dict[str, Any],
) -> None:
    """vk_request already applied gather(), so method tests stub it with parsed content."""
    monkeypatch.setattr(
        vk_service, "vk_request", AsyncMock(return_value=content),
    )


@pytest.mark.asyncio
class TestGather:
    def test_error_body_raises_not_found(self) -> None:
        with pytest.raises(ResourceNotFound):
            vk_service.gather(FakeVKResponse({"error": {"error_code": 100}}))

    def test_normal_body_returned(self) -> None:
        content = {"response": []}

        assert vk_service.gather(FakeVKResponse(content)) == content


@pytest.mark.asyncio
class TestIsGroupReal:
    async def test_empty_response_is_false(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        stub_vk_request(monkeypatch, {"response": []})

        assert await vk_service.is_group_real("doesnotexist") is False

    async def test_existing_group_is_true(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        stub_vk_request(monkeypatch, {"response": [{"id": 1, "name": "habr"}]})

        assert await vk_service.is_group_real("habr") is True


@pytest.mark.asyncio
class TestGetGroupInfo:
    async def test_existing_group_returns_info(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        stub_vk_request(
            monkeypatch,
            {"response": [{"name": "habr", "photo_200": "https://vk/img.jpg"}]},
        )

        group = await vk_service.get_group_info("habr")
        assert group.name == "habr"
        assert group.photo_url == "https://vk/img.jpg"


@pytest.mark.asyncio
class TestGetPosts:
    async def test_parses_post_with_photo(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        stub_vk_request(
            monkeypatch,
            {
                "response": {
                    "items": [
                        {
                            "likes": {"count": 10},
                            "reposts": {"count": 2},
                            "views": {"count": 100},
                            "date": 1700000000,
                            "text": "hello",
                            "attachments": [
                                {
                                    "type": "photo",
                                    "photo": {
                                        "orig_photo": {"url": "https://vk/img.jpg"},
                                    },
                                },
                            ],
                        },
                    ],
                },
            },
        )

        posts = await vk_service.get_posts("habr", count=10, offset=0)
        assert len(posts) == 1
        post = posts[0]
        assert post.likes == 10
        assert post.reposts == 2
        assert post.views == 100
        assert post.timestamp == 1700000000
        assert post.is_pinned is False
        assert post.text == "hello"
        assert post.photos_url == ["https://vk/img.jpg"]
