import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
import llm

load_dotenv()

# Initialize the LLM model
model = llm.get_async_model("github/gpt-5-nano")

# Make an example request
response = model.prompt("Greet me in 5 languages.")
print(response.text())


def create_conversation():
    """Create a new conversation with tools from session state"""
    if "tools" not in st.session_state or not st.session_state.tools:
        return model.conversation()

    # Create tool functions for the LLM library
    tool_functions = []

    # Add each MCP tool as a function
    for tool_name, tool_info in st.session_state.tools.items():
        # Create a wrapper function for the MCP tool
        def create_tool_wrapper(tool_callable, tool_name):
            async def tool_wrapper(**kwargs):
                with st.chat_message("assistant"):
                    st.markdown(f"""Using tool: `{tool_name}({kwargs})` to answer this question.""")
                    result = await tool_callable(**kwargs)
                    st.markdown(f"""Got result from tool `{tool_name}`:""")
                    st.markdown(f"```\n{result}\n```")
                return result

            # Set function attributes for LLM library
            tool_wrapper.__name__ = tool_name
            tool_wrapper.__doc__ = f"MCP tool: {tool_name}"
            return tool_wrapper

        # Add the wrapped tool to our tools list
        wrapped_tool = create_tool_wrapper(tool_info["callable"], tool_name)
        tool_functions.append(wrapped_tool)

    # Create conversation with tools
    return model.conversation(tools=tool_functions)

async def ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversation" not in st.session_state:
        st.session_state.conversation = create_conversation()

    for message in st.session_state.messages:
        # skip tool calls
        if message["role"] == "tool" or 'tool_calls' in message:
            continue
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response = await agent_loop(st.session_state.conversation, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)


async def agent_loop(conversation, messages: List[dict]):
    # Get the latest user message
    latest_user_msg = None
    for msg in reversed(messages):
        if msg["role"] == "user":
            latest_user_msg = msg["content"]
            break

    if latest_user_msg:
        # Use the LLM library's built-in tool calling mechanism
        response = conversation.prompt(latest_user_msg)
        return response.text()

    return "No user message found to respond to."
