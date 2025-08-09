class RunnerContextWrapper:
    def __init__(self, context):
        self.context = context


class GuardrailFunctionOutput:
    def __init__(self, tripwire_triggered: bool, result):
        self.tripwire_triggered = tripwire_triggered
        self.result = result


class Agent:
    def __init__(self, name, Instruction, tools=None, output_type=None):
        self.name = name
        self.instruction = Instruction
        self.tools = tools or []
        self.output_type = output_type


class Runner:
    @staticmethod
    async def run(agent, input_text, context=None):
        # Dummy async run method
        return {"message": f"Agent '{agent.name}' processed: {input_text}"}

    @staticmethod
    def run_sync(agent, input_text, context=None):
        # Sync runner for testing
        wrapper = RunnerContextWrapper(context)
        for tool in agent.tools:
            if getattr(tool, "_is_enabled", lambda *_: True)(wrapper, agent):
                return type("Result", (), {
                    "final_output": tool("1234")
                })()
        return type("Result", (), {
            "final_output": "Access Denied"
        })()


def function_tool(is_enabled=None):
    def decorator(func):
        func._is_enabled = is_enabled
        return func
    return decorator


def input_guradrail(func):
    return func
