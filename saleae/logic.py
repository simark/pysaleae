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


import socket

_CAPTURE = 'CAPTURE'
_GET_ALL_SAMPLE_RATES = 'GET_ALL_SAMPLE_RATES'
_GET_CONNECTED_DEVICES = 'GET_CONNECTED_DEVICES'
_GET_SAMPLE_RATE = 'GET_SAMPLE_RATE'
_SET_NUM_SAMPLES = 'SET_NUM_SAMPLES'
_SET_SAMPLE_RATE = 'SET_SAMPLE_RATE'


class Internalerror(Exception):

    def __init__(self, response):
        self._response = response

    def __str__(self):
        'Internal error, got response: {}'.format(self._response)


class Device:

    def __init__(self, num, name, kind, dev_id, active):
        self._num = num
        self._name = name
        self._kind = kind
        self._dev_id = dev_id
        self._active = active

    @property
    def num(self):
        return self._num

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def dev_id(self):
        return self._dev_id

    @property
    def active(self):
        return self._active

    def __str__(self):
        return repr(self)

    def __repr__(self):
        f = 'Device(num={self.num}, name="{self.name}", ' \
            'kind="{self.kind}", dev_id="{self.dev_id}", ' \
            'active={self.active})'
        return f.format(self=self)


class Logic:

    def __init__(self, ip='127.0.0.1', port=10429):
        '''Initialize a connection to Logic.

        If ip is omitted, 127.0.0.1 is used. If port is omitted, 10429
        is used (the default value in Logic).
        '''

        self._ip = ip
        self._port = port
        self._socket_real = None
        self._recv_size = 0x10000

    @property
    def _socket(self):
        if not self._socket_real:
            self._socket_real = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self._socket_real.connect((self._ip, self._port))

        return self._socket_real

    def _socket_send(self, b):
        self._socket.send(b.encode() + b'\0')

    def _socket_recv(self):
        b = self._socket.recv(self._recv_size).decode()
        b = b.split('\n')
        if b[-1] != 'ACK':
            raise Internalerror(b)
        return b[:-1]

    @property
    def connected_devices(self):
        '''Get the connected Saleae devices.

        Returns a list of Device objects.
        '''

        self._socket_send(_GET_CONNECTED_DEVICES)
        lines = self._socket_recv()

        devices = []
        for line in lines:
            dev_info = [x.strip() for x in line.split(',')]

            num = int(dev_info[0])
            name = dev_info[1]
            kind = dev_info[2]
            dev_id = dev_info[3]
            active = len(dev_info) > 4 and dev_info[4] == 'ACTIVE'

            dev = Device(num, name, kind, dev_id, active)
            devices.append(dev)

        return devices

    def set_num_samples(self, num_samples):
        '''Set the duration of the capture in number of samples.'''

        s = '{}, {}'.format(_SET_NUM_SAMPLES, num_samples)
        self._socket_send(s)
        self._socket_recv()

    def set_num_seconds(self, seconds):
        '''Set the duration of the capture in seconds.

        Set the duration of the capture in seconds, based on the current
        sample rate. Therefore, to get the desired result, this method
        must be called after the sample rate has been set.
        '''

        sr = self.sample_rate[0]
        samples = sr * seconds
        self.set_num_samples(samples)

    @property
    def all_sample_rates(self):
        '''Get all the available sample rates values.

        The returned value is a list of sample rates. Each sample rate
        is a value in the form:

            (digital_sample_rate, analog_sample_rate)

        The available sample rates values depend on the combination of
        digital and analog channel that are enabled.'''

        self._socket_send(_GET_ALL_SAMPLE_RATES)
        lines = self._socket_recv()

        rates = []
        for line in lines:
            line = line.split(',')
            digital = int(line[0])
            analog = int(line[1])
            rate = (digital, analog)
            rates.append(rate)

        return rates

    def sample_rate_at_least(self, digital_min=0, analog_min=0):
        '''Find a sample rate value that is at least a certain value.

        Find the first sample rate that has a digital sample rate of
        at least digital_min and an analog sample rate of at least
        analog_min.

        The returned value is in the form:

            (digital_sample_rate, analog_sample_rate)
        '''

        sample_rates = self.all_sample_rates
        for sr in sorted(sample_rates):
            if sr[0] >= digital_min and sr[1] >= analog_min:
                return sr

        return None

    def set_sample_rate(self, sample_rate):
        '''Set the capture sample rate.'''

        s = '{0}, {1[0]}, {1[1]}'.format(_SET_SAMPLE_RATE, sample_rate)
        self._socket_send(s)
        self._socket_recv()

    @property
    def sample_rate(self):
        '''Get the current capture sample rate.'''

        self._socket_send(_GET_SAMPLE_RATE)
        sr = self._socket_recv()
        return int(sr[0]), int(sr[1])

    def capture(self):
        '''Start a capture.

        Start a capture and block until it is complete. The duration
        and resolution of the capture can be set using a mix of
        set_num_samples, set_num_seconds and set_sample_rate.
        '''

        self._socket_send('CAPTURE')
        self._socket_recv()

    def close(self):
        '''Close the connection to Logic.'''

        self._socket_real.close()
        self._socket_real = None
