from functools import cmp_to_key


class Node:
    def __init__(self, elem_="", parent_=None):
        self.parent = parent_
        self.elem = elem_
        self.childs = []
        self.count = 0
        self.pre_order = 0
        self.post_order = 0

    def insert(self, t):

        if len(t) == 0:
            return

        for child in self.childs:
            if t[0] == child.elem:
                t = t[1:]
                child.count += 1
                child.insert(t)
                return
        self.childs.append(Node(t[0], self))
        t = t[1:]
        self.childs[-1].count += 1
        self.childs[-1].insert(t)
        return


class PPcode:
    def __init__(self, pre_order_, post_order_, count_):
        self.pre_order = pre_order_
        self.post_order = post_order_
        self.count = count_

    def __str__(self):
        return '<' + str(self.pre_order) + ', ' + str(
            self.post_order) + '> : ' + str(self.count) + ';'


def cmp_frequency(elem1, elem2, frequency):
    if frequency[elem1] == frequency[elem2]:
        if elem1 < elem2:
            return -1
        else:
            return 1
    return frequency[elem2] - frequency[elem1]


def transactions_convert(transactions, eps):
    frequency = {}
    for t in transactions:
        elems = set()
        for elem in t:
            if elem not in elems:
                if elem in frequency:
                    frequency[elem] += 1
                else:
                    frequency[elem] = 1

    for j in range(len(transactions)):
        t = transactions[j]
        elems = set()
        converted = []
        for elem in t:
            if elem not in elems and \
                    frequency[elem] >= eps * len(transactions):
                converted.append(elem)
        converted.sort(key=cmp_to_key(
            lambda elem1, elem2: cmp_frequency(elem1, elem2, frequency)))
        transactions[j] = converted


def fp_tree(transactions):
    root = Node()
    for t in transactions:
        root.insert(t)
    return root


def ppc_tree(node, pre_cnt, post_cnt):
    node.pre_order = pre_cnt
    pre_cnt += 1
    for child in node.childs:
        pre_cnt, post_cnt = ppc_tree(child, pre_cnt, post_cnt)
    node.post_order = post_cnt
    post_cnt += 1
    return pre_cnt, post_cnt


def nl1_construction(root, node, nlist):
    if node != root:
        if node.elem in nlist:
            nlist[node.elem].append(
                PPcode(node.pre_order, node.post_order, node.count))
        else:
            nlist[node.elem] = [
                PPcode(node.pre_order, node.post_order, node.count)]
    for child in node.childs:
        nl1_construction(root, child, nlist)
    return


def nl_intersection(nl1, nl2):
    i = 0
    j = 0
    initial_nl3 = []
    while i < len(nl1) and j < len(nl2):
        if nl1[i].pre_order < nl2[j].pre_order:
            if nl1[i].post_order > nl2[j].post_order:
                initial_nl3.append(PPcode(nl1[i].pre_order, nl1[i].post_order,
                                          nl2[j].count))
                j += 1
            else:
                i += 1
        else:
            j += 1
    if len(initial_nl3) == 0:
        return []
    nl3 = [initial_nl3[0]]
    for i in range(1, len(initial_nl3)):
        if nl3[-1].pre_order == initial_nl3[i].pre_order and \
                nl3[-1].post_order == initial_nl3[i].post_order:
            nl3[-1].count += initial_nl3[i].count
        else:
            nl3.append(initial_nl3[i])
    return nl3


def temp2_concstruction(node, temp2, l1_dict):
    ancestor = node.parent
    while ancestor is not None and ancestor.elem != "":
        temp2[l1_dict[ancestor.elem]][l1_dict[node.elem]] += node.count
        ancestor = ancestor.parent
    for child in node.childs:
        temp2_concstruction(child, temp2, l1_dict)
    return


def nl2_construction(root, l1_dict, l1, nl1, min_supp):
    temp2 = [[0 for i in range(len(l1_dict))] for j in range(len(l1_dict))]
    temp2_concstruction(root, temp2, l1_dict)
    nl2 = {}
    for i in range(len(l1_dict)):
        for j in range(len(l1_dict)):
            if temp2[i][j] >= min_supp:
                tmp = nl_intersection(nl1[l1[i][1]], nl1[l1[j][1]])
                if len(tmp) != 0:
                    nl2[(i, j)] = tmp
    return nl2


def nlk_mining(nl_cur, min_supp):
    F = []
    for key in nl_cur:
        F.append(key)
    if len(nl_cur) < 2:
        return F
    nl_next = {}
    for key1 in nl_cur:
        for key2 in nl_cur:
            elem1 = nl_cur[key1]
            elem2 = nl_cur[key2]
            if key1[0] < key2[0] and key1[1:] == key2[1:]:
                key_next = (key1[0], key2[0]) + key1[1:]
                tmp = nl_intersection(elem1, elem2)
                sum = 0
                for elem3 in tmp:
                    sum += elem3.count
                if len(tmp) != 0 and sum >= min_supp:
                    nl_next[key_next] = tmp
    return F + nlk_mining(nl_next, min_supp)


def PrePost(T, eps):

    minimum_support = len(T) * eps

    F = []
    transactions_convert(T, eps)
    root = fp_tree(T)
    ppc_tree(root, 0, 0)
    nl1 = {}
    nl1_construction(root, root, nl1)
    L1 = []
    for key in nl1:
        # print(key, *nl1[key])
        sum = 0
        for ppc_code in nl1[key]:
            sum += ppc_code.count
        L1.append((-1 * sum, key))
    L1.sort()
    L1_dict = {}
    for i in range(len(L1)):
        L1_dict[L1[i][1]] = i
        F.append((i,))

    nl2 = nl2_construction(root, L1_dict, L1, nl1, minimum_support)

    F += nlk_mining(nl2, minimum_support)
    ans = ""
    for pack in F:
        ans += '{'
        # print('{', end='')
        for i in range(len(pack)):
            if i != len(pack) - 1:
                # print(L1[pack[i]][1], end=', ')
                ans += str(L1[pack[i]][1]) + ', '
            else:
                # print(L1[pack[i]][1], end='')
                ans += str(L1[pack[i]][1])
        # print('}')
        ans += '}\n'
    return ans
