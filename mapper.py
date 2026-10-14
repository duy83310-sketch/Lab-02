#!/usr/bin/env python3
"""Mapper - Chu de 2: Goi y nguoi quen (Hadoop Streaming).
Dau vao : moi dong "User<TAB>Ban1,Ban2,..." (cung chap nhan "User: Ban1, Ban2").
Dau ra  : key<TAB>value
          - "U1,U2<TAB>DIRECT"   : hai nguoi da la ban truc tiep
          - "U1,U2<TAB>1:X"      : U1, U2 co chung nguoi ban X
          - "USER_ONLY,U<TAB>NONE": nguoi dung khong co ban (de van xuat dong ket qua)
"""
import sys


def make_pair_key(u1, u2):
    """Chuan hoa khoa cap vo huong: min,max theo thu tu tu dien."""
    return f"{u1},{u2}" if u1 < u2 else f"{u2},{u1}"


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    if '\t' in line:
        parts = line.split('\t', 1)
    elif ':' in line:
        parts = line.split(':', 1)
    else:
        parts = line.split(None, 1)

    user = parts[0].strip()
    if not user:
        continue

    if len(parts) < 2 or not parts[1].strip():
        print(f"USER_ONLY,{user}\tNONE")
        continue

    raw_friends = [f.strip() for f in parts[1].split(',') if f.strip()]
    # Loai tu ket ban (f != user) va khu trung lap bang set()
    friends = sorted(set(f for f in raw_friends if f != user))

    if not friends:
        print(f"USER_ONLY,{user}\tNONE")
        continue

    # 1. Danh dau quan he ban be truc tiep
    for f in friends:
        print(f"{make_pair_key(user, f)}\tDIRECT")

    # 2. Sinh ung vien: moi cap trong danh sach ban cua user co 1 ban chung la user
    n = len(friends)
    for i in range(n):
        for j in range(i + 1, n):
            print(f"{make_pair_key(friends[i], friends[j])}\t1:{user}")
