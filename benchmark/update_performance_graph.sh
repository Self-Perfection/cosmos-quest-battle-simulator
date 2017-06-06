#!/bin/sh -e

CMDLINE='../monsters.py compose_team -c 57700 -m 5 f5a5f4a3f2a1'
BENCHMARK_DAT_FILE='current_performance.dat'

: > "$BENCHMARK_DAT_FILE"

for interpreter in 'python2' 'python3' 'pypy' 'pypy3'; do
    version=$("$interpreter" --version 2>&1 | awk 'END{print $2}')
    printf '"%s %s"\t' "$interpreter" "$version" | tee -a "$BENCHMARK_DAT_FILE"
    /usr/bin/time --format='%U'  "$interpreter" $CMDLINE 3>&2 2>&1 1>/dev/null | tail -1 | tee -a "$BENCHMARK_DAT_FILE"
done

CPUMODEL=$(grep -m1 'model name' /proc/cpuinfo |cut -d: -f2)
gnuplot << EOF
set terminal svg
set output "current_performance.svg"

set title "Running time of '$CMDLINE'\non${CPUMODEL} in seconds" noenhanced
set style fill solid
set boxwidth 0.8
set yrange[0:]

plot "current_performance.dat" using 2:xtic(1) with boxes
EOF
