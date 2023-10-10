


class PID:
    def __init__(self,Kp,Ki,Kd,limits,derivative_filter):
        self._set_point = 0.0
        self._pre_measurement = 0.0
        self._pre_filtered_measurement = 0.0
        self._filtered_measurement = 0.0
        self._intergrated_measurement = 0.0
        self._derivative_filter = derivative_filter
    
    def set_set_point(self,set_point):
        self._set_point = set_point

    def get_val(self,measurement,time_delta):
        
        self._intergrated_measurement += (self._pre_measurement+measurement)/2*
        self._filtered_measurement = measurement*self._derivative_filter + self._filtered_measurement*(self._derivative_filter)




        self._pre_measurement = self._filtered_measurement
