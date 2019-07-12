#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import threading
import math
import queue as Queue

#SDI   = 26#or 26 red 21 green
RCLK  = 20
SRCLK = 16
sleepInOut=0.5

x = 4 #Largeur de l'ecran
y = 4 #hauteur de l'ecran
motif0= [[0x00,0x00],[0x01,0x01]]
nbMotif=len(motif0) #nombre de motif affichable
nbShift=0
queue = Queue.Queue()

frequence1=0.5
sleeptime1=0.5
def nbShiftCalculate(x,y):
	global nbShift
	nbShift=int(math.ceil(x*y/8.0))
	#print("nbShift"+str(nbShift))
	return nbShift
nbShiftCalculate(x,y)

def convertToHexa(motifV,x1,y1,frequence2=0.5,sleeptime2=0.5):
	global x
	global y
	global nbMotif
	global nbShift
	global frequence1
	global sleeptime1
	global motif0
	frequence1=frequence2
	sleeptime1=sleeptime2
	x=x1
	y=y1
	nbShift=nbShiftCalculate(x,y)
	global motif
	motif=[[0 for i in range(nbShift)] for j in range(len(motifV))]
	shiftNumber=0
	shiftCpt=0 #max 8 car un shift ne peux pas aller plus loin
	for motifCpt in range(0,len(motifV)):
		shiftNumber=0
		shiftCpt=0
		for absc in range(0,x):
			for ordo in range(0,y):
				if(shiftCpt>7):
					shiftCpt=0
					shiftNumber=shiftNumber+1
				valeur=motifV[motifCpt][absc][ordo]<<shiftCpt
				#print(str(motifCpt)+","+str(shiftNumber))
				motif[motifCpt][shiftNumber]=motif[motifCpt][shiftNumber] | valeur
				shiftCpt=shiftCpt+1
	for testaff1 in range(0,nbMotif):
		valeuraff=""
		for testaff in range(0,nbShift):
			valeuraff=valeuraff+","+str(motif[testaff1][testaff])

	#exemple de resultat
	#motif[0]=[0x00,0x00] #8bit pour toutes les infos du shift
	#motif[1]=[0x00,0x00]
	#motif[2]=[0xf0,0xf0]
	#motif[3]=[0x0f,0x0f]
	print ("motif", motif)
	motif0=motif
	nbMotif=len(motif0)
	print("nbMotif",nbMotif)
	#queue.put(motif)
	return motif

DataOutPut=[26,21]#liste des pin de data, ajout d element pour plus de shift
def setup():
	GPIO.setmode(GPIO.BCM)    # Number GPIOs by its physical location
	for pinSortie in range(0,len(DataOutPut)): 
		GPIO.setup(DataOutPut[pinSortie], GPIO.OUT)
		print("pinSortie",pinSortie,"=",DataOutPut[pinSortie])
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	
	for pinSortie in range(0,len(DataOutPut)): 
		GPIO.output(DataOutPut[pinSortie], GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def theLoop():
	#print("Loop")
	i=1
	nbShift=2
	while True:
		#if queue.empty():
			#pass
		#else:
			#motif2 = queue.get()
			#print ("motif2 is updated ",motif2)
		print("motif2",motif0[i%nbMotif]," nbmotif",nbMotif)
		for bit in range(0,8):
			for line in range(0,nbShift):
				GPIO.output(DataOutPut[line], 0x80 & (motif0[i%nbMotif][line] << bit))
			GPIO.output(SRCLK, GPIO.HIGH)
			time.sleep(0.01)
			GPIO.output(SRCLK, GPIO.LOW)
			time.sleep(0.01)
		GPIO.output(RCLK, GPIO.HIGH)
		time.sleep(0.01)
		GPIO.output(RCLK, GPIO.LOW)
		#print("signal send",motif2)
		time.sleep(0.01)
		waitingDelay1=sleeptime1
		if(i%nbMotif==0):
			waitingDelay1=frequence1
		i += 1  
		time.sleep(waitingDelay1)
		#print("Loop fin")

def destroy():   # When program ending, the function is executed.
	print ("destroy")
	for pinSortie in range(0,len(DataOutPut)):
		GPIO.output(DataOutPut[pinSortie], GPIO.LOW)
	#GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)
	GPIO.cleanup()
	raise SystemExit
def mainFunction():
	GPIO.cleanup()
	setup()
	threading.Timer(0.5,theLoop).start()

##mainFunction()#pour faire tourner uniquement ce fichier
#setup()
#destroy()
#theLoop()

