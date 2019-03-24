"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""
from unittest import TestCase
from app import app


class UnitBaseTest(TestCase):
    pass
