import sys

import termcolor as tc


def success(msg):
    tc.cprint(f'Success: {msg.lower()}', 'green')


def fatal(msg):
    tc.cprint(f'Error: {msg.lower()}', 'red')
    sys.exit(1)


def call_and_report(callable, *args):
    ok, report = callable(*args)

    if ok:
        if report is not None:
            success(report)
    else:
        fatal(report)
