from dataclasses import dataclass
from typing import Any

NOT_SET = object()


def loop_helper(iterable, previous_default=None, next_default=None):
    # setup data (most only needed if iterable is length 1)
    is_first, index, previous, current = True, 0, previous_default, NOT_SET

    for value in iterable:
        # If this is the first loop, store the value and skip to loop two
        if current is NOT_SET:
            current = value
            continue
        # Make the return for the value one ahead of where we are
        next_ = value
        info = Info(is_first=is_first, index=index, previous=previous, current=current, next=next_, is_last=False)
        yield current, info
        # Setup data for the next loop
        is_first, index, previous, current = False, index+1, current, next_

    # After the loop ends we still have one more yield to do (unless the length of the iterable is zero)
    if current is not NOT_SET:
        info = Info(is_first=is_first, index=index, previous=previous, current=current, next=next_default, is_last=True)
        yield current, info


@dataclass()
class Info:
    is_first: bool
    index: int
    previous: Any
    current: Any
    next: Any
    is_last: bool
