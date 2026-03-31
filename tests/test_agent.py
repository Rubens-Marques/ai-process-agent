import pytest
from unittest.mock import patch, MagicMock
from src.agent.tools.executor import ToolExecutor
from src.agent.tools.definitions import TOOLS


def test_tool_definitions_have_required_fields():
    for tool in TOOLS:
        assert "name" in tool
        assert "description" in tool
        assert "input_schema" in tool


def test_executor_read_file_success(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("conteúdo de teste")
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"))
    result = executor.execute("read_file", {"path": str(test_file)})
    assert result["success"] is True
    assert "conteúdo de teste" in result["content"]


def test_executor_read_file_not_found(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"))
    result = executor.execute("read_file", {"path": "/tmp/nao_existe_xyz.txt"})
    assert result["success"] is False
    assert "error" in result


def test_executor_unknown_tool(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"))
    result = executor.execute("ferramenta_inexistente", {})
    assert result["success"] is False
