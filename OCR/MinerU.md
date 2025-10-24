国内环境配置
如果你的网络环境相当好，上述的docker镜像很快就完成了。当然，大部分情况下速度没那么快，而且可能还会网络中断。
替换download_models.py文件，原本的模型是通过HuggingFace下载，大概率是网络受限的，替换官方使用ModelScope下载的方式
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/scripts/download_models.py -O download_models.py


直接替换为
import json
import shutil
import os

import requests
from modelscope import snapshot_download


def download_json(url):
    # 下载JSON文件
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    return response.json()


def download_and_modify_json(url, local_filename, modifications):
    if os.path.exists(local_filename):
        data = json.load(open(local_filename))
        config_version = data.get('config_version', '0.0.0')
        if config_version < '1.2.0':
            data = download_json(url)
    else:
        data = download_json(url)

    # 修改内容
    for key, value in modifications.items():
        data[key] = value

    # 保存修改后的内容
    with open(local_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    mineru_patterns = [
        # "models/Layout/LayoutLMv3/*",
        "models/Layout/YOLO/*",
        "models/MFD/YOLO/*",
        "models/MFR/unimernet_hf_small_2503/*",
        "models/OCR/paddleocr_torch/*",
        # "models/TabRec/TableMaster/*",
        # "models/TabRec/StructEqTable/*",
    ]
    model_dir = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=mineru_patterns)
    layoutreader_model_dir = snapshot_download('ppaanngggg/layoutreader')
    model_dir = model_dir + '/models'
    print(f'model_dir is: {model_dir}')
    print(f'layoutreader_model_dir is: {layoutreader_model_dir}')

    # paddleocr_model_dir = model_dir + '/OCR/paddleocr'
    # user_paddleocr_dir = os.path.expanduser('~/.paddleocr')
    # if os.path.exists(user_paddleocr_dir):
    #     shutil.rmtree(user_paddleocr_dir)
    # shutil.copytree(paddleocr_model_dir, user_paddleocr_dir)

    json_url = 'https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/magic-pdf.template.json'
    config_file_name = 'magic-pdf.json'
    home_dir = os.path.expanduser('~')
    config_file = os.path.join(home_dir, config_file_name)

    json_mods = {
        'models-dir': model_dir,
        'layoutreader-model-dir': layoutreader_model_dir,
    }

    download_and_modify_json(json_url, config_file, json_mods)
    print(f'The configuration file has been configured successfully, the path is: {config_file}')

修改 requirements.txt 增加魔塔社区
modelscope
配置magic-pdf.json
 配置文件会自动生成在用户目录下，文件名为magic-pdf.json。你可以根据需要修改配置文件中的功能开关
{
"bucket_info": {
"bucket-name-1": [
"ak",
"sk",
"endpoint"
]
},
"models-dir": "{path}/models", # 这里的path默认会是模型下载下来的路径，也可以挪动模型，修改路径
"layoutreader-model-dir": "{path}/layoutreader",
"device-mode": "cpu", # 配置服务运行的基础环境，如果是cpu环境就配置cpu，如果是gup cuda，这里就配置为cuda
"layout-config": {
"model": "layoutlmv3" // 使用layoutlmv3请修改为“layoutlmv3"
},
"formula-config": {
"mfd_model": "yolo_v8_mfd",
"mfr_model": "unimernet_small",
"enable": true // 公式识别功能默认是开启的，如果需要关闭请修改此处的值为"false"
},
"table-config": {
"model": "rapid_table", // 表格识别默认使用"rapid_table"这个速度最快,可以切换为"tablemaster"和"struct_eqtable"
"enable": false, // 表格识别功能默认是开启的，如果需要关闭请修改此处的值为"false"
"max_time": 400
},
"config_version": "1.0.0"
}
修改Dockerfile
在Dockerfile中添加一些镜像站，如下
## 修改docker镜像源
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10-slim-bookworm AS base

## 【添加】
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build Python dependencies  【添加 -i https://mirrors.aliyun.com/pypi/simple/】
COPY requirements.txt .
RUN python -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \
    pip3 install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/

另外，我们更换了download_models.py文件，模型下载地址发生了变更，因此下面两行也需要修改
# Copy Python dependencies and models from the build stage
COPY --from=build /root/.cache/modelscope/hub/models/opendatalab/PDF-Extract-Kit-1___0/models  /opt/models
COPY --from=build /root/.cache/modelscope/hub/models/ppaanngggg/layoutreader  /opt/layoutreader

根据上述修改，基本上能快速构建镜像了。
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10-slim-bookworm AS base

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1


FROM base AS build

# 修改源
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Build Python dependencies  【添加 -i https://mirrors.aliyun.com/pypi/simple/】
# Build Python dependencies
COPY requirements.txt .
RUN python -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \

    pip3 install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/
#     pip uninstall -y paddlepaddle && \
#     pip install -i https://www.paddlepaddle.org.cn/packages/stable/cu118/ \
#         paddlepaddle-gpu==3.0.0rc1

# Download models
COPY download_models.py .
RUN . /app/venv/bin/activate && \
    python ./download_models.py


FROM base AS prod

# Copy Python dependencies and models from the build stage
COPY --from=build /app/venv /app/venv
# COPY --from=build /opt/models /opt/models
# COPY --from=build /opt/layoutreader /opt/layoutreader
# Copy Python dependencies and models from the build stage
COPY --from=build /root/.cache/modelscope/hub/models/opendatalab/PDF-Extract-Kit-1___0/models  /opt/models
COPY --from=build /root/.cache/modelscope/hub/models/ppaanngggg/layoutreader  /opt/layoutreader
# Update the package list and install necessary packages
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create volume for paddleocr models
# RUN mkdir -p /root/.paddleocr
# VOLUME [ "/root/.paddleocr" ]

# Copy the app and its configuration file
COPY entrypoint.sh /app/entrypoint.sh
COPY magic-pdf.json /root/magic-pdf.json
COPY app.py /app/app.py

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run FastAPI using Uvicorn, pointing to app.py and binding to 0.0.0.0:8000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["--host", "0.0.0.0", "--port", "8000"]

构建镜像
docker build -t mineru-api .
docker run -d --gpus all --network docker_ssrf_proxy_network --name mineru-api mineru-api
docker run -d -it -p 8000:8000 --name mineru-api -v /宿主机/output路径:/output  mineru-api 

docker run -d -it -p 8000:8000 --name mineru-api -v /mineru/output:/output  mineru-api 

