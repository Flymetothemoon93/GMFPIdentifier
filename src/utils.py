import os

def create_output_dir(output_dir):
    """如果输出目录不存在，则创建它"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
