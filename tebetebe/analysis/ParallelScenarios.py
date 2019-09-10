from .. import defaults
import logging

class ParallelScenarios():
    """
    Context manager for serving multiple scenarios in parallel. This can be useful for
    comparing routing analysis from multiple scenarios side by side.

    Parameters
    ----------
    *args
        Arbitrary number of scenarios to be compiled, then executed in parallel
    """
    def __init__(self, *args):

        self.log = logging.getLogger(defaults.LOGGER)
        self.scenarios = {scenario.get_name(): scenario for scenario in args}

    def __enter__(self):
        for scenario in self.scenarios.values():
            scenario().__enter__()

        return self.scenarios

    def __exit__(self, exc_type, exc_msg, traceback):
        for scenario in self.scenarios.values():
            scenario.__exit__(exc_type, exc_msg, traceback)
