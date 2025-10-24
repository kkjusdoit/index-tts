#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexTTS2 批量音色克隆工具
上传包含 .wav 文件的文件夹，系统将自动：
1. 遍历文件夹中的所有 .wav 文件
2. 使用每个音频文件作为音色参考
3. 从文件名提取文本（自动去除序号如 '1-'、'1'、'1' 等）
4. 生成对应的语音文件（保留原序号）
"""

import argparse
import os
import re
from pathlib import Path
from indextts.infer_v2 import IndexTTS2
from tqdm import tqdm

def extract_text_from_filename(filename):
    """
    从文件名中提取文本，去除序号和扩展名
    
    示例:
    - 1 how old are you.wav -> how old are you
    - 1-how old are you.wav -> how old are you
    - 1how are you.wav -> how are you
    - 15-你好世界.wav -> 你好世界
    - 15你好世界.wav -> 你好世界
    """
    # 去除扩展名
    name = Path(filename).stem
    
    # 去除开头的数字和连接符（支持多种格式）
    # 匹配: 数字 + 可选的(空格/横线/下划线) 
    name = re.sub(r'^\d+[\s\-_]*', '', name)
    
    # 去除开头和结尾的空格
    name = name.strip()
    
    return name

def get_prefix_from_filename(filename):
    """
    从文件名中提取序号前缀
    
    示例:
    - 1 how old are you.wav -> 1
    - 1-how old are you.wav -> 1-
    - 15-你好世界.wav -> 15-
    """
    name = Path(filename).stem
    match = re.match(r'^(\d+[\s\-_]*)', name)
    return match.group(1) if match else ''

def batch_clone(input_dir, output_dir=None, model_dir='checkpoints', cfg_path='checkpoints/config.yaml'):
    """
    批量克隆文件夹中的音频文件
    """
    input_path = Path(input_dir)
    
    # 如果没有指定输出目录，默认在输入目录下创建 "文件夹名_en" 子文件夹
    if output_dir is None:
        folder_name = input_path.name  # 获取输入文件夹的名字
        output_path = input_path / f'{folder_name}_en'
    else:
        output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        return
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 获取所有 .wav 文件
    wav_files = sorted(input_path.glob('*.wav'))
    
    if not wav_files:
        print(f"❌ 目录中没有找到 .wav 文件: {input_dir}")
        return
    
    print(f"\n{'='*80}")
    print(f"IndexTTS2 批量音色克隆")
    print(f"{'='*80}")
    print(f"📁 输入目录: {input_dir}")
    print(f"📂 输出目录: {output_dir}")
    print(f"🎵 找到 {len(wav_files)} 个音频文件")
    print(f"{'='*80}\n")
    
    # 初始化模型
    print("⏳ 加载模型...")
    tts = IndexTTS2(
        cfg_path=cfg_path,
        model_dir=model_dir,
        use_fp16=False,
        use_cuda_kernel=False,
        use_deepspeed=False
    )
    print("✅ 模型加载完成\n")
    
    # 批量处理
    success_count = 0
    failed_files = []
    
    for wav_file in tqdm(wav_files, desc="🎙️ 处理进度", unit="文件"):
        try:
            # 提取文本和序号
            text = extract_text_from_filename(wav_file.name)
            prefix = get_prefix_from_filename(wav_file.name)
            
            if not text:
                print(f"\n⚠️ 跳过文件（无法提取文本）: {wav_file.name}")
                continue
            
            # 生成输出文件名（保留原序号）
            output_filename = f"{prefix}{text}.wav" if prefix else f"{text}.wav"
            output_file = output_path / output_filename
            
            # 显示当前处理的文件
            tqdm.write(f"\n📝 处理: {wav_file.name}")
            tqdm.write(f"   文本: {text}")
            tqdm.write(f"   输出: {output_filename}")
            
            # 生成语音
            tts.infer(
                spk_audio_prompt=str(wav_file),
                text=text,
                output_path=str(output_file),
                verbose=False  # 不显示详细输出
            )
            
            success_count += 1
            tqdm.write(f"   ✅ 完成")
            
        except Exception as e:
            tqdm.write(f"\n❌ 处理失败: {wav_file.name}")
            tqdm.write(f"   错误: {str(e)}")
            failed_files.append((wav_file.name, str(e)))
    
    # 显示最终统计
    print(f"\n{'='*80}")
    print(f"批量处理完成!")
    print(f"{'='*80}")
    print(f"✅ 成功: {success_count}/{len(wav_files)}")
    if failed_files:
        print(f"❌ 失败: {len(failed_files)}")
        print(f"\n失败的文件:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    print(f"\n📂 输出目录: {output_dir}")
    print(f"{'='*80}\n")

def main():
    parser = argparse.ArgumentParser(
        description='IndexTTS2 批量音色克隆工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --input ./input_wavs  # 输出到 ./input_wavs/cn/
  %(prog)s -i ./my_audio --output ./custom_output  # 自定义输出目录
  %(prog)s -i ./my_audio -m checkpoints -c checkpoints/config.yaml

文件命名规则:
  输入文件名会自动提取文本内容（去除序号前缀）:
    1 how old are you.wav → Text: "how old are you" → 输出: 1-how old are you.wav
    1-how old are you.wav → Text: "how old are you" → 输出: 1-how old are you.wav
    15-你好世界.wav → Text: "你好世界" → 输出: 15-你好世界.wav
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='包含 .wav 文件的输入文件夹路径')
    parser.add_argument('--output', '-o', default=None, help='输出文件夹路径（默认: 输入目录下的 cn 文件夹）')
    parser.add_argument('--model-dir', '-m', default='checkpoints', help='模型目录路径（默认: checkpoints）')
    parser.add_argument('--cfg-path', '-c', default='checkpoints/config.yaml', help='配置文件路径（默认: checkpoints/config.yaml）')
    
    args = parser.parse_args()
    
    batch_clone(
        input_dir=args.input,
        output_dir=args.output,
        model_dir=args.model_dir,
        cfg_path=args.cfg_path
    )

if __name__ == "__main__":
    main()

