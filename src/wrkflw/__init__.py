# read version from installed package
from importlib.metadata import version

__version__ = version("wrkflw")

from .wrkflw import Workflow
from .tasks import SleepTask, PythonTask, ShellTask, RTask
