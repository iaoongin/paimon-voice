import subprocess
import os

# 获取当前文件目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录的绝对路径
parent_dir = os.path.dirname(current_dir)

def say(text):
    print('parent_dir: %s' % parent_dir )
    # 运行另外一个Python脚本，并传递参数
    subprocess.run(['python', 'test.py', text], cwd=current_dir + "/model/VITS-Paimon", capture_output=True)
    # result = subprocess.run(['python', 'test.py'], cwd="../model/VITS-Paimon", capture_output=True)