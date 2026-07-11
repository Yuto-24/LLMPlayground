"""GPT-4o Page File"""

import asyncio
import streamlit as st

from typing import Any
from pydantic import BaseModel

from utils.logger import logger
from utils.models import ModelManager
from utils.models.health_checker import ModelHealthChecker
from components.components import stream_generation, display_chat_history, gpt_parameter
from generator.generator import get_generator, BaseGenerator
from chat_manager.message import format_message
from chat_manager.history_manager import ChatHistoryManager


class ChatConfig(BaseModel):
    title: str
    icon: str
    base_url: str
    generator: Any


def preparing_chat(model_id) -> ChatConfig:
    # Model configuration
    model_manager = ModelManager()
    model_config = model_manager.get_model_details(model_id)
    logger.debug(model_config)

    title = model_config.title
    icon = model_config.icon
    base_url = model_config.api_config.base_url

    # worker
    generator = get_generator(model_config)

    return ChatConfig(
        title=title,
        icon=icon,
        base_url=base_url,
        generator=generator,
    )


MODEL_ID = "gpt4o"

chat_config = preparing_chat(MODEL_ID)

# Page settings
st.set_page_config(
    page_title=chat_config.title,
    page_icon=chat_config.icon,
)
st.header(f"{chat_config.icon} {chat_config.title}")


# Initialize session state
if MODEL_ID not in st.session_state:
    health_checker = ModelHealthChecker()
    with st.spinner(text="Preparing: Checking Status..."):
        health_checker.check(chat_config.base_url)
    st.session_state[MODEL_ID] = ChatHistoryManager(
        chat_log=[],
        params={},
    )


#################### Page Contents ####################

# User input field
USER_INPUT = st.chat_input("メッセージを入力")

# Parameters and system prompt section
with st.expander("Params", expanded=not USER_INPUT):
    SYSTEM_PROMPT = st.text_input(
        "System Prompt",
        autocomplete="system_prompt",
    ) or ""
    PARAMS = gpt_parameter()

# Update session parameters
if PARAMS:
    st.session_state[MODEL_ID].params.update(PARAMS)

# Display chat history
display_chat_history(st.session_state[MODEL_ID].chat_log)

# Process user input and generate a response
if USER_INPUT:
    # Display user input
    with st.chat_message("user"):
        st.write(USER_INPUT)

    # Add system prompt if no chat history exists
    if not st.session_state[MODEL_ID].chat_log:
        st.session_state[MODEL_ID].reset_history(SYSTEM_PROMPT)

    # Update chat history with user input
    new_chat_history = st.session_state[MODEL_ID].get_chat_history()
    new_chat_history.append(format_message("human", USER_INPUT))

    # Generate a response asynchronously
    response = asyncio.run(stream_generation(
        generator=chat_config.generator,
        message_list=new_chat_history,
        **(st.session_state[MODEL_ID].params or {}),
    ))
    new_chat_history.append(format_message("gpt", response))

    # Update chat history in session state
    st.session_state[MODEL_ID].manage_history(new_chat_history, replace=True)

# チャット履歴をクリアするボタンが押されたら、メッセージをリセット
if len(st.session_state[MODEL_ID].chat_log) > 1:
    if st.button('Clear history'):
        # メッセージのリセット
        st.session_state[MODEL_ID].reset_history(SYSTEM_PROMPT)
        st.rerun()  # 画面を更新
    if st.button('Share'):
        # メッセージのリセット
        st.session_state[MODEL_ID].reset_history(SYSTEM_PROMPT)
        st.rerun()  # 画面を更新
