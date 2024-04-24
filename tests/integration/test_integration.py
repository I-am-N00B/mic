import asyncpg
import requests
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'paintings_service/app'))
sys.path.append(str(BASE_DIR / 'museum_service/app'))

from paintings_service.app.main import service_alive as paintings_status
from museum_service.app.main import service_alive as museum_status


@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"


@pytest.mark.asyncio
async def test_paintings_service_connection():
    r = await paintings_status()
    assert r == {'message': 'service alive'}


@pytest.mark.asyncio
async def test_museum_service_connection():
    r = await museum_status()
    assert r == {'message': 'service alive'}
