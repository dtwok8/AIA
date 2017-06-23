#set terminal svg dashed
#set output "/home/kate/NetBeansProjects/bakalarka/dokumentace/gnuplot/haar_raw.svg"
#Set pretty PostScript output and filename
#set terminal postscript enhanced color lw 2 "Times-Roman" 20
# set output "haar.svg"
set terminal svg
set output "haar.svg"

 #Set y axis limits so the plot doesn't go right to the edges of the graph
 set yrange [-1.5:1.5]
 #Set x axis limits so the first and last points are hidden
 set xrange [-0.5:1.5]

 #No legend needed
 set nokey

 #Add lightly-colored axis lines
 set yzeroaxis linetype 1 lc "#7f7f7f"
 set ytics 1
 set xzeroaxis linetype 1 lc "#7f7f7f"
 set xtics 1

 #set style line 1 lc rgb '#0000ff' # ls 1 pt 7 

 #Plot as lines and also points

 set style line 2 lw 2 dashtype "-  " lc rgb '#0000ff' pt 6 ps 2 
 set style line 6 lw 2 lt 1 lc rgb '#0000ff' pt 6 ps 2 
 set style line 7 lw 2 lt 1 lc rgb '#0000ff' pt 7 ps 2 

 plot "<(sed -n '2,3p' haar.dat)" with linespoints ls 6, \
	 "<(sed -n '3,4p' haar.dat)" with linespoints ls 2, \
	"<(sed -n '4p' haar.dat)" with linespoints ls 7, \
	"<(sed -n '4,5p' haar.dat)" with linespoints ls 6, \
	"<(sed -n '5,6p' haar.dat)" with linespoints ls 2, \
	"<(sed -n '6p' haar.dat)" with linespoints ls 7, \
	"<(sed -n '6,7p' haar.dat)" with linespoints ls 6, \
	"<(sed -n '7,8p' haar.dat)" with linespoints ls 2, \
	"<(sed -n '8p' haar.dat)" with linespoints ls 7, \
	"<(sed -n '8,9p' haar.dat)" with linespoints ls 6, \

 #plot "<(sed -n '2,3p' haar.dat)" with lines lc rgb '#0000ff', "" with points ls 1 pt 6 lc rgb '#0060ad', \
 #"<(sed -n '3,4p' haar.dat)" with lines lc rgb '#2e8b57', "" with points ls 1 pt 7 lc rgb '#0060ad'

 #plot sin(x)
 #with points:
 #1 = color red (linestyle 1?)
 #6 = point style 6 (render as circles in PostScript)
  




