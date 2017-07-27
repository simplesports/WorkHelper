import math
#This is where I will define all the Global veriables
global filename
global Loads
Loads = {'LoadName' : [], 'Voltage': [], 'Wattage': [], 'PF': [], 'VA': [], 'Utility':[]}
global wireSizeCircularMill
wireSizeCircularMill = [4110,6530,10380,16510,26240,41740,52620,66360,83690,105600,133100,167800,211600,250000,300000,350000,400000,500000,600000,700000,750000,1000000]
global Voltage_Drop_Panels # this is the current circuit for voltage drop UI
Voltage_Drop_Panels = {}
global phase1
phase1 = (1,2,5,6,9,10,13,14,17,18,21,22,25,26,29,30,33,34,37,38,41,42,45,46,49,50,53,54,57,58,61,62,65,66,69,70,73,74,77,78)
global phase2
phase2 = (3,4,7,8,11,12,15,16,19,20,23,24,27,28,31,32,35,36,39,40,43,44,47,48,51,52,55,56,59,60,63,64,67,68,71,72,75,76,79,80)
