c = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
n = input()
n1 = []
f = False
f2 = False
s = '+7'
for i in n:
    if i != ' ' and i != '\t' and i != '\n':
        n1.append(i)
try:
    for i in n1:
        assert not(i in c or i == '-' or i == '+' or i == '(' or i == ')')

    for i in n1:
        if i == '(' and not f2:
            f2 = True
        if i == ')' and f2:
            f2 = False
        elif i == ')':
            f2 = True

    assert n1[0] == '8':
    n1 = ['+', '7'] + n1[1:]


if n1.count('(') == n1.count(')') and (n1[0] == '+' and n1[1] == '7' or n1[0] == '8') and '--' \
        not in ''.join(n1) and n1[0] != '-' and n1[-1] != '-' and not f and not f2:
    for i in n1[2:]:
        if i in c:
            s += i
    if len(s) == 12:
        print(s)
    else:
        print('error')
else:
    print('error')