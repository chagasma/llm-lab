from langgraph.constants import END

from states.state import State


def should_search_database(state: State):
    last_message = state["messages"][-1]
    content = last_message.content.lower()
    if "db" in content or "database" in content:
        return "search_db"
    return END
