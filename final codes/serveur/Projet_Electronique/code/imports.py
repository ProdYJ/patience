#general imports

import sys
#import smbus2 as smbus#,smbus2
import time
from gpiozero import Button
import smbus as i2cINA
import math

#définition d'objets globaux

I2CbusINA = i2cINA.SMBus(1)


#import other scripts

from INA import *
from MPU_V2 import *
from verin import *
from database import *
from rain import *
from arduino import *
from pump import *
#from picam import *
from Tracker_Solaire import *