# The gust wind load L is defined using a 3-s gust wind. It is
# assumed to be modeled as
# L 1⁄4 ð1=2ÞρaU210 minð1þ2IuGaÞðCp;out Cp;inÞ;



class WindLoadModel:
    
    def __init__(self,**kwargs):
        #the air density
        self.roh_a = kwargs["roh_a"] if kwargs["roh_a"] else 1.29 #[kg/m3]
        # 
        self.I_u = kwargs["I_u"] if kwargs["I_u"] else 0.1 #?
        self.G_a = kwargs["G_a"] if kwargs["G_a"] else 0.125 #"ln(3.2)"

        #
        self.C_out = kwargs["C_out"] if kwargs["C_out"] else 1
        self.C_in = kwargs["C_in"] if kwargs["C_in"] else 0
    
    def get_L(self,U10_min):
        
        L = (1/2) * self.roh_a * (U10_min**2) * (1 + 2* self.I_u * self.G_a) * (self.C_out - self.C_in)
        return L
    
        