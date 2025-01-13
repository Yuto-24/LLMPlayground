"""
This file is managing about UI
"""

import asyncio
from typing import List, Dict, Union, Generator

import streamlit as st

from utils.logger import logger
from generator.generator import BaseGenerator

# Constants for roles
ASSISTANT = "assistant"
USER = "user"


def display_chat_message(role: str, content: str) -> None:
    """Displays a single chat message."""
    with st.chat_message(role):
        st.write(content)


def display_chat_history(message_logs: list, container=None, container_height: int = 0) -> None:
    """Displays the chat history."""
    chat_history_box = container or st.container(height=container_height)
    if message_logs:
        with chat_history_box:
            for message in message_logs:
                if message["role"] in {ASSISTANT, USER} and message["content"].strip():
                    display_chat_message(message["role"], message["content"])


class StreamHolder:
    """ Manager of stream text holder """

    def __init__(self) -> None:
        self.full_text = ""
        self.message_placeholder = st.empty()

    async def add_text_to_chat_box(self, text: str) -> None:
        """
        Adds text to the chat box and updates the UI.
        """
        self.full_text += text
        self.message_placeholder.markdown(self.full_text)
        await asyncio.sleep(0.01)


async def process_stream_response(stream_response: Generator, container=None):
    """Display streaming content inside a container."""
    with container or st.container(height=0):
        with st.chat_message(ASSISTANT):
            holder = StreamHolder()
            full_response = ""
            for chunk in stream_response:
                try:
                    chunk_text = chunk.choices[0].delta.content or ""
                    full_response += chunk_text
                    await holder.add_text_to_chat_box(chunk_text)
                except (IndexError, AttributeError) as e:
                    logger.debug(e)
                    continue
    return full_response


async def stream_generation(
    generator: BaseGenerator,
    message_list: List[Dict[str, str]],
    container=None,
    **parameter,
) -> str:
    """Generate a response from a model and stream it to the container."""
    logger.debug("stream_generation called.")

    # Fetch the streaming response
    stream_response = generator.gen(message_list, **parameter)

    # Display the streaming response
    response = await process_stream_response(stream_response, container)

    # logging
    logger.info(f"message_list: {message_list}")
    logger.info(f"response: {response}")

    return response


# Constants for parameter descriptions
TEMPERATURE_HELP = """ランダム出力制御。高い値ほどランダム出力される。
※範囲 0.0 ～ 2.0"""
TOP_P_HELP = """多様性出力制御。高い値ほど多彩な単語が出力される。
※範囲 0.0 ～ 1.0"""
MAX_NEW_TOKENS_HELP = """トークンの長さ。指定したトークンの上限に達すると回答が打ち切られる。
※範囲 1 ～"""
FREQUENCY_PENALTY_HELP = """頻度ペナルティ制御。正の値ほど、頻出単語へのペナルティを課し、
モデルが新しいトピックについて話す可能性を高める。
※範囲 -2.0 ～ 2.0"""
PRESENCE_PENALTY_HELP = """存在ペナルティ制御。正の値ほど、ペナルティを課し、
モデルが同じ行を逐語的に繰り返す可能性を低下させる。
※範囲 -2.0 ～ 2.0"""


def gpt_parameter(**kwargs) -> Dict[str, Union[str, float, int]]:
    """
    Create and manage GPT parameters input in a Streamlit interface.

    Args:
        **kwargs: Optional default values for each parameter.

    Returns:
        dict: Parameters for GPT model configuration.
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        temperature = st.number_input(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=kwargs.get("temperature", 0.1),
            help=TEMPERATURE_HELP,
        )
        top_p = st.number_input(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=kwargs.get("top_p", 0.98),
            help=TOP_P_HELP,
        )
    with col2:
        max_new_token = st.number_input(
            "Max Tokens",
            min_value=1,
            max_value=16384,
            value=kwargs.get("max_new_token", 1024),
            help=MAX_NEW_TOKENS_HELP,
        )
        frequency_penalty = st.number_input(
            "Frequency Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=kwargs.get("frequency_penalty", 0.0),
            help=FREQUENCY_PENALTY_HELP,
        )
    with col3:
        presence_penalty = st.number_input(
            "Presence Penalty",
            min_value=-2.0,
            max_value=2.0,
            value=kwargs.get("presence_penalty", 0.0),
            help=PRESENCE_PENALTY_HELP,
        )
        stop_word = st.text_input("Stop Word")

    # Compile parameters into a dictionary
    parameter = {
        "temperature": temperature,
        "top_p": top_p,
        "n": 1,  # Number of completions to generate
        "max_tokens": max_new_token,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
    }

    # Add stop word if provided
    if stop_word:
        parameter["stop"] = stop_word

    return parameter
