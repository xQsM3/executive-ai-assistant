"""Overall agent."""

from typing import TypedDict
from langgraph.graph import END, StateGraph

from eaia.main.nodes.triage import triage_input
from eaia.main.nodes.draft_response import draft_response
from eaia.main.nodes.find_meeting_time import find_meeting_time
from eaia.main.nodes.human_node import human_node
from eaia.main.nodes.mark_as_done_node import mark_as_done_node
from eaia.main.nodes.send_cal_invite_node import send_cal_invite_node
from eaia.main.nodes.send_mail_node import send_email_node
from eaia.main.nodes.rewrite import rewrite

from eaia.main.graph.condition_handler import (
    bad_tool_name,
    route_after_triage,
    take_action,
    enter_after_human,
)

from eaia.main.human_inbox import (
    send_message,
    send_email_draft,
    # notify,
    send_cal_invite,
)

from eaia.schemas import (
    State,
)

class ConfigSchema(TypedDict):
    db_id: int
    model: str


def graph_factory():
    graph_builder = StateGraph(State, config_schema=ConfigSchema)
    graph_builder.add_node(human_node)
    graph_builder.add_node(triage_input)
    graph_builder.add_node(draft_response)
    graph_builder.add_node(send_message)
    graph_builder.add_node(rewrite)
    graph_builder.add_node(mark_as_done_node)
    graph_builder.add_node(send_email_draft)
    graph_builder.add_node(send_email_node)
    graph_builder.add_node(bad_tool_name)
    # graph_builder.add_node(notify)
    graph_builder.add_node(send_cal_invite_node)
    graph_builder.add_node(send_cal_invite)

    graph_builder.add_conditional_edges("triage_input", route_after_triage)
    graph_builder.set_entry_point("triage_input")
    graph_builder.add_conditional_edges("draft_response", take_action)
    graph_builder.add_edge("send_message", "human_node")
    graph_builder.add_edge("send_cal_invite", "human_node")
    graph_builder.add_node(find_meeting_time)
    graph_builder.add_edge("find_meeting_time", "draft_response")
    graph_builder.add_edge("bad_tool_name", "draft_response")
    graph_builder.add_edge("send_cal_invite_node", "draft_response")
    graph_builder.add_edge("send_email_node", "mark_as_done_node")
    graph_builder.add_edge("rewrite", "send_email_draft")
    graph_builder.add_edge("send_email_draft", "human_node")
    graph_builder.add_edge("mark_as_done_node", END)
    # graph_builder.add_edge("notify", "human_node")
    graph_builder.add_conditional_edges("human_node", enter_after_human)
    return graph_builder.compile()


graph =  graph_factory()
