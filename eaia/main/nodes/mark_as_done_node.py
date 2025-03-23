from eaia.gmail import mark_as_done

def mark_as_done_node(state):
    mark_as_done(state["email"]["id"])