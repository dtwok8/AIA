set terminal svg
set output "/home/kate/NetBeansProjects/bakalarka/Deskriptor/doc/gnuplot/soucet_vektoru_raw.svg"

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
set yrange [0:10]
#set arrow 3 from 0,-.9 to 0,-1
#set arrow 4 from 0,.9  to 0,1

set zlabel "z" offset 0,5,0 
set zzeroaxis
set ztics axis
set zrange [0:10]
#set arrow 5 from -9,0 to -10,0
#set arrow 6 from 9,0 to 10,0

set arrow 1 from 0,0,0 to 4,8,10 filled back lw 3 lc rgb "blue"
set arrow 2 from 0,0,0 to 8,4,0 filled back lw 3 lc rgb "red"
set arrow 3 from 0,0,0 to 12,12,10 filled back lw 3 lc rgb "green"

#set arrow 4 from 0,0,0 to 0,-3,5 filled back lw 3 lc rgb "blue"
#set arrow 5 from 0,0,0 to 0,-4,2 filled back lw 3 lc rgb "red"
#set arrow 6 from 0,0,0 to 0,-7,7 filled back lw 3 lc rgb "green"


set ticslevel 0

#plot sin(x)
splot NaN#f3(x,y)

  




