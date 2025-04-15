# noinspection PyPep8Naming
import Deduce_patient as dp
import unittest

class TestDeducePatient(unittest.TestCase):
    def test_get_first_names(self):
        assert ['Pablo', 'Javier'] == dp.get_first_names({'VOORNAAM': 'Pablo Javier'})
        assert ['Robert', 'Rob'] == dp.get_first_names({'VOORNAAM': 'Robert', 'ROEPNAAM': 'Rob'})
        assert ['Tom'] == dp.get_first_names({'ROEPNAAM': 'Tom'})


if __name__ == '__main__':
    unittest.main()
