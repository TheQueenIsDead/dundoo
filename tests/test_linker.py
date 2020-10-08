import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock

from commands.command import Command

class TestLinker(unittest.TestCase):


    def test_chained_command_does_not_execute_if_parent_throws_exception(self):
        pass


if __name__ == '__main__':
    unittest.main()
