Project description
Testing code to generate primes through the utilization of prime-distanced symmetry radiating from a prime-factored compound.

Notes
Code works but is slower than the pythonic 1-liner sieve method included as a function in the code. Not tested beyond a target of 1.5E6 (taking about 22 minutes on one 3.8 GHz core. The ls3 file is just a list of primes used for validation.

I’ve chosen to generate base compounds using sequential primes as it seems to fill prime gaps with reasonable effectiveness but the generation of primes below target is not absolute as overlap from these compound numbers in each cycle is not perfect. The amount of gaps does seem to be low for in tests, and lower primes do get discovered as higher ones are generated (10 at 1.5E5, 16 at 1.5E6). Of course, primes up to x2 above target are found too but gaps are greater here due to much reduced overlaps. 

There some remnants of (optimization) test code, I couldn’t be bothered to filter them all out and re-test the code. The current state is functional and they fit the overall aesthetic of the code well. Current implementation takes about 20x that of a pythonic 1-line sieve method (<2E6), and is very unlikely to support (very) large numbers regardless. In principle this should become relatively more efficient at higher numbers.

Optimization angles
Add variable and functionality to track and avoid re-generating preceding compounds, reduce amount of loops and if checks (specifically surrounding addprime function), generation of compounds might be reducable (first identify which combinations fill prime gaps efficiently), 