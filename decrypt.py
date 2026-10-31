# -*- coding: utf-8 -*-
"""解密本仓库的分卷并还原图片。

用法（在有 Python + cryptography 的机器上）：
    pip install cryptography
    python decrypt.py            # 解到 ./out/
    python decrypt.py -o ./restored

原理：每个 part_XXX.zip.enc = nonce(12 字节) || AES-256-GCM 密文 || tag(16 字节)
密钥：KEY.txt 里的 KEY_B64（base64 编码的 32 字节 AES-256 密钥）
"""
import argparse
import base64
import glob
import os
import sys
import zipfile
import io

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def load_key(path="KEY.txt"):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("KEY_B64="):
                return base64.b64decode(line.split("=", 1)[1])
    raise SystemExit("KEY.txt 里没找到 KEY_B64")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="out", help="输出目录")
    ap.add_argument("-k", "--key", default="KEY.txt")
    a = ap.parse_args()

    key = load_key(a.key)
    aes = AESGCM(key)
    os.makedirs(a.out, exist_ok=True)

    parts = sorted(glob.glob("part_*.zip.enc"))
    if not parts:
        raise SystemExit("当前目录没有 part_*.zip.enc")

    total = 0
    for p in parts:
        with open(p, "rb") as f:
            blob = f.read()
        nonce, ct = blob[:12], blob[12:]
        try:
            raw = aes.decrypt(nonce, ct, None)
        except Exception as e:
            raise SystemExit("%s 解密失败（密钥不对或文件损坏）：%s" % (p, e))
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            z.extractall(a.out)
            total += len(names)
        print("%s -> %d files" % (p, len(names)))
    print("done: %d files -> %s" % (total, os.path.abspath(a.out)))


if __name__ == "__main__":
    main()
