import os
import subprocess
from pathlib import Path
import argparse

def upscale_image(input_path, output_path, model="RealESRGAN_x4plus_anime_6B", scale=4):
    """
    使用 Real-ESRGAN 对插画图像进行超分辨率处理
    :param input_path: 输入图像路径
    :param output_path: 输出图像路径（带放大后缀）
    :param model: 使用的模型
    :param scale: 放大倍数（2 / 4 / 8）
    """
    try:
        # 检查 Real-ESRGAN 脚本
        if not os.path.exists("inference_realesrgan.py"):
            raise FileNotFoundError("❌ 没找到 inference_realesrgan.py，请确认当前目录是 Real-ESRGAN 项目目录")

        # 执行命令
        cmd = [
            "python3", "inference_realesrgan.py",
            "-n", model,
            "-s", str(scale),
            "-i", str(input_path),
            "-o", str(output_path)
        ]

        print(f"▶️ 正在处理: {input_path}  (放大 {scale}x, 模型: {model})")
        subprocess.run(cmd, check=True)
        print(f"✅ 已完成: {output_path}")

    except Exception as e:
        print("❌ 出错了：", e)


if __name__ == "__main__":
    # ===== 参数解析 =====
    parser = argparse.ArgumentParser(description="批量插画高清化脚本（Real-ESRGAN）")
    parser.add_argument("--scale", type=int, default=4, choices=[2, 4, 8], help="放大倍数（2 / 4 / 8，默认4）")
    parser.add_argument("--model", type=str, default="RealESRGAN_x4plus_anime_6B",
                        choices=["RealESRGAN_x4plus", "RealESRGAN_x4plus_anime_6B"],
                        help="使用的模型：RealESRGAN_x4plus（通用），RealESRGAN_x4plus_anime_6B（插画推荐）")
    args = parser.parse_args()

    # 输入输出目录
    input_dir = Path("inputs")
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    # 遍历所有图像文件
    supported_ext = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in supported_ext]

    if not files:
        print("⚠️ inputs 文件夹里没有找到图像，请放入要处理的插画")
    else:
        for file in files:
            # 给输出文件名加上 _{scale}x 后缀
            new_name = f"{file.stem}_{args.scale}x{file.suffix}"
            output_path = output_dir / new_name
            upscale_image(file, output_path, model=args.model, scale=args.scale)
