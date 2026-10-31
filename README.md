# image-vault

加密后的图片归档。仓库内只有密文与解密脚本。

## ⚠️ 关于本仓库公开

本仓库为 **public**，且 `KEY.txt` 与密文放在一起 —— 这意味着**任何能看到本仓库的人都可以解密全部内容**。
加密在这里只做到「不被 GitHub 直接索引、不被直接预览」，**不构成访问控制**。
若不希望内容公开，请把 `KEY.txt` 从仓库移除并单独保存，同时清理提交历史。

## 内容

| 文件 | 说明 |
|---|---|
| `part_001.zip.enc` … `part_009.zip.enc` | AES-256-GCM 分卷，共 9 卷 |
| `KEY.txt` | 32 字节密钥（base64） |
| `MANIFEST.json` | 每卷的文件数、明文字节数、SHA-256 |
| `decrypt.py` | 解密与还原脚本 |

## 解密

```bash
pip install cryptography
python decrypt.py            # 解到 ./out/
python decrypt.py -o ./restored
```

## 格式

```
每个 .enc 文件 = nonce(12 字节) || AES-256-GCM 密文 || tag(16 字节)
明文 = 标准 zip，条目为相对路径
```

## 脱敏说明

- 加密前所有图片用 Pillow 重新编码，丢弃原文件内的全部 tEXt/iTXt/EXIF
  （生成工具常把提示词、模型名、工作流、本地绝对路径写进 PNG）
- 压缩包条目一律为相对路径，不含盘符、用户名或临时目录
- `MANIFEST.json` 只记录体积与哈希，不记录条目名
- 提交作者使用 noreply 地址，不含真实邮箱