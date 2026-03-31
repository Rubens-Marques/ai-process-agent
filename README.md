# ai-process-agent

> Agente IA com tools para automação de fluxos de negócio — lê dados, toma decisões e executa ações via function calling.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)
![Claude](https://img.shields.io/badge/Claude_API-Anthropic-8B5CF6?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## Sobre

Implementação do padrão ReAct com Claude API e function calling. O agente recebe uma tarefa em linguagem natural, decide quais tools usar, executa as ações e produz o resultado final — tudo de forma autônoma.

**Problema resolvido:** Fluxos de negócio que exigem ler dados, tomar decisões e escrever resultados podem ser automatizados descrevendo a tarefa em linguagem natural, sem programar caso a caso.

## Tools disponíveis

| Tool | O que faz |
|------|-----------|
| `read_file` | Lê conteúdo de arquivo de texto |
| `write_file` | Escreve resultado em arquivo |
| `query_database` | Executa SELECT em SQLite |
| `http_get` | Faz requisição HTTP GET |

## Como funciona

```
Tarefa em linguagem natural
         │
         ▼
    [Claude API]  ──── pensa e decide qual tool usar
         │
         ▼
   [ToolExecutor] ──── executa a tool
         │
         ▼
   [Claude API]  ──── analisa resultado, decide próximo passo
         │
    (loop até concluir)
         │
         ▼
      Resultado final
```

## Instalação

```bash
git clone https://github.com/Rubens-Marques/ai-process-agent
cd ai-process-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adicionar ANTHROPIC_API_KEY
```

## Como usar

```python
from src.agent.runner.agent import ProcessAgent

agent = ProcessAgent(api_key="sk-ant-...", db_path="./data/agent.db")

result = agent.run("""
    Leia o arquivo /tmp/vendas.csv,
    some o total de vendas do mês de março,
    e escreva o resultado em /tmp/relatorio.txt.
""")
print(result)
```

```bash
# Rodar exemplo incluído
python examples/example_lead_triage.py
```

## Testes

```bash
pytest tests/ -v
```

## Licença

MIT © Rubens Marques
