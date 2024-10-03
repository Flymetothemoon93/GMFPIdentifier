import os
import subprocess

def test_fpidentifier():
    # 定义测试文件的路径
    test_data_dir = "test/test_data"
    rice_fasta = os.path.join(test_data_dir, "rice_with_TE.fasta")
    arabidopsis_fasta = os.path.join(test_data_dir, "arabidopsis_with_TE.fasta")
    
    # 定义输出文件夹
    output_dir = "test/test_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 定义输出文件
    rice_output = os.path.join(output_dir, "rice_results.txt")
    arabidopsis_output = os.path.join(output_dir, "arabidopsis_results.txt")
    
    # 运行 FPIdentifier 主程序对 rice 进行测试
    rice_cmd = f"python src/main.py --input {rice_fasta} --output {rice_output}"
    arabidopsis_cmd = f"python src/main.py --input {arabidopsis_fasta} --output {arabidopsis_output}"
    
    try:
        print("Testing rice_with_TE.fasta...")
        subprocess.run(rice_cmd, shell=True, check=True)
        print(f"Rice test completed. Output saved to: {rice_output}")
        
        print("Testing arabidopsis_with_TE.fasta...")
        subprocess.run(arabidopsis_cmd, shell=True, check=True)
        print(f"Arabidopsis test completed. Output saved to: {arabidopsis_output}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    test_fpidentifier()
