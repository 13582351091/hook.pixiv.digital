import json
import os
# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.realpath(__file__))
# 读取配置文件
with open(os.path.join(current_dir, 'config.json'), 'r') as f:
    config = json.load(f)

if __name__ == '__main__':
    print(config['notify'])
