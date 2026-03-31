"""
Exemplo: agente que lê um arquivo CSV de leads e classifica por prioridade.
"""
import os
import csv
import tempfile
from dotenv import load_dotenv

load_dotenv()


def create_sample_leads_file(path: str):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "empresa", "faturamento", "funcionarios", "interesse"])
        writer.writerows([
            ["Carlos Silva", "Restaurante Bom Sabor", "50000", "15", "alto"],
            ["Ana Lima", "Lanchonete Express", "8000", "3", "baixo"],
            ["Pedro Costa", "Rede Fast Food SP", "500000", "200", "alto"],
        ])


if __name__ == "__main__":
    from src.agent.runner.agent import ProcessAgent

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Configure ANTHROPIC_API_KEY no .env")
        exit(1)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        leads_path = f.name
    create_sample_leads_file(leads_path)

    agent = ProcessAgent(
        api_key=api_key,
        db_path="./data/agent.db",
        system_prompt="Você é um agente SDR. Analise leads e classifique por prioridade de contato.",
    )

    task = f"""
    Leia o arquivo de leads em {leads_path}.
    Para cada lead, avalie: faturamento, número de funcionários e nível de interesse.
    Classifique cada um como: ALTA, MÉDIA ou BAIXA prioridade.
    Escreva o resultado em /tmp/leads_classificados.txt com justificativa para cada classificação.
    """

    print("Executando agente...")
    result = agent.run(task)
    print(f"\nResultado:\n{result}")
