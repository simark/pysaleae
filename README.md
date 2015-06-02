# pysaleae

## Description

**pysaleae** is a small library designed to communicate with
[Saleae](https://www.saleae.com/) Logic's scripting socket interface. It
can be used to automate the capture, export and analysis part of an
experimentation which otherwise can be a very repetitive task.

## Example

Here is a small Python session showing the basic usage of pysaleae. You
can reproduce it by launching Logic in simulation mode (launching it
without any Saleae device connected).

    >>> from saleae import logic
    >>> l = logic.Logic()
    >>> l.connected_devices
    [Device(num=1, name="Logic 4", kind="LOGIC_4_DEVICE", dev_id="0x54abc57e", active=False),
     Device(num=2, name="Logic 8", kind="LOGIC_8_DEVICE", dev_id="0x6a7563b9", active=False),
     Device(num=3, name="Logic Pro 8", kind="LOGIC_PRO_8_DEVICE", dev_id="0x850156", active=False),
     Device(num=4, name="Logic Pro 16", kind="LOGIC_PRO_16_DEVICE", dev_id="0x25a5eed5", active=True)]
    >>> l.all_sample_rates
    [(50000000, 6250000),
     (50000000, 3125000),
     (6250000, 1562500),
     (6250000, 781250),
     (50000000, 125000),
     (50000000, 5000),
     (50000000, 1000),
     (50000000, 100),
     (50000000, 10)]
    >>> l.set_sample_rate((6250000, 781250))
    >>> l.set_num_samples(6250000)
    >>> l.set_num_seconds(1)
    >>> l.capture()
    
## TODO

* Add/Remove analyzers (by loading a .logicsettings file using the the
  load_file command).
* Capture to file and export to file.

## Disclaimer

pysaleae is not affiliated in any way with Saleae. Please report any bug
found in Saleae Logic to Saleae directly, and any bug found in pysaleae
by raising an issue on the Github project page.
