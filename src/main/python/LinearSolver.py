from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
import time
from time import strftime
from time import gmtime

def main():
    # Create the linear solver with the SCIP backend.
    # infinity = solver.infinity()
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Create the variables.
    x = {}
    for i in range(N):
        for u in range(U):
            for k in range(K):
                for j in range(M):
                    x[i*U*K*M+u*K*M+k*M+j] = solver.IntVar(0, 1, 'x[{0},{1},{2},{3}]'.format(i,u,k,j))
    
    # print('Number of variables =', solver.NumVariables())

    # Create a linear constraint.
    # 1. Lớp học không thể xếp vào phòng có sức chứa nhỏ hơn số lượng sinh viên
    for i in range(N):
        for u in range(U):
            for k in range(K):
                for j in range(M):
                    ct = solver.Constraint(0, 0)
                    if s[i] > c[j]:
                        ct.SetCoefficient(x[i*U*K*M+u*K*M+k*M+j],1)

    # 2. Trong một thời điểm, một lớp chỉ có thể học tại 1 phòng
    for i in range(N):
        for u in range(U):
            for k in range(K):
                ct = solver.Constraint(0, 1)
                for j in range(M):
                    ct.SetCoefficient(x[i*U*K*M+u*K*M+k*M+j], 1)

    # 3. Trong cùng thời điểm, không thể có 2 lớp học cùng 1 phòng
    for i1 in range(N-1):
        for i2 in range(i1+1, N):
            for u in range(U):
                for k in range(K):
                    ct = solver.Constraint(0, 1)
                    for j in range(M):
                        ct.SetCoefficient(x[i1*U*K*M+u*K*M+k*M+j], 1)
                        ct.SetCoefficient(x[i2*U*K*M+u*K*M+k*M+j], 1)
                        
    # 4. Trong cùng thời điểm, không thể có 2 lớp cùng giáo viên
    for i1 in range(N-1):
        for i2 in range(i1+1, N):
            if g[i1] == g[i2]:
                for u in range(U):
                    for k in range(K):
                        ct = solver.Constraint(0, 1, 'ct4')
                        for j in range(M):
                            ct.SetCoefficient(x[i1*U*K*M+u*K*M+k*M+j], 1)
                            ct.SetCoefficient(x[i2*U*K*M+u*K*M+k*M+j], 1)

    # 5. Tổng tất cả các tiết học phải được bảo toàn
    for i in range(N):
        SumT = 0
        SumT += int(t[i])
        T = solver.IntVar(SumT, SumT, 't')
        ct = solver.Constraint(0, 0)
        for u in range(U):
            for k in range(K):
                for j in range(M):
                    ct.SetCoefficient(x[i*U*K*M+u*K*M+k*M+j], 1)
        ct.SetCoefficient(T, -1)

    # print('Number of constraints =', solver.NumConstraints())

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print('\nSolution:')
        # for i in range(N):
        #     print('lop', i+1, ': ', end='')
        #     for u in range(U):
        #         for k in range(K):
        #             for j in range(M):
        #                 if(x[i*U*K*M+u*K*M+k*M+j].solution_value() == 1):
        #                     print(u+2,k+1,j+1,end=' | ')
        #     print()

        # Timetable
        # print('\n--TIMETABLE--')
        arr = np.empty((K,U), dtype=object)
        for u in range(U):
            # print('Day', u+2, ':')
            for k in range(K):
                for j in range(M):
                    day = ''
                    for i in range(N):
                        if(x[i*U*K*M+u*K*M+k*M+j].solution_value() == 1):
                            # print('Time {0} - Room {1} - Class {2}'.format(k+1,j+1,i+1))
                            day += '[{0}, {1}]'.format(j+1,i+1)
                    arr[k][u] = day
            # print()
        timetable = pd.DataFrame(arr)
        # print(timetable)
        # timetable.to_csv('timetable.csv', index=False)

def read_data(name='data.txt'):

    data = open(name, 'r')

    global N, M, U, K, t, g, s, c
    line_raw = data.readline().split('\n')
    line = line_raw[0].split(' ')
    N = int(line[0])
    M = int(line[1])
    line_raw = data.readline().split('\n')
    line = line_raw[0].split(' ')
    U = int(line[0])
    K = int(line[1])
    t, g, s, c = [], [], [], []

    for i in range(N):
        line_raw = data.readline().split('\n')
        line = line_raw[0].split(' ')
        t.append(line[0])
        g.append(line[1])
        s.append(line[2])

    line_raw = data.readline().split('\n')
    line = line_raw[0].split(' ')
    for j in range(M):
        c.append(line[j])
    
    print(N, M)
    # [print(t[i], g[i], s[i]) for i in range(N)]
    # [print(c[j], end=' ') for j in range(M)]
    # print()
    data.close()



if __name__ == '__main__':
    start = time.time()
    data_dir = '/home/luong/Documents/hust/toi-uu-lap-ke-hoach/project/Optimization_planning/data/'
    
    read_data(data_dir + 'data40-9-10.txt')
    
    main()
    end = time.time()
    run_time = end - start
    if run_time < 5:
        print(round(run_time * 1000), 'ms')
    elif run_time < 60:
        print(round(run_time), 's')
    else:
        print(strftime("%H:%M:%S", gmtime(run_time)))
