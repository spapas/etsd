from django.test import TestCase


class SampleTestCase(TestCase):

    def setUp(self):
        self.value = 1

    def test_value_is_1(self):
        """Make sure that value is 1"""
        self.assertEqual(self.value, 1)

    def test_value_is_2(self):
        """Make sure that value is 2"""
        self.assertEqual(self.value, 2)
