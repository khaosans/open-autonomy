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

"""This module contains the behaviours for the 'hello_world' skill."""

from abc import ABC
from typing import Generator, Set, Type

from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.hello_world.rounds import (
    DummyRound,
    PrintCountPayload,
    PrintCountRound,
    HelloWorldAbciApp,
)


class DummyBehaviour(BaseBehaviour, ABC):
    """Check whether Tendermint nodes are running."""

    matching_round = DummyRound

    def async_act(self) -> Generator:
        """Do the action."""
        # HW 1: Get owner address from config and print it
        owner_address = self.context.agent_config.get("owner", "0x0")

        # HW 1: Print message with owner address
        self.context.logger.info(
            f"Hello world! The owner's address is {owner_address}"
        )

        self.set_done()
        yield


class PrintCountBehaviour(BaseBehaviour, ABC):
    """Behaviour to track and print the message count."""

    matching_round = PrintCountRound

    def async_act(self) -> Generator:
        """Perform the action."""
        # HW 2: Get the current print count
        print_count = self.synchronized_data.print_count

        # HW 2: Increment the count and submit it in a payload
        self.context.logger.info(f"The message has been printed {print_count} times")
        payload = PrintCountPayload(self.context.agent_address, print_count + 1)
        yield from self.send_a2a_transaction(payload)

        self.set_done()
        yield


class HelloWorldConsensusBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the hello_world abci app."""

    initial_behaviour_cls = DummyBehaviour
    abci_app_cls = HelloWorldAbciApp
    behaviours: Set[Type[BaseBehaviour]] = {
        DummyBehaviour,  # type: ignore
        PrintCountBehaviour,  # type: ignore
    }
