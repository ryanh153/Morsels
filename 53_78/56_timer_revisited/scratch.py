#/usr/bin/python3

import pytest

## Code under test up here

def return_false() :
    return False


## Unit tests below here.
## Run with pytest:
## 'pytest unit_test.py'

## start with failing tests!

def test_first() :
    assert( factorial(1) == 1 )

def test_function() :
    # start with a failing test!
    assert ( return_false() );