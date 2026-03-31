TOOLS = [
    {
        "name": "read_file",
        "description": "Lê o conteúdo de um arquivo de texto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Caminho absoluto do arquivo"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Escreve ou sobrescreve um arquivo de texto.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Caminho do arquivo"},
                "content": {"type": "string", "description": "Conteúdo a escrever"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "query_database",
        "description": "Executa uma query SELECT em banco SQLite. Apenas leitura.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "Query SQL SELECT"},
            },
            "required": ["sql"],
        },
    },
    {
        "name": "http_get",
        "description": "Faz uma requisição HTTP GET e retorna o corpo da resposta.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL para requisição"},
            },
            "required": ["url"],
        },
    },
]
