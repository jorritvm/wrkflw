# read version from installed package
from wrkflw import *
from importlib.metadata import version
__version__ = version("wrkflw")