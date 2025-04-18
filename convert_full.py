# -*- coding: utf-8 -*-
# 作者: kongge
# 版本: 1.0.0
import os
import subprocess
import sys
from PIL import Image
import time  # 导入 time 模块

def get_unique_filename(directory, base_name, extension):
    """
        directory (str): 文件所在的目录。
        base_name (str): 文件名的基本部分。
        extension (str): 文件扩展名（包含点）。
    Returns:
        str: 唯一的完整文件名。
    """
    filepath = os.path.join(directory, base_name + extension)
    if not os.path.exists(filepath):
        return filepath

    counter = 1
    while True:
        new_filename = os.path.join(directory, f"{base_name}{counter}{extension}")
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1

def convert_png_to_dxf(png_input_path, dxf_output_path, potrace_path="potrace"):
    """
    通过灰度化和矢量化，将 PNG 图片转换为填充的 DXF 文件。

    Args:
        png_input_path (str): 输入 PNG 文件的路径。
        dxf_output_path (str): 输出 DXF 文件的路径。
        potrace_path (str): potrace 可执行文件的路径。
        默认为 'potrace'，假设它在系统 PATH 中。
    Returns:
        bool: 如果成功则返回 True，否则返回 False。
    """
    print(f"\n开始处理: {os.path.basename(png_input_path)}")
    print(f"  输入: {png_input_path}")
    print(f"  输出 DXF 将保存至: {dxf_output_path}")

    # --- 验证输入 ---
    if not os.path.exists(png_input_path):
        print(f"错误: 输入文件未找到: '{png_input_path}'")
        return False
    # 简单检查是否是 PNG
    if not png_input_path.lower().endswith('.png'):
        print(f"错误: 文件 '{os.path.basename(png_input_path)}' 不是 PNG 格式。已跳过。")
        return False

    # 从输入路径获取基本文件名和目录
    base_name = os.path.splitext(os.path.basename(png_input_path))[0]
    # 将临时文件存储在输入文件所在的目录，避免权限问题
    temp_dir = os.path.dirname(png_input_path)

    # 定义临时位图文件路径 (potrace 对 BMP 格式支持良好)
    # 添加时间戳或唯一标识符避免多文件同时处理时的冲突 (虽然拖拽通常是顺序执行)
    timestamp = int(time.time() * 1000)
    temp_bmp_path = os.path.join(temp_dir, f"{base_name}_temp_{timestamp}.bmp")
    print(f"  临时文件: {temp_bmp_path}")

    try:
        # --- 加载 PNG 并转换为灰度图/黑白图 ---
        print("  步骤 1: 加载 PNG 并转换为黑白图...")
        img = Image.open(png_input_path)
        gray_img = img.convert('L')
        threshold = 128
        bw_img = gray_img.point(lambda p: 0 if p < threshold else 255, '1')
        bw_img.save(temp_bmp_path, "BMP")
        print("  步骤 1: 完成。")

        # --- 使用 potrace 进行矢量化 (输出为 DXF，并启用填充) ---
        print("  步骤 2: 使用 potrace 进行矢量化...")
        output_dir = os.path.dirname(dxf_output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        command = [
            potrace_path,
            "-b", "dxf",
            "-o", dxf_output_path,
            "--fillcolor", "#000000",
            "--",
            temp_bmp_path
        ]

        result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8')

        if result.returncode != 0:
            print(f"  错误: 运行 potrace 失败 (返回码 {result.returncode})。")
            print("  Potrace 输出:")
            stderr_lines = result.stderr.strip().splitlines()
            print("  " + "\n  ".join(stderr_lines[-5:]))
            if "No such file or directory" in result.stderr or "not found" in result.stderr or result.returncode == 127 or "'potrace' 不是内部或外部命令" in result.stderr:
                print("\n  *** 错误: 未找到 'potrace' 命令。请确保已安装 potrace 并将其添加到系统 PATH。***")
            return False
        else:
            if result.stderr:
                print("  Potrace 警告信息:")
                print("  " + "\n  ".join(result.stderr.strip().splitlines()))
            print(f"  步骤 2: 完成。DXF 文件已创建: {dxf_output_path}")
            return True

    except FileNotFoundError:
        print(f"\n*** 错误: 未找到命令或程序 '{potrace_path}'。 ***")
        print("请安装 potrace 并确保它位于系统的 PATH 环境变量中。")
        return False
    except Exception as e:
        print(f"  处理文件时发生意外错误: {e}")
        return False
    finally:
        # --- 清理临时文件 ---
        if os.path.exists(temp_bmp_path):
            try:
                os.remove(temp_bmp_path)
            except Exception as e:
                print(f"  警告: 无法删除临时文件 {temp_bmp_path}: {e}")


# --- 脚本入口和使用说明 ---
if __name__ == "__main__":
    # 检查是否有文件被拖拽进来 (参数数量大于1)
    if len(sys.argv) < 2:
        print("请将一个或多个 PNG 文件拖拽到此脚本图标上进行转换。")
        print("\n脚本会自动将转换后的 DXF 文件保存在与原 PNG 文件相同的目录下，")
        print("文件名为 convert.dxf，如果已存在则自动添加数字编号。")
        input("按 Enter 键退出...")
        sys.exit(0)

    # 获取当前可执行文件所在的目录
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # 构建 potrace.exe 的完整路径
    potrace_executable = os.path.join(base_dir, "potrace", "potrace.exe")

    print("开始批量处理拖拽的文件...")
    print(f"将使用 Potrace: {potrace_executable}")
    print("-" * 30)

    success_count = 0
    fail_count = 0

    # 遍历所有拖拽进来的文件路径 (从 sys.argv[1] 开始)
    for input_file_path in sys.argv[1:]:
        # 自动生成输出文件路径 (与输入文件同目录，固定文件名为 convert.dxf)
        output_dir = os.path.dirname(input_file_path)
        output_file_path = get_unique_filename(output_dir, "convert", ".dxf")

        # 调用转换函数处理单个文件
        success = convert_png_to_dxf(input_file_path, output_file_path, potrace_executable)

        if success:
            success_count += 1
            print(f"成功转换: {os.path.basename(input_file_path)} -> {os.path.basename(output_file_path)}")
        else:
            fail_count += 1
            print(f"转换失败: {os.path.basename(input_file_path)}")
        print("-" * 30)  # 每个文件处理后加分隔线

    print("\n批量处理完成。")
    print(f"总计: {success_count} 个文件成功转换, {fail_count} 个文件失败。")
    print("\n提醒：生成的 DXF 文件需要使用 CAD 软件 (如 AutoCAD) 或")
    print("专用转换器 (如 ODA File Converter) 来查看或转换为 DWG 文件。")
    input("\n按 Enter 键退出...")
    sys.exit(0)