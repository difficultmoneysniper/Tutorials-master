# Motor.py
#
# Created:  Jun 2014, E. Botero
# Modified: Jan 2016, T. MacDonald

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import SUAVE

# package imports
import numpy as np
from SUAVE.Components.Energy.Energy_Component import Energy_Component

# ----------------------------------------------------------------------
#  Motor Class
# ----------------------------------------------------------------------
    
class Motor(Energy_Component):
    
    def __defaults__(self):
        
        self.resistance         = 0.0
        self.no_load_current    = 0.0
        self.speed_constant     = 0.0
        self.propeller_radius   = 0.0
        self.propeller_Cp       = 0.0
        self.gear_ratio         = 0.0
        self.gearbox_efficiency = 0.0
        self.expected_current   = 0.0
        self.interpolated_func  = None
    
    def omega(self,conditions):
        """ The motor's rotation rate
            
            Inputs:
                Motor resistance - in ohms
                Motor zeros load current - in amps
                Motor Kv - in rad/s/volt
                Propeller radius - in meters
                Propeller Cp - power coefficient
                Freestream velocity - m/s
                Freestream dynamic pressure - kg/m/s^2
                
            Outputs:
                The motor's rotation rate
               
            Assumptions:
                Cp is not a function of rpm or RE
               
        """
        # Unpack
        V     = conditions.freestream.velocity[:,0,None]
        rho   = conditions.freestream.density[:,0,None]
        Cp    = conditions.propulsion.propeller_power_coefficient[:,0,None]
        Res   = self.resistance
        etaG  = self.gearbox_efficiency
        exp_i = self.expected_current
        io    = self.no_load_current + exp_i*(1-etaG)
        G     = self.gear_ratio
        Kv    = self.speed_constant/G
        R     = self.propeller_radius
        v     = self.inputs.voltage
    
        # Omega
        # This is solved by setting the torque of the motor equal to the torque of the prop
        # It assumes that the Cp is constant
        omega1  =   ((np.pi**(3./2.))*((- 16.*Cp*io*rho*(Kv*Kv*Kv)*(R*R*R*R*R)*(Res*Res) +
                    16.*Cp*rho*v*(Kv*Kv*Kv)*(R*R*R*R*R)*Res + (np.pi*np.pi*np.pi))**(0.5) - 
                    np.pi**(3./2.)))/(8.*Cp*(Kv*Kv)*(R*R*R*R*R)*Res*rho)
        omega1[np.isnan(omega1)] = 0.0
        
        Q = ((v-omega1/Kv)/Res -io)/Kv
        # store to outputs
       
        #P = Q*omega1
        
        self.outputs.torque = Q
        self.outputs.omega = omega1

        return omega1
    
    def torque(self,conditions):        
        Res   = self.resistance
        etaG  = self.gearbox_efficiency
        exp_i = self.expected_current
        io    = self.no_load_current + exp_i*(1-etaG)
        G     = self.gear_ratio
        Kv    = self.speed_constant/G
        v     = self.inputs.voltage
        omega = self.inputs.omega
        
        # Torque
        Q = ((v-omega1/Kv)/Res -io)/Kv
        
        self.outputs.torque = Q
        self.outputs.omega  = omega
    
        return Q
    
    def voltage_current(self,conditions):
        Res   = self.resistance
        etaG  = self.gearbox_efficiency
        exp_i = self.expected_current
        io    = self.no_load_current + exp_i*(1-etaG)
        G     = self.gear_ratio
        kv    = self.speed_constant/G
        Q     = self.inputs.torque
        omega = self.inputs.omega        
        
        v = (Q*kv+io)*Res + omega/kv
        i = (v-omega/kv)/Res
        
        self.outputs.voltage = v
        self.outputs.current = i
        
        return
    
    
    def current(self,conditions):
        """ The motor's current
            
            Inputs:
                Motor resistance - in ohms
                Motor Kv - in rad/s/volt
                Voltage - volts
                Gear ratio - ~
                Rotation rate - rad/s
                
            Outputs:
                The motor's current
               
            Assumptions:
                Cp is invariant
               
        """    
        
        # Unpack
        G     = self.gear_ratio
        Kv    = self.speed_constant
        Res   = self.resistance
        v     = self.inputs.voltage
        omeg  = self.outputs.omega*G
        etaG  = self.gearbox_efficiency
        exp_i = self.expected_current
        io    = self.no_load_current + exp_i*(1-etaG)
        
        i=(v-omeg/Kv)/Res
        
        # This line means the motor cannot recharge the battery
        i[i < 0.0] = 0.0

        # Pack
        self.outputs.current = i
          
        etam=(1-io/i)*(1-i*Res/v)
        conditions.propulsion.etam = etam
        
        return i

    def load_csv_data(self,file_name):
        
        # Load the CSV file
        my_data = np.genfromtxt(file_name, delimiter=',')
        
        x = my_data[11:,:2] # Speed and torque
        z = my_data[11:,2]  # Efficiency
        
        f = scipy.interpolate.CloughTocher2DInterpolator(xy,z)
        
        # Keep the interpolated function
        self.interpolated_func = f
        
        return f
        
    def power_from_fit(self,conditions):
        
        # Unpack
        omega  = self.inputs.omega
        torque = self.inputs.torque
        func   = self.interpolated_func
        
        # Find the values
        efficiency = func(omega,torque)
        
        # Ensure the values make some sense
        efficiency[efficiency<0.] = 0.
        efficiency[efficiency>1.] = 1.
        
        # Mechanical Power
        mech_power = rpm*torque
        
        # Electrical Power
        elec_power = mech_power/efficiency
        
        # Pack the outputs
        self.outputs.efficiency = efficiency
        self.outputs.power_in   = elec_power
        
        return elec_power