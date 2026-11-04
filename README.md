# NexusPC

## Setup

Install the Python dependencies:

```shell
python -m pip install -r requirements.txt
```

CPU and GPU sensor readings use
[PyLibreHardwareMonitor](https://pypi.org/project/PyLibreHardwareMonitor/),
which supplies the LibreHardwareMonitor integration through its package
dependencies. A separate `LibreHardwareMonitorLib.dll` in the application
folder is not required.
