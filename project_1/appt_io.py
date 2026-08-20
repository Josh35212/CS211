"""
Input and output conversions for Appt and Agenda objects.
parse_appt is inverse of Appt.__str__
parse_agenda is inverse of Agenda.text

"""

import appt
import datetime
from typing import Iterable


def parse_appt(appt_text: str) -> appt.Appt:
    """Parse something like
    "2018-05-03 15:40 16:15 | Study hard"
    into an Appt object.
    Period is separated from title by |
    Date must be yyyy-mm-dd  (with leading zeros if needed)
    Times are in 24 hour format, with leading zeros if needed,
    e.g., 03:00 is 3am and 15:00 is 3pm.
    Note this is inverse of the Appt.__str__ method.
    """
    try:
        period, desc = appt_text.split('|')
        date, start, finish = period.split()
        # In Python 3.7 we could do:
        # period_start = datetime.fromisoformat(f"{date}T{start}")
        # period_finish = datetime.fromisoformat(f"{date}T{finish}")
        # In Python 3.6 we need to use strptime
        iso_8601_fmt = "%Y-%m-%dT%H:%M"
        period_start = datetime.datetime.strptime(f"{date}T{start}", iso_8601_fmt)
        period_finish = datetime.datetime.strptime(f"{date}T{finish}", iso_8601_fmt)
    except Exception as err:
        raise ValueError(f"*** Failed to parse '{appt_text}' ***\n{err}")
    return appt.Appt(period_start, period_finish, desc)


def read_agenda(file: Iterable[str]) -> appt.Agenda:
    """Read an agenda from a file or list of str.
    Skips comments and blank lines.
    May throw exception if a line is not in proper format.
    """
    agenda = appt.Agenda()
    for line in file:
        line = line.strip()
        # Trim trailing comment (or whole line)
        line = line.split("#")[0]
        if len(line) > 0:
            # Remaining content should be an appointment spec
            agenda.append(parse_appt(line))
    return agenda


def parse_agenda(s: str) -> appt.Agenda:
    """Read an agenda from a triple-quoted string with
    one line per appointment.  Skips blank lines and
    comment lines beginning with #.
    """
    lines = s.split("\n")
    return read_agenda(lines)
