import re

from academy import Academy


print("Prepare Academy...")
ac = Academy()
print("Academy is ready!")

count = 0
count_err = 0
with open('lemonde.dump', 'r') as text:
	for line in text:
		for word in re.split('\\W+', line):
			count += 1
			if not ac.check(word):
				count_err += 1
				print('[%d/%d] Invalid word: %s' % (count_err, count, word))


