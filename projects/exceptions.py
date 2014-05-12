class ProjectSetupError(Exception):
    """
    :py:class:`ProjectSetupError` is a *Jumpstart-native exception* that handles errors regarding the setup of a :py:class:`Project`.

    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)