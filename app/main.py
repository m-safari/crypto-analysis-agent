from app.container import AppContainer
from app.llm.agent import create_agent

def main():
    container = AppContainer()

    tools = container.tools

    agent = create_agent(
        llm=container.llm,
        tools=tools,
    )
    
    png = agent.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(png)

    config = {
        "configurable": {
            "thread_id": "user-1"
        }
    }

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ("exit", "quit"):
            break

        response = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            },
            config=config,
        )

        print("\nAssistant:", response["messages"][-1].content)


if __name__ == "__main__":
    main()
