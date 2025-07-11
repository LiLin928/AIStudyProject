from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_deepseek import ChatDeepSeek
from typing import Annotated
from typing_extensions import TypedDict
import os
from dotenv import load_dotenv 

# 加载环境变量
load_dotenv(override=True)

class State(TypedDict):
    """聊天机器人的状态定义"""
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    """聊天机器人节点函数"""
    model = ChatDeepSeek(model="deepseek-chat")
    return {"messages": [model.invoke(state["messages"])]}

# 构建图
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 编译图
graph = graph_builder.compile()
