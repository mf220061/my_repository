import itertools

# DB に対する操作のこと、 Rt(x) だと
# R: 操作の内容（ R/W のいずれか）
# t: どのトランザクションに属する操作か
# x: 操作の対象となるデータ
# position は元の課題に記載されているスケジュールでの位置
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

# 競合しない操作のペアのリストを作成
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
# #04.pdf の 28, 29 ページを元にして競合の確認を行う。
def check(a, b):
    if a.sousa == 'r' and b.sousa == 'r':
        return False
    if a.data != b.data:
        if a.sousa != b.sousa and a.transaction == b.transaction:
            return True
        return False
    return True

# 目的となる直列スケジュールの作成
# ここで直列スケジュールはトランザクションごとに操作をまとめたものをつなげたものとする。
# そのため、今回のようにトランザクションが
# ３つある場合、直列化可能スケジュールは 3! 個つまり６個考えられる。
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
    transactions = [transaction_S, transaction_T, transaction_U]
    goals = []
    for i in list(itertools.permutations(transactions)):
        serial_schedule = []
        for j in i:
            serial_schedule += j
        goals.append(serial_schedule)
    return goals

# スケジュールを構成するデータベースに対する操作を並べ替えて、
# 新たなスケジュールを構築する。
# 並べ替えには、リストの全ての並びを生成する itertools.permutations を使用する。
# そのとき、操作の順番が入れ替わっているものについては、競合を確認する。
# 全ての操作について競合しないスケジュールを返す。
def search_schedule(schedule, nconflicts):
    schedules = list(itertools.permutations(schedule))
    enable_schedules = []
    for s in schedules:
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
    return enable_schedules

# 競合直列化可能であるかを確認する。
# まず、競合の起きない操作のペアのリストを check_conflict を用いて作成する。
# 次に、 search_schedule を用いて、元のスケジュールと競合の起きないスケジュールのリストを作成する。
# その後、 make_goal で元のスケジュールから直列スケジュールを作成する。
# 最後に、直列スケジュールのいずれかが元のスケジュールと競合の起きないスケジュールのリストに
# 含まれるかを確認して、含まれる場合、「競合直列化可能」と表示する。
# また。含まれない場合、「競合直列化不可能」と表示する。
def solve(schedule):
    print(' 元のスケジュール：', end='')
    print_schedule(schedule)
    nconflicts = check_conflict(schedule)
    es = search_schedule(schedule, nconflicts)
    gs = make_goal(schedule)
    hantei = False
    for g in gs:
        print(' goal: ', end='')
        print_schedule(g)
        if tuple(g) in es:
            print(' 可能')
            hantei = True
        else:
            print(' 不可能')

    print(' 結果：', end='')
    if hantei:
        print(' 競合直列化可能')
    else:
        print(' 競合直列化不可能')
    print()


S1 = [ # (1) のスケジュール
        Sousa("r", "t", "x"),
        Sousa("r", "s", "x"),
        Sousa("r", "u", "x"),
        Sousa("r", "t", "y"),
        Sousa("r", "s", "y"),
        Sousa("w", "u", "x"),
        Sousa("w", "t", "x"),
        Sousa("w", "s", "z")
    ]

S2 = [ # (2) のスケジュール
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

S3 = [ # (3) のスケジュール
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

S4 = [ # オリジナルのスケジュール
        Sousa('r', 's', 'x'),
        Sousa('r', 's', 'y'),
        Sousa('r', 't', 'x'),
        Sousa('r', 't', 'z'),
        Sousa('w', 's', 'y'),
        Sousa('r', 'u', 'y'),
        Sousa('r', 'u', 'z'),
        Sousa('w', 'u', 'y'),
        Sousa('w', 't', 'x'),
        Sousa('w', 't', 'z')
    ]

print(' (1) のスケジュール')
solve(S1)

print(' (2) のスケジュール')
solve(S2)

print(' (3) のスケジュール')
solve(S3)

print(' オリジナルのスケジュール')
solve(S4)
