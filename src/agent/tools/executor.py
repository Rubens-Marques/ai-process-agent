import sqlite3
from pathlib import Path
from urllib.parse import urlparse
import requests


class ToolExecutor:
    def __init__(self, db_path: str, work_dir: str = "."):
        self.db_path = db_path
        self.work_dir = Path(work_dir).resolve()

    def execute(self, tool_name: str, inputs: dict) -> dict:
        handlers = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "query_database": self._query_database,
            "http_get": self._http_get,
        }
        handler = handlers.get(tool_name)
        if not handler:
            return {"success": False, "error": f"Tool desconhecida: {tool_name}"}
        try:
            return handler(inputs)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_file(self, inputs: dict) -> dict:
        path = Path(inputs["path"])
        if not path.exists():
            return {"success": False, "error": f"Arquivo não encontrado: {inputs['path']}"}
        return {"success": True, "content": path.read_text(encoding="utf-8")}

    def _write_file(self, inputs: dict) -> dict:
        path = Path(inputs["path"])
        if not path.is_absolute():
            path = self.work_dir / path
        resolved = path.resolve()
        if not str(resolved).startswith(str(self.work_dir)):
            return {"success": False, "error": f"Caminho fora do diretório permitido: {inputs['path']}"}
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(inputs["content"], encoding="utf-8")
        return {"success": True, "message": f"Arquivo escrito em {resolved}"}

    def _query_database(self, inputs: dict) -> dict:
        sql = inputs["sql"].strip()
        if not sql.upper().startswith("SELECT"):
            return {"success": False, "error": "Apenas queries SELECT são permitidas"}
        if ";" in sql:
            return {"success": False, "error": "Multi-statements não são permitidos"}
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.execute(sql)
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description] if cursor.description else []
            return {"success": True, "columns": columns, "rows": rows}
        finally:
            conn.close()

    def _http_get(self, inputs: dict) -> dict:
        url = inputs["url"]
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return {"success": False, "error": "Apenas URLs http/https são permitidas"}
        response = requests.get(url, timeout=10, allow_redirects=False)
        response.raise_for_status()
        return {"success": True, "status_code": response.status_code, "body": response.text[:2000]}
