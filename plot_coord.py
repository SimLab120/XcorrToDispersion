import pygmt
import pandas as pd

xl_file = "Data/coordinates.csv"

df = pd.read_csv(xl_file,header=0,)
region = [79.31,79.37,30.73,30.76]
rectangle = [[region[0],region[2],region[1],region[3]]]


grid=pygmt.datasets.load_earth_relief(resolution='01s',region=region,registration='gridline',)
print(grid)
inc=[0.000278/2,0.000278/2]
sgrid = pygmt.grdsample(grid,spacing=inc,interpolation='b')
dgrid = pygmt.grdgradient(grid=sgrid,radiance=[270,30.7])

with pygmt.config(MAP_FRAME_TYPE="plain",FONT_ANNOT_PRIMARY="7p"):
	fig = pygmt.Figure()
	fig.grdimage(grid=sgrid,projection="M10c",frame=["WSrt","xa0.02","ya0.01"],cmap='oleron')
	fig.plot(x=df.LONGITUDE,y=df.LATITUDE,style="i0.3c",fill="red",pen="black")
	fig.text(x=df.LONGITUDE,y=df.LATITUDE,text=df.REC_NO)
	
	fig.colorbar(frame=["xa+lElevation","y+lKm"])
	with fig.inset(position="jBL+o0.1c",box="+gwhite+pblack",region=[72,86.5,25,34],projection="M1c"):
		fig.coast(area_thresh=10000,land="gray",water="blue",borders="a"+"/"+"0.1p,black,solid")
		fig.plot(data=rectangle,style="r+s",pen="1p,blue")
		
	fig.show()
	fig.savefig('Station_map.png')

