# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the payloads for the 'hello_world' skill."""

from typing import Dict, Tuple

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


class DummyPayload(BaseTxPayload):
    """Represent a transaction payload for the dummy skill."""

    def __init__(self, sender: str, content: str) -> None:
        """Initialize a 'dummy' payload."""
        super().__init__(sender)
        self._content = content

    @property
    def content(self) -> str:
        """Get the content."""
        return self._content

    @property
    def data(self) -> Dict:
        """Get the data."""
        return {"content": self.content}

    @classmethod
    def from_json(cls, obj: Dict) -> "DummyPayload":
        """From json."""
        return cls(sender=obj["sender"], content=obj["content"])

    def __hash__(self) -> int:
        """Get the hash."""
        return hash(self.sender + self.content)

    @property
    def values(self) -> Tuple[str]:
        """Get the values."""
        return (self.content,)
