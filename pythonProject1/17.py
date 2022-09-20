def F(n, m):
    if n < m:
        n, m = m, n
    if n != m:
        return F(n - m, m)
    else:
        return n


c = []
d = []

for i in range(1, 100):
    for j in range(1, 100):
        if F(i, j) > 15 and i != j:
            c.append([i, j])
        if F(j, i) > 15 and i != j:
            c.append([i, j])

for i in c:
    d.append(i[0] + i[1])

print(c[d.index(min(d))])
