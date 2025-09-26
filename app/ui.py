import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
import llm

load_dotenv()

# Initialize the LLM model
model = llm.get_async_model("github/gpt-5-nano")


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
                    print(f"Calling tool {tool_name} with args {kwargs}")
                    st.markdown(f"""Using tool: `{tool_name}({kwargs})` to answer this question.""")
                    result = await tool_callable(**kwargs)
                    print(f"Result from tool {tool_name}: {result}")
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
    print(f"Creating conversation with tools: {[tool.__name__ for tool in tool_functions]}")
    return model.conversation(tools=tool_functions)

async def ui():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversation" not in st.session_state:
        st.session_state.conversation = create_conversation()

    conversation: llm.AsyncConversation = st.session_state.conversation

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
            response = conversation.chain(prompt)
            text = await response.text()
            st.session_state.messages.append({"role": "assistant", "content": text})
            with st.chat_message("assistant"):
                st.markdown(text)

