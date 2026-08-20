"""
Defines two classes: 
1) Appt for a single appointment
2) Agenda for a list of appointments
Name: Josh Gilliam 
Credit: Lines 50 ad 51 was explained by Noel Hernandez in a class encore session, 
conflicts function in Agenda class was doublechecked by ChatGPT.
"""

from datetime import datetime

class Appt:
    """An appointment has a start time, an end time, and a title.
    The start and end time should be on the same day.
    Usage example:
        appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
        appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
        if appt2 > appt1:
            print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
        elif appt1.overlaps(appt2):
            print("Oh no, a conflict in the schedule!")
            print(appt1.intersect(appt2))
    Should print:
        Oh no, a conflict in the schedule!
        2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

    def __init__(self, start: datetime, finish: datetime, desc: str):
        """An appointment from start time to finish time, with description desc.
        Start and finish should be the same day.
        """
        assert finish > start, f"Period finish ({finish}) must be after start ({start})"
        self.start = start
        self.finish = finish
        self.desc = desc

    def __eq__(self, other: 'Appt') -> bool:
        """Equality means same time period, ignoring description"""
        return self.start == other.start and self.finish == other.finish
    
    def __lt__(self, other: 'Appt') -> bool:
        """Less than means appointment a (self) is before appointment b (other)"""
        return self.finish <= other.start
    
    def __gt__(self, other: 'Appt') -> bool:
        """Greater than means appointment a (self) is after appointment b (other)"""
        return not self.start <= other.finish
    
    def overlaps(self, other: 'Appt') -> bool:
        """Is there a non-zero overlap between these periods?"""
        #return not (self.__lt__(other) or self.__gt__(other)) is overcomplicated 
        return not ((self < other) or (self > other))

    def intersect(self, other: 'Appt') -> 'Appt':
        """The overlapping portion of two Appt objects"""
        assert self.overlaps(other)  # Precondition

        start = max(self.start, other.start)
        finish = min(self.finish, other.finish)
        desc = f"{self.desc} and {other.desc}"

        return Appt(start, finish, desc)
    
    def __str__(self) -> str:
        """The textual format of an appointment is
        yyyy-mm-dd hh:mm hh:mm  | description
        Note that this is accurate only if start and finish
        are on the same day.
        """
        date_iso = self.start.date().isoformat()
        start_iso = self.start.time().isoformat(timespec='minutes')
        finish_iso = self.finish.time().isoformat(timespec='minutes')
        return f"{date_iso} {start_iso} {finish_iso} | {self.desc}" 
    
    def __repr__(self) -> str:
        return f"Appt({repr(self.start)}, {repr(self.finish)}, {repr(self.desc)})"


class Agenda:
    """An Agenda is a collection of appointments, 
    similar to a list. 

    Usage:
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda.text()}")
        print(f"Conflicts:\n {ag_conflicts}")

    Expected output:
    In agenda:
    2018-03-15 13:30 15:30 | Early afternoon nap
    2018-03-15 15:00 16:00 | Coffee break
    Conflicts:
    2018-03-15 15:00 15:30 | Early afternoon nap and Coffee break
    """

    def __init__(self):
        self.elements = [ ]

    def __eq__(self, other: 'Agenda') -> bool:
        """Delegate to __eq__ (==) of wrapped lists"""
        return self.elements == other.elements
    
    def __len__(self: 'Agenda') -> int:
        """Delegate to __len__ (len) of wrapped lists"""
        return len(self.elements)
    
    def append(self, appt: 'Appt'):
        """Delegate to append method of wrapped lists"""
        (self.elements).append(appt)
    
    def __str__(self):
        """Each Appt on its own line"""
        lines = [ str(e) for e in self.elements ]
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """The constructor does not actually work this way"""
        return f"Agenda({self.elements})"
    
    def sort(self):
        """Sort agenda by appointment start times"""
        self.elements.sort(key=lambda appt: appt.start)

    def conflicts(self) -> 'Agenda':
        """Returns an agenda consisting of the conflicts
        (overlaps) between this agenda and the other.
        Side effect: This agenda is sorted
        """
        conflicts = Agenda()
        self.sort()

        for i in range(self.__len__()):
            x = self.elements[i]
            for j in range(i + 1, self.__len__()):
                y = self.elements[j]
                if y.start >= x.finish:
                    break
                start = y.start
                finish = min(x.finish, y.finish)
                desc = f"{x.desc} and {y.desc}"
                conflicts.append(Appt(start, finish, desc))   
                      
        return conflicts
    

if __name__ == "__main__":
    print("Running usage examples")
    appt1 = Appt(datetime(2018, 3, 15, 13, 30), datetime(2018, 3, 15, 15, 30), "Early afternoon nap")
    appt2 = Appt(datetime(2018, 3, 15, 15, 00), datetime(2018, 3, 15, 16, 00), "Coffee break")
    if appt2 > appt1:
        print(f"appt1 '{appt1}' was over when appt2 '{appt2}'  started")
    elif appt1.overlaps(appt2):
        print("Oh no, a conflict in the schedule!")
        print(appt1.intersect(appt2))
    agenda = Agenda()
    agenda.append(appt1)
    agenda.append(appt2)
    ag_conflicts = agenda.conflicts()
    if len(ag_conflicts) == 0:
        print(f"Agenda has no conflicts")
    else:
        print(f"In agenda:\n{agenda}")
        print(f"Conflicts:\n {ag_conflicts}")