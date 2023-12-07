# This transpiles the Python code to C and compiles it with gcc to speed up the execution
# However, this does not suffice for part 2 of day 5
# https://stackoverflow.com/a/40057634/2278742

PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)
cython day_05/you_give_a_seed_a_fertilizer.py --embed
gcc -O3 $(python3-config --includes) day_05/you_give_a_seed_a_fertilizer.c -o day_05/you_give_a_seed_a_fertilizer $(python3-config --ldflags) -l$PYTHONLIBVER
day_05/you_give_a_seed_a_fertilizer