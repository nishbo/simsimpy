class Error(Exception):
    """Handles errors that occur in this class."""

    def __init__(self, msg, value):
        """Inits an exception with a message and wrong value.

        Args:
            msg: String with description of what happened.
            value: Value that supposedly was wrongly provided.
        """
        self.msg = msg
        self.value = value

    def __str__(self):
        return repr('%s Value: %s' % (self.msg, str(self.value)))
