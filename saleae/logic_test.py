# This file is part of pysaleae.
#
# pysaleae is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysaleae is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pysaleae.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (c) 2015 Simon Marchi <simon.marchi@polymtl.ca>

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
