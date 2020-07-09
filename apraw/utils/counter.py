import random


class ExponentialCounter:
    """A class to provide an exponential counter with jitter."""

    def __init__(self, max_counter: int):
        """
        Initialize an instance of ExponentialCounter.

        Parameters
        ----------
        max_counter: int
            The maximum value to reach before resetting.
        """
        self._value = 1
        self._max = max_counter

    def count(self) -> int:
        """
        Increment the counter and return the current value with jitter.

        Returns
        -------
        value: int
            The current value defined by the counter.
        """
        max_jitter = self._value / 16.0
        self._value = min(self._value * 2, self._max)
        value = self._value + random.random() * max_jitter - max_jitter / 2
        return value

    def reset(self):
        """
        Reset the counter to 1.

        Returns
        -------
        value: int
            The reset value for easy use.
        """
        self._value = 1
        return self._value
