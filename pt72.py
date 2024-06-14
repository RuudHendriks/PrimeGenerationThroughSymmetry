from itertools import chain, combinations, combinations_with_replacement
from functools import reduce
from math import prod
import numpy
import copy
import time

# incorporate a function/variable that tracks past combo's made for each exponent

def ccccombomaker(components, maxcount, maxprod, prevtested, mincount = 0, sequential = False, startzero = 0, maxrepeats = -1, maxgap = 0):

	comps = {}
	current = [0, 0]
	adder = 1
	breakloop = 0
	tested = {}
	print('making combos', len(components), maxcount, maxprod, components, prevtested)

	combo = len(current)
	if combo in prevtested:
		for w, x in enumerate(current):
			current[w] = prevtested[combo]
		tested[len(current)] = prevtested[len(current)]

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
			if adder > maxcount or (adder < mincount and w == len(current)):					# ENFORCE COMPOUND MAXIMUM AND MINIMUM
				adder = 1
				current[w - 1] += 1
				current[w] = current[w - 1] - 1
				break

		if (sequential == True or startzero == 1) and current[0] != 0:	# ENFORCE FACTOR SEQUENCE START WITH ZERO
			current[0] = len(components) + 1
			adder = 1

		if adder != 1: 											# CONVERT CURRENT INDEX TO ACTUAL NUMBER FOR TRACKING OF FACTORS
			if adder > maxcount:
				print('WTF', adder, maxcount)
			z = []
			for y in current:
				z.append(components[y])
			comps[adder] = z
			# TURN INTO COPY OF 'CURRENT' AFTER COMBONR
			tested[len(current)] = current[0]
			adder = 1

		if breakloop == 0:										# PROGRESS COUNTER
			current[-1] += 1	

		if current[0] >= len(components) - 1:					# ADD A FACTOR IF BELOW MAXIMUM, should be at end because overflow counting requires multiple loops
			if maxprod > len(current):
				current.append(0)
				for x, y in enumerate(current):
					current[x] = 0
	print("tested", tested)
	return comps, tested

def addprime(candidate, checklist, exceptions, base = 0, operator = 0, diff = 0):
	if candidate > 1 and candidate not in checklist and candidate not in exceptions:
		checklist.append(candidate)
#		if operator == 'neg' and candidate not in primes:
#			print('NEG prime added:', candidate, '=', base, operator, diff)
		if candidate > 5 and candidate % 5 == 0:
			print('CANDIDATE ERRROR', candidate, checklist, exceptions)
			quit()
			exit()
	return

prevtested = {'base': {}, 'larger': {}}
primes = [2, 3, 5]
maxcomposite = int(50000)
testedcomposites = []
runningnumber = 3
maxcomponents = 2
composites = {}
compositecollection = {}
largercomposites = {}
interval = maxcomposite / 20
times = {}
times[0] = time.time()
f = open("ls3.txt", "r")
file = f.readlines()

# FIND A WAY TO SKIP CYCLING THROUGH THE LAST 20% OF GENERATED COMPOSITES

while int(runningnumber) < maxcomposite:
	# MAKING ALL THESE COMBOS IS THE MAIN BOTTLENECK!!
#	composites = ccccombomaker(primes[0:maxcomponents], (runningnumber * 2), len(str(runningnumber)), False, 1)
	print("new round", runningnumber)
	newcomposites, newtested = ccccombomaker(primes[0:maxcomponents], (runningnumber * 2), len(str(runningnumber)) + 2, prevtested['base'], sequential = True, startzero = 0)
	prevtested['base'] = newtested
	composites.update(newcomposites)
	print(composites)

	maxcomponents += 1

#start evaluating known compound distances
	sortcomposites = sorted(composites.items())
#	print(sortcomposites)
	limit = int(sortcomposites[-1][0])
	sortcomposites = dict(sortcomposites)
#	print(len(sortcomposites), sortcomposites)
#	print(primes)
	compcount = 0

	for i, c in sortcomposites.items():
		if i not in compositecollection:
			compositecollection[i] = c
		if i in testedcomposites or i < (runningnumber * 1):
			continue
		if i > runningnumber * 2 and maxcomponents > 2:
			print('something shit')
			break
		if i > limit or (i > maxcomposite and maxcomponents > 2):
			print('maxxing', i, ">", maxcomposite, 'or', limit)
			runningnumber = i
			break
		compcount += 1
		runningnumber = i

# filter prime composites from positive symmetry base for potential primes
		primes.sort()
#		print('searching', i, c)
		j = int(i)
		minprime = 0
		maxprime = 0
		pwr = 2

		for x in primes:
#			print(x, i, c[-1], (i * 2) / c[-1])
			if x not in c:
#				print('checking ', x, maxprime)
				if minprime == 0:
					minprime = primes.index(x)
#					print('firstprime found', x)
				if maxprime == 0 and x * primes[minprime] > j * 2:
					maxprime = primes.index(x)
#					print('maxbase found', x, 'x', primes[minprime], '>', j, 'x 2')
					break					
				while pow(x, pwr) < j * 2:
					if pow(x, (pwr)) > j * 2:
						print('PWR', x, (pwr), j)
						break
#					print(pow(x, pwr), x, "^", pwr, "<", j)
					pwr += 1
		if maxprime == 0:
			maxprime = primes.index(primes[-1])
#			print('manually adding maxprime', primes[-1])

		print("testing for composite: ", i, compcount, '/', len(composites) + 1, c, pwr, minprime, maxprime)

		newlargercomposites, prevtested['larger'] = ccccombomaker(primes[0:maxprime], (i * 2), pwr, prevtested['larger'])
		print('newlargercomposites', newlargercomposites)
		print('oldlargercomposites', largercomposites)
		largercomposites.update(newlargercomposites)
		print('largercomposites', largercomposites)

		addprime((i - 1), primes, largercomposites)
		addprime((i + 1), primes, largercomposites)
		addprime(((i * 2) - 1), primes, largercomposites)
		
		for p in primes:
			newposp = i + p 
			newnegp = i - p
			if p > i:
				break

			if p not in c:
#			print("potential + found: ", i, p, newposp, c)
				addprime(newposp, primes, largercomposites, i, "pos", p)
#			print("potential - found: ", i, p, newnegp, c)
				addprime(newnegp, primes, largercomposites, i, "neg", p)
			if len(primes) % interval == 0:
				times[len(primes)] = time.time()

		testedcomposites.append(i)

primes.sort()

times[len(primes)] = time.time()
testedcomposites.sort()
print('tested composites:', len(testedcomposites), testedcomposites)

print(len(primes), 'primes found')

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


print('found under target:', checked, under, (under / checked) * 100, "%")
print('missers under target:', len(missingunder), (len(missingunder) / (len(missingunder) + under)) * 100, '%')
print('missing under', missingunder)
print('missers over target:', len(missingover), (len(missingover) / (len(missingover) + over)) * 100, '%')

#print('primes;', primes)
