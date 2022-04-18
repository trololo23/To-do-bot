from enum import Enum, auto


class UserState(Enum):
    Waiting_For_Task = auto()
    Waiting_For_Marking = auto()
    Waiting_For_Erase = auto()
    Start_Task = auto()
    Start_Marking = auto()
    Start_Erase = auto()
