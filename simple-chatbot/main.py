from graph import create_graph, compile_workflow, graph_visualization

print("Creating graph and compiling workflow...")
workflow = create_graph()
graph = compile_workflow(workflow)
print("Graph and workflow created.")
graph_visualization(graph, "./img/graph.png")

config = {"configurable": {"thread_id": "1"}}

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["/quit", "/exit", "/q"]:
            print("Goodbye!")
            break

        for event in graph.stream({"messages": ("user", user_input)}, config):
            # print(event)
            for value in event.values():
                print(value)
