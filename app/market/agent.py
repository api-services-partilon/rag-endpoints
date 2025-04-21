from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace
from pydantic import BaseModel

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
)

english_agent = Agent(
    name="english_agent",
    instructions="You translate the user's message to English",
    handoff_description="An english to english translator",
)

thai_agent = Agent(
    name="thai_agent",
    instructions="You translate the user's message to Thai",
    handoff_description="An english to thai translator",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        english_agent.as_tool(
            tool_name="translate_to_english",
            tool_description="Translate the user's message to English",
        ),
        thai_agent.as_tool(
            tool_name="translate_to_thai",
            tool_description="Translate the user's message to Thai",
        ),
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
)

json_formatter_agent = Agent(
    name="json_formatter_agent",
    instructions="You format the user's message into a JSON object.",
)

async def useAgents(msg: str):
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"'{text}'")

        synthesizer_result = await Runner.run(
            synthesizer_agent, orchestrator_result.to_input_list()
        )

        json_result = await Runner.run(
            json_formatter_agent, synthesizer_result.final_output
        )

    return json_result