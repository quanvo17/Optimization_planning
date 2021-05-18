import localsearch.constraints.basic.IsEqual;
import localsearch.constraints.basic.LessOrEqual;
import localsearch.functions.basic.FuncPlus;
import localsearch.functions.sum.Sum;
import localsearch.model.ConstraintSystem;
import localsearch.model.LocalSearchManager;
import localsearch.model.VarIntLS;
import localsearch.search.HillClimbing;

import java.io.File;
import java.util.Scanner;

public class ClassSchedule_HillClimbing {
    int U, K;
    int N; // Số lớp học
    int M; // Số phòng học
    int[] s; // sĩ số các lớp
    int[] g; // giáo viên
    int[] c; // số chỗ ngồi của các phòng
    int[] t; // tổng số tiết của các lớp trong tuần

    VarIntLS[][] val;
    int p = 0;

    LocalSearchManager mgr;
    VarIntLS[][][][] x;
    ConstraintSystem CS;

    private void stateModel() {
        input("data/.txt");
        mgr = new LocalSearchManager();
        x = new VarIntLS[N][U][K][M];
        val = new VarIntLS[N * U * K][M];

        for (int i = 0; i < N; i++) {
            for (int u = 0; u < U; u++) {
                for (int k = 0; k < K; k++) {
                    for (int j = 0; j < M; j++) {
                        // sức chứa : if s[i] >= c[j] thì x[i][u][k][j] = 0
                        if (s[i] > c[j])
                            x[i][u][k][j] = new VarIntLS(mgr, 0, 0);
                        else x[i][u][k][j] = new VarIntLS(mgr, 0, 1);
                    }
                }
            }
        }

        CS = new ConstraintSystem(mgr);

        //1.1 lop tai 1 tiet chi hoc o 0 hoac 1 phong: sum(x[i][u][k][0->M-1]) <= 1 voi moi i, u, k
        int[] oneM = new int[M];
        for (int j = 0; j < M; j++) oneM[j] = 1;

        for (int i = 0; i < N; i++) {
            for (int u = 0; u < U; u++) {
                for (int k = 0; k < K; k++) {
                    for (int j = 0; j < M; j++) {
                        val[p][j] = x[i][u][k][j];

                    }
                    CS.post(new LessOrEqual(new Sum(val[p]), 1));
                    p++;
                }
            }
        }

        //2. i1, i2 cung thu, tiet -> khac phong: x[i1][u][k][j] + x[i2][u][k][j] <= 1 voi moi i1, i2, u, k, j (i1 < i2)
        for (int i1 = 0; i1 < N - 1; i1++) {
            for (int i2 = i1 + 1; i2 < N; i2++) {
                for (int u = 0; u < U; u++) {
                    for (int k = 0; k < K; k++) {
                        for (int j = 0; j < M; j++) {
                            CS.post(new LessOrEqual(new FuncPlus(x[i1][u][k][j], x[i2][u][k][j]), 1));
                        }

                    }
                }
            }
        }

        //3. lop i1, i2 cung giao vien -> khac thu, khac tiet:
        //for(i1) for (i2 > i1) if g[i1] = g[i2] => x[i1][u][k][j1] + x[i2][u][k][j2] <= 1 voi moi u, k, j1 < j2
        for (int i1 = 0; i1 < N - 1; i1++) {
            for (int i2 = i1 + 1; i2 < N; i2++) {
                if (g[i1] == g[i2]) {
                    for (int u = 0; u < U; u++) {
                        for (int k = 0; k < K; k++) {
                            for (int j1 = 0; j1 < M; j1++) {
                                for (int j2 = j1 + 1; j2 < M; j2++) {
                                    CS.post(new LessOrEqual(new FuncPlus(x[i1][u][k][j1], x[i2][u][k][j2]), 1));
                                }
                            }
                        }
                    }
                }
            }
        }

        //5. tong cac tiet cua lop i trong tuan = t[i]----for i: sum(for u, k, j theo x) = t[i]

        for (int i = 0; i < N; i++) {
            VarIntLS[] tmp = new VarIntLS[U*K*M];
            int idx = 0;
            for (int u = 0; u < U; u++) {
                for (int k = 0; k < K; k++) {
                    for (int j = 0; j < M; j++) {
                        tmp[idx] = x[i][u][k][j];
                        idx++;
                    }
                }
            }
            CS.post(new IsEqual(new Sum(tmp),t[i]));
        }

        mgr.close();
    }

    private void search(){
        HillClimbingSearch searcher = new HillClimbingSearch(CS);
        searcher.search(10000,10000);

        System.out.println("lop: thu-tiet-phong");
        for (int i = 0; i < N; i++) {
            System.out.println();
            System.out.print("lop " + (i+1) + " : ");
            for (int u = 0; u < U; u++) {
                for (int k = 0; k < K; k++) {
                    for (int j = 0; j < M; j++) {
                        if (x[i][u][k][j].getValue() == 1) {
                            System.out.print((u+2) + "-" + (k+1) + "-" + (j+ 1)+ ", ");
                        }
                    }
                }
            }
        }
        System.out.println("\n");
    }

    public void solve(){
        stateModel();
        search();
    }
    private void input(String file_name) {
        try {
            File f = new File(file_name);
            Scanner scanner = new Scanner(f);

            N = scanner.nextInt();
            M = scanner.nextInt();
            U = scanner.nextInt();
            K = scanner.nextInt();

            s = new int[N];
            g = new int[N];
            c = new int[M];
            t = new int[N];
            for (int i = 0; i < N; i++) {
                t[i] = scanner.nextInt();
                g[i] = scanner.nextInt();
                s[i] = scanner.nextInt();
            }
            for (int i = 0; i < M; i++) {
                c[i] = scanner.nextInt();
            }

            /*b = new int[U*K];
            for (int i = 0; i < U*K; i++) {
                b[i] = 1;
            }*/

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        final long startTime = System.currentTimeMillis();
        ClassSchedule_HillClimbing app = new ClassSchedule_HillClimbing();
        app.solve();
        final long duration = System.currentTimeMillis() - startTime;
        long minutes = (duration / 1000) / 60;
        long seconds  = (duration / 1000) % 60;
        System.out.println(duration);
        System.out.println("\n" + minutes + "phút " + seconds + "s");
    }
}
