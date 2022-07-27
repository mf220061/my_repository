import itertools

# DBに対する操作のこと、Rt(x)だと
# R: 操作の内容（R/Wのいずれか）
# t: どのトランザクションに属する操作か
# x: 操作の対象となるデータ
# positionは元の課題に記載されているスケジュールでの位置
class Sousa:
    position = 0

    def __init__(self, sousa, transaction, data):
        self.sousa = sousa
        self.transaction = transaction
        self.data = data
        self.position = Sousa.position
        Sousa.position += 1

# 描画準備
def print_sousa(sousa):
    return sousa.sousa.upper() + sousa.transaction + '(' + sousa.data + ')'

# 描画
def print_schedule(schedule):
    N = len(schedule)
    for i in range(N):
        print(print_sousa(schedule[i]), end=' ')
    print()

# スケジュール全体の競合しない操作のリストを作成
def check_conflict(schedule):
    N = len(schedule)
    a, b = 0, 1
    ans = []
    for i in range(N*(N-1)//2):
        if not check(schedule[a], schedule[b]):
            ans.append([schedule[a], schedule[b]])
        b += 1
        if b == N:
            a += 1
            b = a + 1
    return ans

# 競合の確認
# ここを修正するべきかも
def check(a, b):
    if a.sousa == 'r' and b.sousa == 'r':
        return False
    if a.data != b.data:
        if a.sousa != b.sousa and a.transaction == b.transaction:
            return True
        return False
    return True

# 目的となる直列スケジュールの作成
# プログラムの流れとしては、元のスケジュールを競合の無いように
# 並べ替え、ここで作成するスケジュールと同じになるかを確認する。
# なる場合は、競合直列化可能であると考えられる。
def make_goal(schedule):
    transaction_T = []
    transaction_S = []
    transaction_U = []
    for i in schedule:
        if i.transaction == 't':
            transaction_T.append(i)
        elif i.transaction == 's':
            transaction_S.append(i)
        else:
            transaction_U.append(i)
    #return transaction_U + transaction_S + transaction_T
    transactions = [transaction_S, transaction_T, transaction_U]
    goals = []
    for i in list(itertools.permutations(transactions)):
        serial_schedule = []
        for j in i:
            serial_schedule += j
        goals.append(serial_schedule)
    return goals

def search_schedule(schedule, nconflicts):
    #print(nconflicts)
    schedules = list(itertools.permutations(schedule))
    enable_schedules = []
    for s in schedules:
        #print_schedule(s)
        for i in range(1, len(s)):
            for j in range(i):
                if s[j].position > s[i].position:
                    if [s[i], s[j]] not in nconflicts:
                        break
            else:
                continue
            break
        else:
            enable_schedules.append(s)
    print()
    for i, e in enumerate(enable_schedules):
        print(i, end=' ')
        print_schedule(e)
    print()
    return enable_schedules

def solve(schedule):
    nconflicts = check_conflict(schedule)
    es = search_schedule(schedule, nconflicts)
    gs = make_goal(schedule)
    for g in gs:
        print('goal: ', end='')
        print_schedule(g)
        if tuple(g) in es:
            print('可能')
        else:
            print('不可能')
S1 = [
        Sousa("r", "t", "x"),
        Sousa("r", "s", "x"),
        Sousa("r", "u", "x"),
        Sousa("r", "t", "y"),
        Sousa("r", "s", "y"),
        Sousa("w", "u", "x"),
        Sousa("w", "t", "x"),
        Sousa("w", "s", "z")
    ]

S2 = [
        Sousa("r", "t", "x"),
        Sousa("r", "s", "y"),
        Sousa("r", "u", "z"),
        Sousa("r", "t", "y"),
        Sousa("r", "s", "x"),
        Sousa("r", "u", "y"),
        Sousa("w", "t", "z"),
        Sousa("w", "s", "z"),
        Sousa("w", "u", "z")
    ]

S3 = [
        Sousa("r", "t", "x"),
        Sousa("r", "s", "x"),
        Sousa("r", "u", "x"),
        Sousa("r", "t", "y"),
        Sousa("r", "s", "z"),
        Sousa("w", "t", "y"),
        Sousa("r", "u", "z"),
        Sousa("w", "s", "z"),
        Sousa("w", "t", "z"),
        Sousa("w", "u", "x")
    ]

S4 = [
        Sousa('r', 's', 'a'),
        Sousa('r', 's', 'b'),
        Sousa('r', 't', 'a'),
        Sousa('r', 't', 'c'),
        Sousa('w', 's', 'b'),
        Sousa('r', 'u', 'b'),
        Sousa('r', 'u', 'c'),
        Sousa('w', 'u', 'b'),
        Sousa('w', 't', 'a'),
        Sousa('w', 't', 'c')
    ]

solve(S1)
solve(S2)
solve(S3)
solve(S4)
