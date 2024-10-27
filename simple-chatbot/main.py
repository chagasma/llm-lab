from graph import create_graph, compile_workflow

print("Creating graph and compiling workflow...")
workflow = create_graph()
graph = compile_workflow(workflow)
print("Graph and workflow created.")

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["/quit", "/exit", "/q"]:
            print("Goodbye!")
            break

        for event in graph.stream({"messages": ("user", user_input)}):
            # print(event)
            for value in event.values():
                print(value)
