## @ingroup Methods-Missions-Segments-Common
# Noise.py
# 
# Created:  Oct 2020, M. Clarke

# ----------------------------------------------------------------------
#  Update Noise
# ----------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Common
def compute_noise(segment):
    """ Evaluates the radiated noise from an aircraft to an observer or set of observer locations

        Inputs -
            segment.analyses.noise             [Function]

        Outputs
            N/A

        Assumptions -


    """    
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    