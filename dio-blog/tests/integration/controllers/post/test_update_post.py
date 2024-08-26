import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from src.schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create(PostIn(title="post 1", content="some content", published=True))
    await service.create(PostIn(title="post 2", content="some content", published=True))
    await service.create(PostIn(title="post 3", content="some content", published=False))


async def test_update_post_success(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "update title post 1"}
    post_id = 1

    # When
    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["title"] == data["title"]


async def test_update_post_not_authenticated_fail(client: AsyncClient):
    # Given
    post_id = 1

    # When
    response = await client.patch(f"/posts/{post_id}", headers={})

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_update_post_not_found_fail(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "update title post 4"}
    post_id = 4

    # When
    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND
