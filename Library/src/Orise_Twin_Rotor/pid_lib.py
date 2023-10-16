from typing import Tuple


class PID:
    '''
    PID controller
    '''
    def __init__(self,Kp:float,Ki:float,Kd:float,limits:Tuple[float,float],derivative_filter_omega:float=float('inf'),derivative_on_measurement:bool=False):
        ''''
        limits - Limits on the output of the PID controller based on the limits of the inputs of the control systme  Tuple of floats (a,b) where a <= b
        derivative_filter_omega = omega for low pass derivative filter on derivative make sure it is larger than half the average sampling time 
        derivaitve_on_measurement = Enable derivative on measurement instead of error
        '''
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd

        self._derivative_filter_omega = derivative_filter_omega
        self._tau = 1/self._derivative_filter_omega
        self._derivative_on_measurement = derivative_on_measurement
        self._limits = limits
        assert(self._limits[0] <= self._limits[1])

        self._set_point = 0.0

        self._pre_i = 0.0
        self._pre_d = 0.0
        self._pre_e = 0.0
        self._pre_measurement = 0.0

    def set_set_point(self,set_point:float):
        self._set_point = set_point

    @property
    def parameteres(self):
        return (self._Kp,self._Ki,self._Kd,self._derivative_filter_omega)

    def set_parameteres(self,Kp:float,Ki:float,Kd:float):
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd

    def clamp(self,val):
        '''
        clamp the value between the limits
        '''
        if(val < self._limits[0]):
            return self._limits[0]
        if(val > self._limits[1]):
            return self._limits[1]
        return val

    def get_val(self,measurement:float,time_delta:float):
        '''
        p[n] = K_p*e[n]
        i[n] = (Ki*T/2)*(e[n]+e[n-1])+i[n-1]
        d[n] = (2*Kd)/(2*tau+T)*(e[n]-e[n-1])+(2*tau-T)/(2*tau+T)*d[n-1]
        '''
        e = self._set_point-measurement #error
        T = time_delta 
        tau = self._tau if (self._tau*2 > T) else T/2

        #Proportional 
        p =  self._Kp*e

        #Integral
        i = (self._Ki*T)/2*(e+self._pre_e)+self._pre_i

        #derivative with low pass
        d = (2*self._Kd)/(2*tau+T)*(e - self._pre_e)+(2*tau-T)/(2*tau+T)*self._pre_d

        if(self._derivative_on_measurement):
            #derivative on measurement with low pass
            d = (2*self._Kd)/(2*tau+T)* (-(measurement-self._pre_measurement))+(2*tau-T)/(2*tau+T)*self._pre_d

        output = p+i+d

        self._pre_i = i
        self._pre_d = d 
        self._pre_e = e
        self._pre_measurement = measurement

        return self.clamp(output)

    def __call__(self,measurement:float,time_delta:float):
        '''
        Return the calculated control value
        '''
        return self.get_val(measurement,time_delta)






