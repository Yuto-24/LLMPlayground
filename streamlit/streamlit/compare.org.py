""" Page to compare the models """

from typing import List
from pydantic.dataclasses import dataclass
import asyncio

import streamlit as st

from utils.logger import logger
from utils.models import ModelManager
from utils.models.health_checker import ModelHealthChecker
from components.components import stream_generation, display_chat_history, gpt_parameter
from generator.generator import get_generator
from chat_manager.message import format_message
from chat_manager.history_manager import ChatHistoryManager


############# Page Setting #############
PAGE_TITLE = "Compare"
PAGE_ICON = "🏹"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
)
# Header
st.header(f"{PAGE_ICON} {PAGE_TITLE}")

############# Constant Setting #############
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

model_manager = ModelManager()
health_checker = ModelHealthChecker()


@dataclass
class ModelCompareState(ModelHealthChecker):
    model_name: str = None


@dataclass
class Compare:
    models: List[ModelCompareState]


############# Initialize #############
if "test" not in st.session_state:
    st.session_state.test = Compare([
        {
            # "model_name": "",
            "chat_log": [],
            "params": {},
        },
        {
            "model_name": "",
            "chat_log": [],
            "params": {},
        }
    ])


############# model select #############

col1, col2 = st.columns(2)
with col1:
    first_model = st.selectbox(
        "model 1",
        [
            model_manager.get_model_details(f).title for f
            in model_manager.get_available_model_ids()
        ],
        index=0,
    )
    st.session_state.test.models[0].model_name = model_manager.get_model_id_by_name(first_model)
with col2:
    second_model = st.selectbox(
        "model 2",
        [
            model_manager.get_model_details(f).title for f
            in model_manager.get_available_model_ids()
        ],
        index=1,
    )
    st.session_state.test.models[1].model_name = model_manager.get_model_id_by_name(second_model)

########## Page コンテンツ ##########
USER_INPUT = st.chat_input("メッセージを入力", disabled=False,)


############# Parameter Settings #############
with st.expander("Initial Settings", expanded=not USER_INPUT):
    SYSTEM_PROMPT = st.text_input(
        "system prompt",
        # value="",
        autocomplete="system_prompt",
    )
    PARAMS = gpt_parameter()

if len(PARAMS) > 0:
    st.session_state.test.models[0].params = PARAMS
    st.session_state.test.models[1].params = PARAMS


############# Async Setting #############

# 2列のレイアウトを作成
chat_col_left, chat_col_right = st.columns(2)


async def main():
    """ This is main Architecture of Call """

    # 両方の Requests を同時に非同期で取得
    response = await asyncio.gather(
        stream_generator(
            generator=st.session_state.test.models[0].model_name,
            message_list=st.session_state.test.models[0].chat_log,
            container=chat_col_left,
        ),
        stream_generator(
            generator=st.session_state.test.models[1].model_name,
            message_list=st.session_state.test.models[1].chat_log,
            container=chat_col_right,
        ),
    )

    return response


with chat_col_left:
    display_chat_history(st.session_state.test.models[0].chat_log, container_height=600)
with chat_col_right:
    display_chat_history(st.session_state.test.models[1].chat_log, container_height=600)


########## Chat Input ##########
if USER_INPUT:
    with chat_col_left:
        with st.chat_message("user"):
            st.write(USER_INPUT)
    with chat_col_right:
        with st.chat_message("user"):
            st.write(USER_INPUT)

    message = {"role": "user", "content": USER_INPUT}

    # Chat Log に user input を追加
    # left
    if st.session_state.test.models[0].chat_log == []:
        st.session_state.test.models[0].chat_log.append(
            {"role": "system", "content": SYSTEM_PROMPT or ""}
        )
    st.session_state.test.models[0].chat_log.append(message)
    # right
    if st.session_state.test.models[1].chat_log == []:
        st.session_state.test.models[1].chat_log.append(
            {"role": "system", "content": SYSTEM_PROMPT or ""}
        )
    st.session_state.test.models[1].chat_log.append(message)

    # stream を出力
    res = asyncio.run(main())

    # Chat Log に user input を追加
    st.session_state.test.models[0].chat_log.append(
        {"role": "assistant", "content": res[0]}
    )
    st.session_state.test.models[1].chat_log.append(
        {"role": "assistant", "content": res[1]}
    )

# チャット履歴をクリアするボタンが押されたら、メッセージをリセット
if len(st.session_state.test.models[0].chat_log) > 1:
    if st.button('Clear history'):
        # メッセージのリセット
        st.session_state.test.models[0].chat_log = [
            {"role": "system", "content": SYSTEM_PROMPT or ""}
        ]
        st.session_state.test.models[1].chat_log = [
            {"role": "system", "content": SYSTEM_PROMPT or ""}
        ]
        st.rerun()  # 画面を更新

# with chat_col_left:
#     st.write(st.session_state.test.models[0])
# with chat_col_right:
#     st.write(st.session_state.test.models[1])
