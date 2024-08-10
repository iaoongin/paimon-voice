# 派蒙语音

让世界任务剧情有语音。

# 原理

截图 -> 文本 -> 朗读

# 演示

<video id="video" controls="" preload="none">
    <source id="mp4" src="assets/paimon-voice-demo.mp4" type="video/mp4">
</video>


# 下载模型


1. 语义分割模型
`https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/paraphrase-multilingual-MiniLM-L12-v2.zip`

    解压到 `model/paraphrase-multilingual-MiniLM-L12-v2`


2. vits模型

    2.1 
    `https://github.com/iaoongin/VITS-Paimon/archive/refs/tags/model.zip`

    解压到 `model/VITS-Paimon`

    2.2 `https://github.com/iaoongin/VITS-Paimon/releases/download/model/G_1434000.pth`

    下载到 `model/VITS-Paimon/content/VITS-Paimon/G_1434000.pth`


# 安装依赖

## 当前项目
```
pip install -r requirements.txt
```
## VITS-Paimon项目
```
cd model/VITS-Paimon
pip install -r requirements.txt
```

# 运行

```
python main.py
```