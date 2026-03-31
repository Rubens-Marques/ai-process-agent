import json
import anthropic
from src.agent.tools.definitions import TOOLS
from src.agent.tools.executor import ToolExecutor


class ProcessAgent:
    def __init__(
        self,
        api_key: str,
        db_path: str,
        model: str = "claude-3-5-haiku-20241022",
        max_iterations: int = 10,
        system_prompt: str = "",
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.executor = ToolExecutor(db_path=db_path)
        self.model = model
        self.max_iterations = max_iterations
        self.system_prompt = system_prompt or (
            "Você é um agente de automação de processos. "
            "Use as tools disponíveis para completar as tarefas solicitadas. "
            "Seja preciso, eficiente e informe o resultado final claramente."
        )
    def run(self, task: str) -> str:
        messages: list[dict] = [{"role": "user", "content": task}]

        for _ in range(self.max_iterations):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                return self._extract_text(response)

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self.executor.execute(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, ensure_ascii=False),
                        })
                messages.append({"role": "user", "content": tool_results})
                continue

            return f"Agente encerrado: stop_reason={response.stop_reason}"

        return f"Limite de {self.max_iterations} iterações atingido."

    def _extract_text(self, response) -> str:
        texts = [b.text for b in response.content if hasattr(b, "text")]
        return "\n".join(texts)
