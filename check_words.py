import re
import sys

from academy import Academy

filename = '/home/elie/irclogs/ens/#courssysteme.log'

print("Prepare Academy...")
ac = Academy()
print("Academy is ready!")

ac.white_list('whitelist.txt')


def ignore(word):
	"""ignore(word)
	Filter words, especially numbers"""
	return re.match('^\d+$', word)!= None

count = 0
count_err = 0
with open(filename, 'r') as text:
	for line in text:
		for word in re.split('\\W+', line):
			if ignore(word):
				continue
			count += 1
			sys.stderr.write('[%d/%d] %s                   \r' % (count_err, count, word))
			sys.stderr.flush()
			if not ac.check(word):
				count_err += 1
				print('[%d/%d] Invalid word: %s' % (count_err, count, word))


