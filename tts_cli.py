#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexTTS2 命令行工具
直接通过命令行进行语音克隆，无需 WebUI
"""

import argparse
from indextts.infer_v2 import IndexTTS2

def main():
    parser = argparse.ArgumentParser(description='IndexTTS2 命令行语音克隆工具')
    parser.add_argument('--speaker', '-s', required=True, help='说话人音频文件路径（用于克隆音色）')
    parser.add_argument('--text', '-t', required=True, help='要合成的文本内容')
    parser.add_argument('--output', '-o', default='output.wav', help='输出音频文件路径（默认: output.wav）')
    parser.add_argument('--emotion-audio', '-e', default=None, help='情感参考音频（可选）')
    parser.add_argument('--model-dir', '-m', default='checkpoints', help='模型目录路径')
    parser.add_argument('--cfg-path', '-c', default='checkpoints/config.yaml', help='配置文件路径')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"IndexTTS2 语音克隆")
    print(f"{'='*60}")
    print(f"🎤 说话人音频: {args.speaker}")
    print(f"📝 合成文本: {args.text}")
    print(f"🎵 输出文件: {args.output}")
    if args.emotion_audio:
        print(f"😊 情感参考: {args.emotion_audio}")
    print(f"{'='*60}\n")
    
    # 初始化模型
    print("⏳ 加载模型...")
    tts = IndexTTS2(
        cfg_path=args.cfg_path,
        model_dir=args.model_dir,
        use_fp16=False,
        use_cuda_kernel=False,
        use_deepspeed=False
    )
    print("✅ 模型加载完成\n")
    
    # 生成语音
    print("🎙️ 正在生成语音...")
    tts.infer(
        spk_audio_prompt=args.speaker,
        text=args.text,
        output_path=args.output,
        emo_audio_prompt=args.emotion_audio,
        verbose=True
    )
    
    print(f"\n✅ 语音合成完成！")
    print(f"📁 输出文件: {args.output}\n")

if __name__ == "__main__":
    main()

