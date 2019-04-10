from angles import Angle, RA_angle, Dec_angle, Deg10, Hour_angle
from locales import kittpeak
import matplotlib.pyplot as plt
import json
import math
from skymap_gui import SkymapApp
from Tkinter import Tk, Frame
from astrolib2 import astroobj
import random


def dist( ra1, dec1, ra2, dec2):
	
	return Angle( math.sqrt( (ra2 - ra1)*(ra2 - ra1)+(dec2 - dec1)*(dec2 - dec1) ) )



def doFK5grid( fk5cat, place, skymap=False ):
	obs = []
	script_file = open('pr_03_04_15.txt','w')
	if skymap:
		root = Tk()
		main = Frame( root )
		main.pack()
		sky=SkymapApp(main, place, 800)
		
		sky.updateMain()
		sky.pack()
		

	ups = []
	
	for obj in fk5cat: 
		ra, dec = RA_angle( str( obj['ra'] ) ), Dec_angle( str( obj['dec'] ) )
		

		el, az = place.eq2hor( ra, dec )
		thisEl = el.deg10

		if el.deg10 > 90:
			thisEl = el.deg10-360
		
		if thisEl > 85 or thisEl < 35:
			pass
	
		else:
			ups.append(obj)

	del fk5cat		

	az_step = [8, 24, 8, 24, 48, 48, 48  ]

	counter = 0
	counter2=0
	alt_num=0
	
	dither = [-2,2]
	
	
	for alt in [Deg10(num + (random.random()*4)-2 ) for num in range(35, 85, 8)]:
	
		for az in [Deg10( num + (random.random()*4)-2 ) for num in range(0,360, az_step[alt_num])]:

			
			ds = []	
			ra,dec = place.hor2eq(alt,az)
			close_ra, close_dec = Deg10(359), Deg10(89)
			smallest = 370
			done_flag = False
			ii = 0
			for obj in []:#ups:
			
				objra = RA_angle(str( obj['ra'] ) )
				objdec = Dec_angle( str( obj['dec'] ) )
			
				d = dist( ra, dec, objra, objdec )

			
				if d.deg10 < 0.5:
					closest_ra = objra
					closest_dec = objdec
					name = obj['fk5no']
					theObj = obj
					done_flag = True
					break
				
				elif d.deg10 < smallest:
					closest_ra = objra
					closest_dec = objdec
					smallest = d.deg10
					name = obj['fk5no']
					theObj = obj
					done_flag = True
			
				ii+=1
		
			#ups.pop( ups.index(theObj) )
		
			#star_alt, star_az = place.eq2hor( closest_ra, closest_dec )
			#print star_alt, star_az
			#alts.append( star_alt.deg10 )
			#azs.append( star_az.deg10 )
		

			#place.updatetime(50)
			#ras.append( closest_ra.deg10 )
			O = astroobj('pr{0:04d}'.format(counter2), ra, dec )
			place.updatetime(50)
			obs.append(O)
			#if skymap:	sky.addObj( O )
			thisEL,ThisAz = place.eq2hor( O.ra, O.dec )
		
			cmd = "obs 5.0 object '{name}' 1 V {ra} {dec} 2000.0\r\n"
			script_file.write( cmd.format(name=O.name, ra=O.ra.Format('hours', ''), dec=O.dec.Format('degarc180', '')[:-1]) )
		

			#dec = closest_dec.deg10

		
			counter2+=1
		counter+=1
		alt_num+=1
	script_file.close()
	print counter2
	if skymap:
		sky.place.updatetime( -50*158 )
		for ob in obs:
			
			sky.addObj(ob)
		
		root.mainloop()
	

def dodarks(count=5):
	cmd = 'obs 0.0 zero foo{names:04} 5'
	print cmd
	
	
with open('fk5.json') as fp:
	fk5cat = json.load( fp )

p=kittpeak()
print p.stardate.UT.hours
p.updatetime(1*60)
print p.stardate.UT.hours
doFK5grid(fk5cat, kittpeak(), True)


