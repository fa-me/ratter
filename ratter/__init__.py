__name__ = "ratter"
__version__ = '0.1.0.dev'
__author__ = "Fabian Meyer"
__maintainer__ = "Fabian Meyer"
__email__ = "fabian.meyer@mailbox.org"
__url__ = "https://gitlab.cc-asp.fraunhofer.de/fmeyer/ratter"
__summary__ = """calculate coherent reflection, absorption
and transmission of thin layer stacks"""


from .material import Material
from .layer import Layer
from .stack import Layerstack
from .expressions import as_function_of
from .symbols import LAMBDA_VAC