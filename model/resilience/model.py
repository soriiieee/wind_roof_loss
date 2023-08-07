import os
import sys
import json



class ResistanceModel:
    
    def __init__(self,config,logger = None):
        # 住宅の密度
        self.config = config
        self.logger = logger
        
    
    def set_params(self):
        with open(self.config["resilience"]["buld_json"],"r") as f:
            data = json.load(f)
        
        print(data)
        exit()
        
        
    def get_01roof_R(self,F,slope,attach_type:dict):
        """_summary_

        Args:
            F (_type_): 屋根荷重
            slope (_type_): _屋根slope角度
            attach_type(_dict_) : 結合カテゴリと、結合方法ごと(2009,喜)

        Returns:
            _type_: _description_
        """
        
        # R,g,rt + 
        # theta = np.deg2rad(slope)
        atache_power = self.get_
        R = F * np.cos(np.deg2rad(slope)) 
        return L
    
    def get_atach_power(self,key,value):
        if 
        