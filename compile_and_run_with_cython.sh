# This transpiles the Python code to C and compiles it with gcc to speed up the execution
# However, this does not suffice for part 2 of day 5

# Explanation of Cython usage:
# https://stackoverflow.com/a/40057634/2278742

# Explanation of gcc optimization options:
# https://stackoverflow.com/a/38511897/2278742
source .venv/bin/activate
PYTHONLIBVER=python$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')$(python3-config --abiflags)
rm solution.*
cython $1/$(ls $1 | grep py) --embed -o solution.c
gcc -Ofast -funroll-loops -march=native $(python3-config --includes) solution.c -o solution.bin $(python3-config --ldflags) -l$PYTHONLIBVER
./solution.bin