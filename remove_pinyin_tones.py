#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LMDG词库拼音声调转换脚本
将带声调的拼音转换为不带声调的拼音，使其兼容Rime小鹤双拼方案
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

# 完整的声调字符映射表
TONE_MAP = {
    # a 的声调
    'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a', 'ɑ̄': 'a', 'ɑ́': 'a', 'ɑ̌': 'a', 'ɑ̀': 'a',
    # e 的声调
    'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e', 'ê̄': 'e', 'ế': 'e', 'ê̌': 'e', 'ề': 'e',
    # i 的声调
    'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
    # o 的声调
    'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
    # u 的声调
    'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
    # ü 的声调
    'ǖ': 'ü', 'ǘ': 'ü', 'ǚ': 'ü', 'ǜ': 'ü', 'ü': 'ü',
    # v 作为 ü 的替代
    'ǖ': 'v', 'ǘ': 'v', 'ǚ': 'v', 'ǜ': 'v',
    # n, m 的声调（用于鼻音韵母）
    'ń': 'n', 'ň': 'n', 'ǹ': 'n',
    'ḿ': 'm', 'm̀': 'm',
}


def remove_tone(char):
    """移除单个字符的声调"""
    return TONE_MAP.get(char, char)


def remove_tones_from_pinyin(pinyin_text):
    """
    移除拼音文本中的所有声调
    
    Args:
        pinyin_text: 带声调的拼音文本
    
    Returns:
        不带声调的拼音文本
    """
    result = []
    for char in pinyin_text:
        result.append(remove_tone(char))
    return ''.join(result)


def process_dict_line(line, line_num):
    """
    处理词典文件的一行
    
    Args:
        line: 原始行文本
        line_num: 行号（用于调试）
    
    Returns:
        转换后的行文本
    """
    # 跳过注释行、空行和元数据行
    if line.startswith('#') or line.strip() == '' or line.startswith('---') or line == '...\n':
        return line
    
    # 跳过配置行（name, version, sort等）
    if ':' in line and '\t' not in line:
        return line
    
    # 处理词条行（格式：词语\t拼音\t权重）
    if '\t' in line:
        parts = line.split('\t')
        if len(parts) >= 2:
            word = parts[0]  # 词语
            pinyin = parts[1]  # 拼音
            rest = parts[2:] if len(parts) > 2 else []  # 权重等其他字段
            
            # 转换拼音中的声调
            pinyin_no_tone = remove_tones_from_pinyin(pinyin)
            
            # 重新组合
            new_parts = [word, pinyin_no_tone] + rest
            return '\t'.join(new_parts)
    
    return line


def convert_dict_file(input_file, output_file=None, create_backup=True):
    """
    转换词典文件
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径（如果为None，则覆盖原文件）
        create_backup: 是否创建备份文件
    
    Returns:
        转换统计信息字典
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_file}")
    
    # 创建备份
    if create_backup:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = input_path.with_suffix(f'.backup_{timestamp}.yaml')
        shutil.copy2(input_path, backup_path)
        print(f"✓ 已创建备份文件: {backup_path}")
    
    # 读取原文件
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 转换统计
    stats = {
        'total_lines': len(lines),
        'converted_lines': 0,
        'skipped_lines': 0,
        'header_lines': 0
    }
    
    # 处理每一行
    converted_lines = []
    for i, line in enumerate(lines, 1):
        new_line = process_dict_line(line, i)
        converted_lines.append(new_line)
        
        # 统计
        if new_line != line and '\t' in line:
            stats['converted_lines'] += 1
        elif line.startswith('#') or line.strip() == '' or ':' in line:
            stats['header_lines'] += 1
        else:
            stats['skipped_lines'] += 1
    
    # 确定输出文件
    if output_file is None:
        output_path = input_path
    else:
        output_path = Path(output_file)
    
    # 写入转换后的内容
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(converted_lines)
    
    print(f"✓ 转换完成: {output_path}")
    
    return stats


def main():
    """主函数"""
    import sys
    
    print("=" * 60)
    print("LMDG词库拼音声调转换工具")
    print("=" * 60)
    print()
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        # 用户指定了文件名
        dict_files = sys.argv[1:]
    else:
        # 显示使用说明
        print("📖 使用方法:")
        print()
        print("   单个文件:")
        print("   python3 remove_pinyin_tones.py <文件名.dict.yaml>")
        print()
        print("   多个文件:")
        print("   python3 remove_pinyin_tones.py 文件1.dict.yaml 文件2.dict.yaml ...")
        print()
        print("   所有词库文件:")
        print("   python3 remove_pinyin_tones.py *.dict.yaml")
        print()
        print("=" * 60)
        return 0
    
    # 处理每个文件
    total_files = len(dict_files)
    success_count = 0
    
    for i, dict_file in enumerate(dict_files, 1):
        # 跳过备份文件
        if '.backup_' in dict_file:
            print(f"⏭️  跳过备份文件: {dict_file}")
            continue
        
        print(f"\n[{i}/{total_files}] 处理文件: {dict_file}")
        print("-" * 60)
        
        try:
            # 执行转换
            stats = convert_dict_file(dict_file, create_backup=True)
            
            # 显示统计信息
            print()
            print("📊 转换统计:")
            print(f"   总行数: {stats['total_lines']}")
            print(f"   转换行数: {stats['converted_lines']}")
            print(f"   头部/配置行: {stats['header_lines']}")
            print(f"   跳过行数: {stats['skipped_lines']}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()
    
    # 汇总
    print()
    print("=" * 60)
    print(f"✅ 完成! 成功处理 {success_count}/{total_files} 个文件")
    print("=" * 60)
    
    return 0 if success_count == total_files else 1


if __name__ == "__main__":
    exit(main())
