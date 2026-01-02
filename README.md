# Rime-词库拼音声调转换脚本

### ✨ 脚本特性

✅ 自动备份：每次转换前自动创建带时间戳的备份

✅ 批量处理：一次处理多个文件

✅ 智能跳过：自动跳过备份文件

✅ 详细统计：显示每个文件的转换统计

✅ 安全可靠：出错不影响其他文件


<img alt="Cl 2026-01-02 15 17 10" src="https://github.com/user-attachments/assets/f5d5549a-0861-4843-96dc-afd5f4be5563" />

```
python3 remove_pinyin_tones.py *.dict.yaml
```
## 📖 使用方法
### 方法一：处理单个文件




```
cd /Users/time/Downloads/未命名文件夹/fcitx5/rime/cn_dicts
python3 remove_pinyin_tones.py lmdg-cuoyin.dict.yaml
```
### 方法二：处理多个指定文件
```
python3 remove_pinyin_tones.py lmdg-cuoyin.dict.yaml lmdg-jichu.dict.yaml lmdg-lianxiang.dict.yaml
```
### 方法三：处理所有词库文件（推荐） ⭐
```
python3 remove_pinyin_tones.py *.dict.yaml
```
这会自动处理目录下所有 .dict.yaml 文件，已转换过的文件和备份文件会自动跳过。

### 方法四：查看使用说明
```
python3 remove_pinyin_tones.py
```
不加任何参数，会显示使用说明。
