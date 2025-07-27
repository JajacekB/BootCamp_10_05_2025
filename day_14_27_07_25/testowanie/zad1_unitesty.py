from unittest import TestCase

class TryTesting(TestCase):
    def test_always_passed(self):
        self.assertTrue(True)

    def test_uppercase(self):
        assert  "python".upper() == "PYTHON"

    def test_reversed(self):
        assert list(reversed([1, 2, 3])) == [3, 2, 1]

    def test_reversed_test(self):
        self.assertEqual(
            list(reversed([1, 2, 3])),
            [3, 2, 1],
            "Odwracanie listy"
        )

    def test_alleays_fail(self):
        self.assertTrue(False)