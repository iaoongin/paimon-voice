import subprocess

# 运行另外一个Python脚本，并传递参数
result = subprocess.run(['python', 'test.py', "我的身体?我的身体怎么了么?"], cwd="../model/VITS-Paimon", capture_output=True)

# print(result)