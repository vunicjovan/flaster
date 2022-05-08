from argparse import ArgumentParser
from pathlib import Path

ARGUMENTS = dict(
    target_path=dict(
        help="Path related to the project location",
        nargs="?",
        default=str(Path.home()),
    ),
    project=dict(
        help="Name of the Flask project",
        nargs="?",
        default="flaster-project",
    ),
    apps=dict(
        help="Array of Flask Blueprint apps",
        nargs="+",
        default=[],
    ),
)


class Commander:
    def _set_arguments(self):
        """
        Sets arguments provided by global ARGUMENTS dictionary to argument parser.
        """

        [
            self.parser.add_argument(
                f"--{a}",
                help=d.get("help"),
                nargs=d.get("nargs"),
                default=d.get("default"),
            )
            for a, d in ARGUMENTS.items()
        ]

    def __init__(self):
        """
        Initializes argument parser and sets its arguments.
        """

        self.parser = ArgumentParser()
        self._set_arguments()
        self.args = self.parser.parse_args()
