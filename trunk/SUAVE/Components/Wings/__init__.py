## @defgroup Components-Wings Wings
# @ingroup Components
#
# __init__.py
# 
# Created:  
# Modified: Feb 2016, T. MacDonald

# classes
from .Wing import Wing
from .Control_Surface import Control_Surface
from .Main_Wing import Main_Wing, Segment_Container
from .Vertical_Tail import Vertical_Tail
from .Horizontal_Tail import Horizontal_Tail
from .Segment import Segment#, Segment_Container

# packages
from . import Airfoils

