import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call


@pytest.mark.asyncio
async def test_run_migrations_executes_all_statements():
    mock_conn = AsyncMock()
    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_ctx.__aexit__ = AsyncMock(return_value=False)

    with patch("app.database.engine") as mock_engine:
        mock_engine.begin.return_value = mock_ctx
        from app.database import run_migrations
        await run_migrations()

    assert mock_conn.execute.call_count == 3
