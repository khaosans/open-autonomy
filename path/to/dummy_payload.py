class DummyPayload(BaseTxPayload):
    """Represent a transaction payload for the dummy skill."""

    def __init__(self, sender: str, content: str) -> None:
        """Initialize a 'dummy' payload.

        Args:
            sender (str): The sender of the transaction.
            content (str): The content of the transaction.
        """
        super().__init__(sender)
        self._content = content

    @property
    def content(self) -> str:
        """Get the content.

        Returns:
            str: The content string.
        """
        return self._content

    @property
    def data(self) -> Dict:
        """Get the data.

        Returns:
            Dict: The data dictionary containing the content.
        """
        return {"content": self.content}
