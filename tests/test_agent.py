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


def test_executor_write_file_within_work_dir(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"), work_dir=str(tmp_path))
    result = executor.execute("write_file", {"path": "output.txt", "content": "dados"})
    assert result["success"] is True
    assert (tmp_path / "output.txt").read_text() == "dados"


def test_executor_write_file_outside_work_dir_rejected(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"), work_dir=str(tmp_path))
    result = executor.execute("write_file", {"path": "/etc/passwd", "content": "hack"})
    assert result["success"] is False
    assert "fora do diretório" in result["error"]


def test_executor_query_database_rejects_multi_statement(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"), work_dir=str(tmp_path))
    result = executor.execute("query_database", {"sql": "SELECT 1; DROP TABLE x"})
    assert result["success"] is False
    assert "Multi-statements" in result["error"]


def test_executor_http_get_rejects_non_http_scheme(tmp_path):
    executor = ToolExecutor(db_path=str(tmp_path / "test.db"))
    result = executor.execute("http_get", {"url": "file:///etc/passwd"})
    assert result["success"] is False
    assert "http/https" in result["error"]
