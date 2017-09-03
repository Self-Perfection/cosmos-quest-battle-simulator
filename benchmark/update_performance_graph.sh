#!/bin/sh -e

CMDLINE='../monsters.py compose_team -c 57700 -m 5 f5a5f4a3f2a1'
BENCHMARK_DAT_FILE='current_performance.dat'

: > "$BENCHMARK_DAT_FILE"

for interpreter in 'python2' 'python3' 'pypy' 'pypy3'; do
    if ! command -v "$interpreter" >/dev/null; then
        echo "$interpreter not found. Skipping"
        continue
    fi
    version=$("$interpreter" --version 2>&1 | awk 'END{print $2}')
    printf '"%s %s"\t' "$interpreter" "$version" | tee -a "$BENCHMARK_DAT_FILE"
    /usr/bin/time --format='%U'  "$interpreter" $CMDLINE 3>&2 2>&1 1>/dev/null | tail -1 | tee -a "$BENCHMARK_DAT_FILE"
done

CPUMODEL=$(grep -m1 'model name' /proc/cpuinfo |cut -d: -f2)
for t in svg; do
    gnuplot << EOF
    set terminal $t
    set output "current_performance.$t"

    set title "Running time of '$CMDLINE'\non${CPUMODEL} in seconds" noenhanced
    set style fill solid
    set boxwidth 0.8
    set yrange[0:]

    plot "current_performance.dat" using 2:xtic(1) with boxes
EOF
done

#Lossleless optimization of png compression
if [ -r 'current_performance.png']; then
    optipng -i 0 -o7 current_performance.png
    advdef -z4 current_performance.png
fi
