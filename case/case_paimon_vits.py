import subprocess

# 运行另外一个Python脚本，并传递参数
result = subprocess.run(['python', 'test.py', "前面的区域，以后再来探索吧!"], cwd="../model/VITS-Paimon", capture_output=True)

# print(result)