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
    
    

class WindLoadModel2:
    def __init__(self,config):
        
        self.yane_shape = config["yane"] #kirizuma/yosemuune/katanagare/nokogiri/enko
        self.
        
    
    def get_L2(self,U10_min,H,sodo,A):
        """
        w = q x Cf x A
        Args:
            U10_min (_type_): _description_
        """
        E = self._E(H,sodo)
        Cf = self._Cf()
        
        L = 0.6 * E  * (U10_min)**2 * Cf * A
        
    
    def _E(self,H,sodo=1):
        Er_DICT ={
            # https://www.kenken.go.jp/japanese/research/lecture/h16/slide/06-1/ref/No6.htm
            "1" : [5, 250, 0.1],
            "2" : [5, 350, 0.15],
            "3" : [5, 450, 0.2],
            "4" : [10, 550, 0.27],
        }          
        ## Er --
        Zb,Zg,alpha = Er_DICT[str(sodo)]
        if H<Zb:
            Er = 1.7 * (Zb/Zg) ** alpha
        else:
            Er = 1.7 * (H/Zg) ** alpha
        ## Gf --
        Gr = self._Gf(H,sodo)
        return Er**2 * Gr
    
    def _Gf(self,H,sodo=1):
        Gf_DICT ={
            # https://www.kenken.go.jp/japanese/research/lecture/h16/slide/06-1/ref/No6.htm
            "1" : [2.0, 1.8],
            "2" : [2.2, 2.0],
            "3" : [2.5, 2.1],
            "4" : [3.1, 2.3],
        }
        v1 , v2 = Gf_DICT[str(sodo)]
        
        if H<10:
            return v1
        if H>40:
            return v2
        W = [abs(H-10),abs(H-40)]
        return (v1 * W[0] + v2*W[1]) / (W[0] + W[1])

    def _Cf(self,H,sodo,shape,point,slope,isInner=False):
        # ref:
            # https://www.kenken.go.jp/japanese/research/lecture/h16/slide/06-1/ref/No1.htm
        
        
        """
        
        2 　屋根ふき材に対するピーク風力係数は、次の各号に掲げる屋根の形式に応じ、それぞれ当該各号に定めるところにより計算した数値とする。
        
        一　切妻屋根面、片流れ屋根面及びのこぎり屋根面　イに規定するピーク外圧係数（屋外から当該部分を垂直に押す方向を正とする。以下同じ）
        からロに規定するピーク内庄係数（屋内から当該部分を垂直に押す方向を正とする。以下同じ）を減じた値とする。
        
        イ　ピーク外圧係数は、正の場合にあっては次の表1に規定するCpeに次の表2に規定するGpeを乗じて得た数値とし、
        負の場合にあっては次の表3に規定する数値とする。
        ロ　ピーク内圧係数は，次の表6に規定する数値とする。
        二　円弧屋根面　イに規定するピーク外圧係数からロに規定するピーク内庄係数を減じた値とする。
        イ　ピーク外圧係数は、正の場合にあっては次の表4に規定するCpeに次の表2に規定するGpeを乗じて得た数値とし、
        負の場合にあっては次の表5に規定する数値とする。
        ロ　ピーク内圧係数は次の表6に規定する数値とする。
        三　独立上家　平成12年建設省告示第1454号第3に規定する風力係数に、当該風力係数が零以上の場合にあっては次の表2に、
        零未満の場合にあっては次の表7にそれぞれ規定するGpeを乗じて得た数値とすること。
        
        """
        Gpe2_DICT ={
            # https://www.kenken.go.jp/japanese/research/lecture/h16/slide/06-1/ref/No6.htm
            "1" : [2.2, 1.9],
            "2" : [2.6, 2.1],
            "3" : [3.1, 2.3],
            "4" : [3.1, 2.3],
        }
        
        
        def get_Cpe1(slope):
            if slope<10: return 0      
            if slope<30: return 0.2     
            if slope<45: return 0.4 
            if slope<90: return 0.8   
            
        def get_Cpe2(H,sodo):
            v1,v2 = Gpe2_DICT(str(sodo))
            if H<5:
                return v1
            if H>40:
                return v2
            W = [abs(H-10),abs(H-40)]
            return (v1 * W[0] + v2*W[1]) / (W[0] + W[1])
        
        def get_Cpi(Cpe,mode="open"):
            
            if mode == "open":
                return 1.5
            if mode == "close":
                if Cpe>0:    
                    return -0.5
            
        # 1.ピーク外圧係数
        
        Cpe1 = get_Cpe1(slope)
        Cpe2 = get_Cpe2(H,sodo)
        Cpe = Cpe1 * Cpe2
        
        Cpi = get_Cpi(Cpe,"open")
        
        
        
        # 2.ピーク内圧係数
        
        
        
        return 
        
        