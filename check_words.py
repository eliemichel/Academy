import re

from academy import Academy


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
with open('lemonde.dump', 'r') as text:
	for line in text:
		for word in re.split('\\W+', line):
			if ignore(word):
				continue
			count += 1
			print('[%d/%d] %s' % (count_err, count, word), end='')
			if not ac.check(word):
				count_err += 1
				print('[%d/%d] Invalid word: %s' % (count_err, count, word))


