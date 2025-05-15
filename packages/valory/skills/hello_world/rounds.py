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

"""This module contains the data classes for the hello_world ABCI application."""

from enum import Enum
from typing import Dict, Optional, Tuple, Type, cast

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    BaseSynchronizedData,
    BaseTxPayload,
    CollectDifferentUntilAllRound,
    CollectSameUntilThresholdRound,
)
from packages.valory.skills.hello_world.payloads import DummyPayload


class Event(Enum):
    """Event enumeration for the hello_world abci demo."""

    DONE = "done"
    ROUND_TIMEOUT = "round_timeout"
    RESET_TIMEOUT = "reset_timeout"


class DummyRound(CollectDifferentUntilAllRound):
    """
    This class represents the registration round.

    Input: None
    Output: a synchronized data with the set of participants.

    It schedules the SelectKeeperARound.
    """

    payload_class = DummyPayload
    synchronized_data_class = BaseSynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Event]]:
        """Process the end of the block."""
        return self.synchronized_data, Event.DONE


class PrintCountPayload(BaseTxPayload):
    """Payload for tracking print count."""

    def __init__(self, sender: str, print_count: int) -> None:
        """Initialize payload."""
        super().__init__(sender)
        self._print_count = print_count

    @property
    def print_count(self) -> int:
        """Get the print count."""
        return self._print_count


class SynchronizedData(BaseSynchronizedData):
    """Synchronized data extended with print_count."""

    @property
    def print_count(self) -> int:
        """Get the print count."""
        return cast(int, self.db.get("print_count", 0))


class PrintCountRound(CollectSameUntilThresholdRound):
    """Round to track print count."""

    payload_class = PrintCountPayload
    synchronized_data_class = SynchronizedData

    def end_block(self) -> BaseSynchronizedData:
        """Update synchronized data with incremented print count."""
        updated_count = self.synchronized_data.print_count + 1
        return self.synchronized_data.update(print_count=updated_count)


class HelloWorldAbciApp(AbciApp[Event]):
    """HelloWorldAbciApp

    Initial round: DummyRound

    Initial states: {DummyRound}

    Transition states:
        0. DummyRound
            - done: 1. PrintCountRound
        1. PrintCountRound
            - done: 0. DummyRound

    Final states: {}

    Timeouts:
        round timeout: 30.0
        reset timeout: 30.0
    """

    initial_round_cls: Type[AbstractRound] = DummyRound
    transition_function: AbciAppTransitionFunction = {
        DummyRound: {Event.DONE: PrintCountRound},
        PrintCountRound: {Event.DONE: DummyRound},
    }
    event_to_timeout: Dict[Event, float] = {
        Event.ROUND_TIMEOUT: 30.0,
        Event.RESET_TIMEOUT: 30.0,
    }
