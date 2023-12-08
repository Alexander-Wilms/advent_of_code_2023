# Advent of Code 2023

Create requirements.txt:
```
pipreqs --force --mode no-pin --ignore .venv
```

Create venv to install packages via pip, separate from distro's Python packages:
```
python3.11 -m venv .venv
./.venv/bin/pip3 install -U mypy
./.venv/bin/pip3 install -r requirements.txt
```

Run tests:
```
./.venv/bin/pytest -vrx
```

Use Cython to compile Python to C in order to improve performance:
```
./compile_and_run_with_cython.sh day_08
```
