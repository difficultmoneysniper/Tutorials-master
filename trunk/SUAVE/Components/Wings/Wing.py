## @ingroup Components-Wings
# Wing.py
# 
# Created:  
# Modified: Sep 2016, E. Botero
#           Jul 2017, M. Clarke
#           Oct 2017, E. Botero
#           Oct 2018, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import SUAVE
from SUAVE.Core import Data, ContainerOrdered
from SUAVE.Components import Component, Lofted_Body, Mass_Properties, Physical_Component
from .Airfoils import Airfoil

import numpy as np

# ------------------------------------------------------------
#   Wing
# ------------------------------------------------------------

## @ingroup Components-Wings
class Wing(Lofted_Body):
    """This class defines the wing in SUAVE

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    None

    Outputs:
    None

    Properties Used:
    N/A
    """      
    def __defaults__(self):
        """This sets the default values of a wing defined in SUAVE.
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """         

        self.tag             = 'wing'
        self.mass_properties = Mass_Properties()
        self.origin          = [[0.0,0.0,0.0]]
        
        self.symmetric                 = True
        self.vertical                  = False
        self.t_tail                    = False
        self.taper                     = 0.0
        self.dihedral                  = 0.0
        self.aspect_ratio              = 0.0
        self.thickness_to_chord        = 0.0
        self.span_efficiency           = 0.9
        self.aerodynamic_center        = [0.0,0.0,0.0]
        self.exposed_root_chord_offset = 0.0
        self.total_length              = 0.0

        self.spans = Data()
        self.spans.projected = 0.0
        self.spans.total     = 0.0
        
        self.areas = Data()
        self.areas.reference = 0.0
        self.areas.exposed   = 0.0
        self.areas.affected  = 0.0
        self.areas.wetted    = 0.0

        self.chords = Data()
        self.chords.mean_aerodynamic = 0.0
        self.chords.mean_geometric   = 0.0
        self.chords.root             = 0.0
        self.chords.tip              = 0.0
        
        self.sweeps               = Data()
        self.sweeps.quarter_chord = 0.0
        self.sweeps.leading_edge  = 0.0
        self.sweeps.half_chord    = 0.0        

        self.twists = Data()
        self.twists.root = 0.0
        self.twists.tip  = 0.0

        self.control_surfaces = Data()
        self.flaps = Data()
        self.flaps.chord      = 0.0
        self.flaps.angle      = 0.0
        self.flaps.span_start = 0.0
        self.flaps.span_end   = 0.0
        self.flaps.type       = None
        self.flaps.area       = 0.0

        self.slats = Data()
        self.slats.chord      = 0.0
        self.slats.angle      = 0.0
        self.slats.span_start = 0.0
        self.slats.span_end   = 0.0
        self.slats.type       = None

        self.high_lift     = False
        self.high_mach     = False
        self.vortex_lift   = False

        self.transition_x_upper = 0.0
        self.transition_x_lower = 0.0
        
        self.dynamic_pressure_ratio = 0.0
        
        self.Airfoil            = Data()
        
        self.non_dimensional_origin = [[0.0,0.0,0.0]]
        self.PGM_compulsory         = False
        self.PGM_characteristics    = ['taper','aspect_ratio','thickness_to_chord','areas.reference','sweeps.quarter_chord','dihedral','non_dimensional_origin[0][0]','non_dimensional_origin[0][1]','non_dimensional_origin[0][2]']
        self.PGM_char_min_bounds    = [0,1.,0.001,0.1,0,0,0,-np.inf,-np.inf]   
        self.PGM_char_max_bounds    = [5.,np.inf,1.0,np.inf,np.inf,np.pi/4,np.inf,np.inf,np.inf]
        #self.Segments               = SUAVE.Components.Wings.Segment_Container()
        self.Segments               = ContainerOrdered()
        self.Fuel_Tanks             = SUAVE.Core.Container()

    def append_segment(self,segment):
        """ Adds a segment to the wing 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return
    
    def append_airfoil(self,airfoil):
        """ Adds an airfoil to the segment 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(airfoil,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Airfoil.append(airfoil)

        return        


    def append_control_surface(self,control_surface):
        """ Adds a component to vehicle 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(control_surface,Data):
            raise Exception('input control surface must be of type Data()')

        # Store data
        self.control_surfaces.append(control_surface)

        return
    
    def append_fuel_tank(self,fuel_tank):
        """ Adds a fuel tank to the wing 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(fuel_tank,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Fuel_Tanks.append(fuel_tank)

        return    
    
class Container(Physical_Component.Container):
    def get_children(self):
        """ Returns the components that can go inside
        
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:
        None
    
        Outputs:
        None
    
        Properties Used:
        N/A
        """       
        from . import Main_Wing
        from . import Vertical_Tail
        from . import Horizontal_Tail
        
        return [Main_Wing,Vertical_Tail,Horizontal_Tail]


# ------------------------------------------------------------
#  Handle Linking
# ------------------------------------------------------------

Wing.Container = Container