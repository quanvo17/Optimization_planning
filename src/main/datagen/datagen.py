import random as rd
import sys


def dataGen(name='test.txt', N=10, M=2, U=5, K=12, T=[2,4], G=10, S=[25,40], C=[30, 40]):

  # rd.seed(0)
  original_stdout = sys.stdout
  file_name = '../../../data/' + name
  with open(file_name, 'w') as f:
    sys.stdout = f

    t = []
    g = []
    s = []
    c = []
    print(N, M)
    print(U, K)
    for i in range(N):
      t.append(rd.randint(T[0], T[1]))
      g.append(rd.randint(1, G))
      s.append(rd.randint(S[0], S[1]))
      print(str(t[i]) + ' ' + str(g[i]) + ' ' + str(s[i]))
    for i in range(M):
      c.append(rd.choice([C[0], C[1]]))
      print(c[i], end=' ')

    sys.stdout = original_stdout


dataGen(name='data30.txt', N=30, M=5, G=5)
