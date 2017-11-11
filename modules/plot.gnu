set term png

set output "plot.png"

set yrange[0:1]
set ytics 0.1

set xlabel 'iterations'
set ylabel 'errors'

plot 'plot' using 1:2 title 'training error' with lines, 'plot' using 1:3 title 'generalization error' with lines
