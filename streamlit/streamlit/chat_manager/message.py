from typing import Literal


def format_message(type: Literal["system", "human", "gpt"], prompt: str):
    roles = {"system": "system",
             "human": "user",
             "gpt": "assistant",
             }
    return {"role": roles[type], "content": prompt}
