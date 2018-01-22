integers = [1,2,3,4,5,6,7,8,9]
def sum_to2(total, N, integer_list = integers):

	if N == 0:
		return used(integer_list) if total == 0 else False

	else:
		output = []
		for n in integer_list:
			copy = list(integer_list)
			del copy[copy.index(n)]
			answer = sum_to2(total - n, N - 1, copy)
			if answer:
				output+=answer
	output.sort()
	return list(set(output))

#return list of numbers that have been deleted given a list of numbers
def used(array):
	copy = list([2,3,4,5,6,7,8,9])
	for n in array:
		del copy[copy.index(n)]
	return copy


print sum_to2(18,3, [2,3,4,5,6,7,8,9])




v = [[1,2,3,5],[1,2,3,4]]
t = 6

1,1
1,2
1,3
1,4

2,1
2,2
2,3
2,4

3,1
3,2
3,3
3,4

5,1 5,2


[[1],[2],[3],[5]]

def sum_total_with_N(total, values):
	sums = []
	for v in values[0]:
		sums.append([v])
	for list in values[1:]:




sum_total_with_N(t,v)