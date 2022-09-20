def Transfer_numbers(number, base):
    s = ''
    while number > 0:
        s = str(number % base) + s
        number = number // base
    return s

c = []
f = open('input.txt')
for i in range(1, 143):
    c.append(int(f.readline()))

count = 0
max_elements = -400

for i in c:
  s = Transfer_numbers(i,8)
  t = len(s)
  if s[t-1] == '7' and s[t-2:] != '27':
      count +=1
      if i>max_elements:
          max_elements = i
print(count, max_elements)

