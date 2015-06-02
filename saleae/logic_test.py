from unittest import TestCase

from saleae import logic


class LogicTest(TestCase):

    '''Tests for the Logic class.

    These tests are intended to be ran while Logic is open in simulation
    mode, that is when no Saleae device is connected.'''

    def setUp(self):
        self._logic = logic.Logic()

    def tearDown(self):
        self._logic.close()

    def test_connected_devices(self):
        devices = self._logic.connected_devices

        assert len(devices) == 4

    def test_sample_rate_at_least(self):
        sample_rates = sorted(self._logic.all_sample_rates)
        first = self._logic.sample_rate_at_least()
        assert first == sample_rates[0]

        last = self._logic.sample_rate_at_least(
            digital_min=sample_rates[-1][0],
            analog_min=sample_rates[-1][1])

        assert last == sample_rates[-1]
