
from typing import List, Dict, Optional, Union

from utils.logger import logger
from .message import format_message


class ChatHistoryManager:
    def __init__(self,
                 chat_log: List[Dict[str, str]] = None,
                 params: Optional[Dict[str, str]] = None,
                 ):
        self.chat_log = chat_log if chat_log is not None else []
        self.params = params if params is not None else {}

    def manage_history(self, new_logs: Union[Dict[str, str], List[Dict[str, str]]], replace: bool = False):
        """Manage chat history by appending or replacing logs."""
        logger.debug("manage_history called")
        if isinstance(new_logs, dict):
            new_logs = [new_logs]
        if replace:
            self.chat_log = new_logs
        else:
            self.chat_log.extend(new_logs)

    def reset_history(self, system_prompt):
        self.chat_log = [format_message("system", system_prompt)]

    def get_chat_history(self):
        return self.chat_log
