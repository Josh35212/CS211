"""
Appointment file generator, used for generating larger test cases.

Usage:  TODO
"""

import appt
import appt_io
import datetime


def repeat(first: str, hours_between: int, repetitions: int) -> appt.Agenda:
    """An agenda made up of a series of appointments at some regular interval,
    starting with an appointment described by the first string which
    should look like "2108-12-5 10:15 13:15 | This is a dummy".
    """
    agenda = appt.Agenda()
    mtg = appt_io.parse_appt(first)
    interval = datetime.timedelta(hours=hours_between)
    desc = mtg.desc
    for rep in range(repetitions):
        agenda.append(mtg)
        mtg = appt.Appt(mtg.start + interval, mtg.finish + interval, f"{desc} #{rep + 1}")
    return agenda


def sample():
    agenda = repeat("2018-11-20 08:00 08:59 | Sample appt", 1, 5000)
    for mtg in agenda:
        print(mtg)


sample()
