set terminal svg
set output "/home/kate/Plocha/2D_kruznice.svg"

set grid
set nokey
set size square # stejnej pomer na x a y

set border 0

set xlabel "x" offset 28,12.5
set xzeroaxis
set xtics axis
set xrange [-7:7]

set ylabel 'y' offset 24,12 rotate by 0
set yzeroaxis
set ytics axis
set yrange [-7:7]

#set ticslevel 0
set tics font "Helvetica,10"

set object 1 circle at 0,0 size 5.5 arc [0 : 120] fc rgb "slategray" fs transparent solid 0.3 dt 2 
set object 2 circle at 0,0 size 5.5 arc [120 : 240] fc rgb "seagreen" fs transparent solid 0.3 dt 2
set object 3 circle at 0,0 size 5.5 arc [240 : 360] fc rgb "khaki" fs transparent solid 0.3 dt 2 

set arrow 1 from 0,0 to -2,-5 filled back lw 3 lc rgb "blue"  
set label "[ -2 , -5 ]" at -5,-5.5

fz(x) = (x == 0) ? sin(x) : 1/0
plot fz(x) 




