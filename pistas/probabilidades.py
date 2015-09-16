# coding=utf-8
__author__ = 'adrian'
from random import randint


dif_list = []


def probability(ans, coins, coins_paid, trust):
    pos_ans = 0
    for i in range(len(ans) - 1):
        if ans[i] == ans[-1]:
            pos_ans = i
            break
    P = [0, 0, 0, 0]
    for i in range(100):
        random_pos = randint(0, 3)
        if random_pos == 0:
            P[0] += 1
        elif random_pos == 1:
            P[1] += 1
        elif random_pos == 2:
            P[2] += 1
        elif random_pos == 3:
            P[3] += 1

    def random_not_pos_ans():
        while True:
            r = randint(0, 3)
            if r != pos_ans:
                break
        return r

    def dism():
        dism_ = (sum(P) - 100) / 2
        for i in range(4):
            if i == pos_ans: continue
            if i == r: continue
            P[i] -= dism_
            if P[i] < 0: P[i] = 0

    if trust == "ALTA":  # P ALTA
        P[pos_ans] += 21
        for i in range(4):
            if i == pos_ans: continue
            P[i] -= 7
    elif trust == "BUENA":  # P BUENA
        P[pos_ans] += 21
        r = random_not_pos_ans()
        P[r] += 10
        # TEST
        # dif = P[pos_ans] - P[r]
        # dif_list.append(dif)
        dism()
    elif trust == "MEDIA":  # P MEDIA
        P[pos_ans] += 21
        r = random_not_pos_ans()
        P[r] += 15
        # TEST
        # dif = P[pos_ans] - P[r]
        # dif_list.append(dif)
        dism()
    elif trust == "BAJA":  # P BAJA
        P[pos_ans] += 5
        r = random_not_pos_ans()
        P[r] -= 5
        # TEST
        # max_ = max(P)
        # for i in range(len(P)):
        # if P[i] == max_ and i == pos_ans:
        #         dif_list.append(1)
    elif trust == "MALA":  # P MALA
        pass
        # TEST
        # max_ = max(P)
        # for i in range(len(P)):
        # if P[i] == max_ and i == pos_ans:
        #         dif_list.append(1)
    return P


def test_B_C():
    for i in range(500):
        probability(coins_paid=150)
    print("elems", len(dif_list))
    print("dif ave", sum(dif_list) / len(dif_list))
    print("%neg", len([neg for neg in dif_list if neg < 0]) * 100 / len(dif_list))


def test_D_E():
    for i in range(500):
        probability(coins_paid=50)
    print("%neg", len(dif_list) * 100 / 500)