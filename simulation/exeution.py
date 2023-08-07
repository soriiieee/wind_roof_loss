import os
import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pandas as pd

class MonteCarlo:
    def __init__(self) -> None:
        self.cwd = str(Path(__file__).parent.parent)
        print("start-loop")
        
        # 結果の格納先フォルダを作る
        self.results = []
        self.result_out = os.path.join(self.cwd , "data","02_out","results.csv")
        self.result_png = os.path.join(self.cwd , "data","02_out","results.png")
        os.makedirs(os.path.dirname(self.result_out),exist_ok=True)
        

    def loop_pi(self,epoch=500000):
        """_summary_
        sample function ->https://www.kenschool.jp/blog/?p=7410
        Args:
            f (_object_): 実行する関数
            epoch (int, optional): _description_. Defaults to 1000.
        """
        i=0
        while i < epoch:
            x,y = np.random.rand(), np.random.rand()
            color = "r" if x**2+y**2<=1 else "b"
            self.results.append([x,y,color])
            i+=1
        
        df = pd.DataFrame(self.results,columns = ["x","y","color"])
        df.to_csv(self.result_out,index=False)
        f,ax = plt.subplots(figsize=(10,10))
        ax.scatter(df["x"],df["y"],color=df["color"])
        x_list = np.linspace(0,1,1000)
        y_list = np.sqrt(1-x_list**2)
        ax.plot(x_list,y_list,color="k")
        
        pi_pred = 4 *df[df["color"]=="r"].shape[0]  / len(df)
        ax.set_title("pi pred by MonteCarlo ={}".format(str(pi_pred)))
        f.savefig(self.result_png,bbox_inches="tight")
        print(df["color"].value_counts())
        return 
        
            
        
    def loop(self,f,epoch=1000):
        """_summary_

        Args:
            f (_object_): 実行する関数
            epoch (int, optional): _description_. Defaults to 1000.
        """
        pass
        
        
        
        
        
        
        
        
    