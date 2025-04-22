from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace

english_agent = Agent(
    name="english_agent",
    instructions="You translate the user's 'description' attributes to English",
    handoff_description="An target language to english translator",
)

thai_agent = Agent(
    name="thai_agent",
    instructions="You translate the user's 'description' attributes to Thai",
    handoff_description="An target language to thai translator",
)

korean_agent = Agent(
    name="korea_agent",
    instructions="You translate the user's 'description' attributes to Korean",
    handoff_description="An target language to korean translator"
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools." 
        "The output is only 'Content' object"
    ),
    tools=[
        english_agent.as_tool(
            tool_name="translate_to_english",
            tool_description="Translate the user's 'description' attributes to English",
        ),
        thai_agent.as_tool(
            tool_name="translate_to_thai",
            tool_description="Translate the user's 'description' attributes to Thai",
        ),
        korean_agent.as_tool(
            tool_name="translate_to_korean",
            tool_description="Translate the user's 'description' attributes to Korean",
        )
    ],
)

synthesizer_agent = Agent(
    name="synthesizer_agent",
    instructions="You inspect translations, correct them if needed, and produce a final concatenated response.",
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

    return synthesizer_result