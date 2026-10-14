#!/usr/bin/env python3
"""Reducer - Chu de 2: Goi y nguoi quen (Hadoop Streaming).
Nhan cac dong da sap xep theo key (U1,U2). Loai cap co nhan DIRECT,
cong so ban chung cho cac cap con lai, xuat Top 2 cho moi nguoi dung
(diem giam dan; bang diem thi ten tang dan)."""
import sys
from collections import defaultdict

current_key = None
is_direct_friend = False
mutual_friends = set()

recommendations = defaultdict(list)   # user -> [(score, candidate, [mutuals])]
all_users = set()


def process_pair(key, is_direct, mutual_set):
    if not key:
        return
    if key.startswith("USER_ONLY,"):
        all_users.add(key.split(",", 1)[1])
        return

    u1, u2 = key.split(",", 1)
    all_users.add(u1)
    all_users.add(u2)

    # Chi goi y neu CHUA la ban truc tiep va co it nhat 1 ban chung
    if not is_direct and len(mutual_set) > 0:
        score = len(mutual_set)
        mutual_list = sorted(mutual_set)
        recommendations[u1].append((score, u2, mutual_list))
        recommendations[u2].append((score, u1, mutual_list))


for line in sys.stdin:
    line = line.strip()
    if not line or '\t' not in line:
        continue

    key, val = line.split('\t', 1)

    if key != current_key:
        process_pair(current_key, is_direct_friend, mutual_friends)
        current_key = key
        is_direct_friend = False
        mutual_friends = set()

    if val == "DIRECT":
        is_direct_friend = True
    elif val.startswith("1:"):
        mutual_friends.add(val.split(":", 1)[1])

process_pair(current_key, is_direct_friend, mutual_friends)

for user in sorted(all_users):
    cand_list = recommendations[user]
    cand_list.sort(key=lambda x: (-x[0], x[1]))
    top_2 = cand_list[:2]
    if top_2:
        formatted = ", ".join(f"{cand} ({score})" for score, cand, _ in top_2)
    else:
        formatted = "Không có gợi ý (0)"
    print(f"{user}\t{formatted}")
