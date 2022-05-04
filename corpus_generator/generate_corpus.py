import argparse
import logging
import sys
import os
from pathlib import Path
import json

from issue import Issue

__author__ = "Cliff Wulfman"
__copyright__ = "Cliff Wulfman"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from fluff.skeleton import fib`,
# when using this Python module as a library.

def generate_corpus(inpath, outpath_root):
    mets_files = Path(inpath).glob("**/*METS.xml")
    root = Path(outpath_root)
    for f in mets_files:
        issue_path = root / Path('/'.join(f.parts[-5:-1]))
        print(issue_path)
        issue_path.mkdir(parents=True)
        issue = Issue(f.parents[0])
        articles = issue.articles
        new_name = '.'.join((f.parts[-1][:-9], 'jsonl'))
        out_file = issue_path / Path(new_name)
        with open(out_file, 'w') as f:
            for article in articles:
                json.dump(article.jsonl, f)
                f.write('\n')


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "-inpath",
        help="path to METS/ALTO files"
    )
    parser.add_argument(
        "-outpath",
        help="output directory"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    generate_corpus(args.inpath, args.outpath)

def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m fluff.skeleton 42
    #
    run()
