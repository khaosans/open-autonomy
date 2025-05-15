from packages.valory.skills.test_abci.rounds import PrintCountRound

class TestAbciApp(AbciApp):
    """Test ABCI application."""

    transition_function = {
        DummyRound: {PrintCountRound},
        PrintCountRound: {DummyRound},
    }
