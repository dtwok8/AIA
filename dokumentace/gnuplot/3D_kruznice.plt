set terminal svg
set output "/home/kate/NetBeansProjects/bakalarka/Deskriptor/doc/gnuplot/3D_kruznice_raw.svg"

set grid
set nokey
set view 60,120 #otoceni nahledu

#plot [-3.14:3.14] sin(x), sin(x) with impulses
#plot sin(x)


set border 0

set xlabel "x" offset -9,-3,0
set xzeroaxis
set xtics axis
set xrange [0:10]
#set arrow 1 from -9,0 to -10,0
#set arrow 2 from  9,0 to  10,0

set ylabel "y" offset 17,-2,0 
set yzeroaxis
set ytics axis
set yrange [-10:10]
#set arrow 3 from 0,-.9 to 0,-1
#set arrow 4 from 0,.9  to 0,1

set zlabel "z" offset 0,5,0 
set zzeroaxis
set ztics axis
set zrange [0:10]
#set arrow 5 from -9,0 to -10,0
#set arrow 6 from 9,0 to 10,0

set arrow 1 from 0,0,0 to 4,9,8 filled back lw 3 lc rgb "blue"
set arrow 2 from 0,0,0 to 4,9,0 filled back lw 3 lc rgb "red"
#set arrow 2 from 0,0,0 to 4,7,0 filled back lw 3 lc rgb "red"
#set arrow 3 from 0,0,0 to 0,7,0 filled back lw 3 lc rgb "green"

set object 1 circle at 0,0 size 5.5 arc [0 : 120] fc rgb "slategray" fs transparent solid 0.3 dt 2 
set object 2 circle at 0,0 size 5.5 arc [120 : 240] fc rgb "seagreen" fs transparent solid 0.3 dt 2
set object 3 circle at 0,0 size 5.5 arc [240 : 360] fc rgb "khaki" fs transparent solid 0.3 dt 2 

R=5 
d=4 
e=6 
c=15 
set ticslevel 0
f1(x,y) = x + y

#set zrange [0:2]
# Radius
r = 1.0
fx(x,y) = r*cos(x)*cos(y)
fy(x,y) = r*cos(x)*sin(y)

fk(x,y) = r*cos(x) + r*sin(y) 
fkk(x,y)= (x-3)*x + (y-3)*y - 2
fz(x)   = r*sin(x)
f3(x,y) = (y > 0 && y < 0) ? 5 :1/0
f4(y,z) = (y > -pi/2 && y < pi/2) ? y*y + z*z :1/0 #sin(y) : 1/0

#plot sin(x)
splot NaN#f3(x,y)

  




