import unittest
from unittest.mock import Mock

from commands.command import Command


class TestCommand(unittest.TestCase):

    def test_constructor_links_next_node_when_passed_in_constructor(self):
        # Assemble
        c2 = Command()
        c1 = Command(next=c2)

        # Assert
        self.assertEqual(c1.get_next(), c2)
        self.assertEqual(c2.get_previous(), c1)

    def test_constructor_links_previous_node_when_passed_in_constructor(self):
        # Assemble
        c1 = Command()
        c2 = Command(previous=c1)

        # Assert
        self.assertEqual(c1.get_next(), c2)
        self.assertEqual(c2.get_previous(), c1)

    def test_constructor_links_previous_and_next_node_when_passed_in_constructor(self):
        # Assemble
        c1 = Command()
        c3 = Command()
        c2 = Command(previous=c1, next=c3)

        # Assert
        self.assertEqual(c1.get_previous(), None)
        self.assertEqual(c1.get_next(), c2)
        self.assertEqual(c2.get_previous(), c1)
        self.assertEqual(c2.get_next(), c3)
        self.assertEqual(c3.get_previous(), c2)
        self.assertEqual(c3.get_next(), None)

    def test_set_next_sets_node_correctly(self):
        # Assemble
        c1 = Command()
        c2 = Command()

        # Action
        c1.set_next(c2)

        # Assert
        self.assertEqual(c1.get_next(), c2)
        self.assertEqual(c1.get_previous(), None)
        self.assertEqual(c2.get_next(), None)
        self.assertEqual(c2.get_previous(), c1)

    def test_set_previous_sets_node_correctly(self):
        # Assemble
        c1 = Command()
        c2 = Command()

        # Action
        c2.set_previous(c1)

        # Assert
        self.assertEqual(c1.get_next(), c2)
        self.assertEqual(c1.get_previous(), None)
        self.assertEqual(c2.get_next(), None)
        self.assertEqual(c2.get_previous(), c1)

    def test_all_execute_when_no_errors_are_thrown(self):
        # Setup command chain with mocked __do__ functions
        c2 = Command()
        c1 = Command(next=c2)
        c1.__do__ = Mock()
        c2.__do__ = Mock()

        # Action
        c1.run()

        # Assert all functions called
        c1.__do__.assert_called_once()
        c2.__do__.assert_called_once()

    def test_chained_command_does_not_execute_if_parent_throws_exception(self):
        # Assemble command chain with mocked __do__ functions
        # Initial command triggered will throw exception
        c1 = Command()
        c2 = Command(previous=c1)
        c1.__do__ = Mock(side_effect=Exception('Oh No!'))
        c2.__do__ = Mock()

        # Action
        c1.run()

        # Assert command one was called (Threw an exception) and c2 was not called
        c1.__do__.assert_called_once()
        c2.__do__.assert_not_called()

    def test_child_command_rolls_back_self_on_exception(self):
        # Assemble command chain with mocked __do__ functions
        # Initial command triggered will throw exception
        c1 = Command()
        c2 = Command(previous=c1)
        c2.__do__ = Mock(side_effect=Exception('Oh No!'))
        c2.__undo__ = Mock()

        # Action
        c1.run()

        # Assert command 2 was rolled back
        c2.__undo__.assert_called_once()

    def test_child_command_rolls_back_parent_on_exception(self):
        # Assemble command chain with mocked __do__ functions
        # Initial command triggered will throw exception
        c1 = Command()
        c2 = Command(previous=c1)
        c1.rollback = Mock()
        c2.__do__ = Mock(side_effect=Exception('Oh No!'))

        # Action
        c1.run()

        # Assert command one was rolled back
        c1.rollback.assert_called_once()

    def test_set_action_overrides_with_function(self):
        c1 = Command()

        def my_action(): return 1

        c1.set_action(my_action)

        self.assertEqual(1, c1.__do__())

    def test_set_action_overrides_with_function_and_allows_params(self):
        # Assemble
        c1 = Command()

        def my_action(x, y): return x + y

        # Action
        c1.set_action(my_action)

        # Assert
        self.assertEqual(3, c1.__do__(1, 2))

    def test_set_action_overrides_with_lambda(self):
        # Assemble
        c1 = Command()
        # Action
        c1.set_action(lambda x, y: x + y)
        # Assert
        self.assertEqual(3, c1.__do__(1, 2))

    def test_find_head_returns_head_in_chain(self):
        c1 = Command()
        c2 = Command(previous=c1)
        c3 = Command(previous=c2)

        self.assertEqual(c3.find_head(), c1)


if __name__ == '__main__':
    unittest.main()
