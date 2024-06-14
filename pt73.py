from itertools import chain, combinations, combinations_with_replacement
from functools import reduce
from math import prod
import numpy
import copy
import time

# only here as reference / benchmark
def primesieve(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

# used to generate compounds from primes and the exceptions to the prime candidates generated from it (takes some experimental parameters)
def ccccombomaker(components, maxcount, maxprod, mincount = 0, sequential = False, startzero = 0, maxrepeats = -1, maxgap = 0):
	comps = {}
	current = [0, 0]											# TRACKS COMPOUND FACTORS FROM PRIME LIST
	adder = 1
	breakloop = 0
	while current[0] < len(components):
		prev = -1
		repeats = 0
		allrepeats = 0
		for w, x in enumerate(current):
			if x >= len(components):							# COUNTS NUMBERS
				for y, z in enumerate(current):
					if z >= len(components):
						current[y - 1] += 1
						# THE EXTRA -1 IS TO COMPENSATE FOR CURRENT[-1] + 1 after main for loop
						current[y] = current[y - 1] - 1
						adder = 1
						breakloop = 1
						break

			if current[-1] < len(components) and sequential == True and breakloop == 0:			# MOVES ON TO THE NEXT LOOP IF COMPONENTS ARENT SEQUENTIAL
				if  w > 0 and x != current[w - 1] + 1 and x != current[w - 1]:
					breakloop = 1
					adder = 1
					current[-1] += 1

			if prev == x and maxrepeats > -1:					# ENFORCE MAXIMUM REPEATS
				repeats += 1
				if repeats > maxrepeats:
					adder = 1
					current[w] += 1
					breakloop = 1
			else: 
				repeats = 0
			prev = x

			if prev + maxgap < x:								# ENFORCE MAXIMUM GAP DISTANCE
				adder = 1 
				current[w] += 1
				breakloop = 1

			if breakloop != 0:									# PREVENT WEIRD MULTIPLICATIONS AND UNWANTED COMPOUND GENERATION
				breakloop = 0
				break

			adder = adder * components[x]
			if adder > maxcount or (adder < mincount and w == len(current)):	# ENFORCE COMPOUND MAXIMUM AND MINIMUM
				adder = 1
				current[w - 1] += 1
				current[w] = current[w - 1] - 1
				break

		if (sequential == True or startzero == 1) and current[0] != 0:			# ENFORCE FACTOR SEQUENCE START WITH ZERO
			current[0] = len(components) + 1

		if adder != 1: 											# CONVERT CURRENT INDEX TO ACTUAL NUMBER FOR TRACKING OF FACTORS
			if adder > maxcount:
				print('WTF', adder, maxcount)
			z = []
			for y in current:
				z.append(components[y])
			comps[adder] = z
			adder = 1

		if breakloop == 0:										# PROGRESS COUNTER
			current[-1] += 1	

		if current[0] >= len(components) - 1:					# ADD A FACTOR IF BELOW MAXIMUM, should be at end because overflow counting requires multiple loops
			if maxprod > len(current):
				current.append(0)
				for x, y in enumerate(current):
					current[x] = 0
	return comps

def addprime(candidate, checklist, largercomposites, base = 0, operator = 0, diff = 0):
	if candidate > 1 and candidate not in checklist and candidate not in largercomposites:
		checklist.append(candidate)
	return

# set of primes to start calculations with
primes = [2, 3, 5]
# highest compound number to calculate primes from
maxcomposite = int(150000)
# all previous compound numbers tested, quite possibly redundant
testedcomposites = []
compositecollection = {}
# tracking highest tested number, poorly implemented
runningnumber = 3
# maximum factors in compound number
maxcomponents = 2
# for timing purposes
interval = maxcomposite / 20
times = {'base': {}, 'larger': {}, 'inbetween': {}}
times[0] = time.time()
# this is a file containing the first 1E6 primes, up to 15485863
f = open("ls3.txt", "r")
file = f.readlines()

while int(runningnumber) < maxcomposite:
	print("new round", runningnumber)
# generate compounds from primes (using sequential primes, with option to use multiples, reduces redundancy and leaves few gaps in each round of generation)
	composites = {}
	composites.update(ccccombomaker(primes[0:maxcomponents], (runningnumber * 2), len(str(runningnumber)) + 2, sequential = True, startzero = 0))
	maxcomponents += 1
	
# start evaluating known compound distances
	sortcomposites = sorted(composites.items())
	limit = int(sortcomposites[-1][0])
	sortcomposites = dict(sortcomposites)
	compcount = 0
	for i, c in sortcomposites.items():
		if i not in compositecollection:
			compositecollection[i] = c
		if i in testedcomposites or i < (runningnumber * 1):
			continue
		if i > runningnumber * 2 and maxcomponents > 2:
			break
		if i > limit or (i > maxcomposite and maxcomponents > 2):
			runningnumber = i
			break
		compcount += 1
		runningnumber = i
		print("testing for composite: ", i, c, compcount, '/', len(composites))
		
# filter prime composites for symmetry radiating from compound
		largercomposites = []
		primes.sort()
		j = int(i)
		minprime = 0
		maxprime = 0
		pwr = 2
		for x in primes:
			if x not in c:
				if minprime == 0:
					minprime = primes.index(x)
				if maxprime == 0 and x * primes[minprime] > j * 2:
					maxprime = primes.index(x)
					break					
				while pow(x, pwr) < j * 2:
					if pow(x, (pwr + 1)) > j * 2:
						break
					pwr += 1
		if maxprime == 0:
			maxprime = primes.index(primes[-1])

# generate list of exceptions to the found prime potentials
		largercomposites = ccccombomaker(primes, (i * 2), pwr)
		addprime((i - 1), primes, largercomposites)
		addprime((i + 1), primes, largercomposites)
		addprime(((i * 2) - 1), primes, largercomposites)
		for p in primes:
			if p > i:
				break
			if p not in c:
				addprime(i + p, primes, largercomposites, i, "pos", p)
				addprime(i - p, primes, largercomposites, i, "neg", p)
		testedcomposites.append(i)

# checks and stats		
primes.sort()
times[1] = time.time()
print(len(primes), 'primes found')
testedcomposites.sort()
print('tested composites:', len(testedcomposites))
print('total time', times[1] - times[0])
under = 0
over = 1
checked = 0
missingunder = []
missingover = []
falseposcheck = []

for i, x in enumerate(file):
	if int(x) > primes[-1]:
		print('breaking', i, x)
		break
	prime = int(x.rstrip('\n'))
	if prime < maxcomposite:
		checked += 1
		if prime in primes:
			under += 1
		else:
			missingunder.append(prime)
	if prime > maxcomposite:
		if prime in primes:
			over += 1
		else:
			missingover.append(prime)
	falseposcheck.append(prime)

print('checking false positives for target', maxcomposite)
for x in primes:
	if x not in falseposcheck:
		print('FALSE POSITIVE FOUND:', x)

print('found under target:', checked, '/', under, (under / checked) * 100, "%")
print('missers under target:', len(missingunder), (len(missingunder) / (len(missingunder) + under)) * 100, '%')
print('primes missing under target:', missingunder)
print('missers between target and (2 * target):', len(missingover), (len(missingover) / (len(missingover) + over)) * 100, '%')

#print('primes;', primes)
