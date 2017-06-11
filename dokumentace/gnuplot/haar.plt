set terminal svg
set output "/home/kate/NetBeansProjects/bakalarka/dokumentace/gnuplot/haar_raw.svg"

set grid
set nokey
set view 60,120 #otoceni nahledu

#plot [-3.14:3.14] sin(x), sin(x) with impulses
#plot sin(x)


set border 0


#set arrow 1 from -1,0 to 1,0 filled back lw 3 lc rgb "grey"
#set arrow 2 from 0,0,0 to 8,4,0 filled back lw 3 lc rgb "red"
#set arrow 3 from 0,0,0 to 12,12,10 filled back lw 3 lc rgb "green"

#set arrow 4 from 0,0,0 to 0,-3,5 filled back lw 3 lc rgb "blue"
#set arrow 5 from 0,0,0 to 0,-4,2 filled back lw 3 lc rgb "red"
#set arrow 6 from 0,0,0 to 0,-7,7 filled back lw 3 lc rgb "green"

haar(x) = (0 < x < 1/2) ? 1 : 0

set ticslevel 0

f(x)=x<=1 ? -(x-1)**2+1 :  x>7 ? (-48)*sin(240)+1+0.5*x : (-(x-1)**2+1)*sin(30*x)+1
plot f(x)
  




