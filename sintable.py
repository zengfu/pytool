import numpy as np
import math
point=np.linspace(0,np.pi,100)
data=(np.sin(point)*1023)
#data=data.astype(int)
np.savetxt('sintable.txt',data,fmt='%f,')
