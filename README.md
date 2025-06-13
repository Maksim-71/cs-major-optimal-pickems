## 安装说明

```bash
pip install -r requirements.txt
```


## 使用方法

1. 设置胜率矩阵

    - 在 `/supplement` 中找到 `winrate.json` 和 `winrate-bo3.json` 设置您的胜率矩阵
    - 将设置好的 `winrate.json` 和 `winrate-bo3.json` 移动到根目录下
    - 可以运行`config.py`检查配置是否正确


2. 运行模拟
    
    - 设置队伍信息的路径`path_teams`和胜率矩阵的路径`path_winrate``path_winrate_bo3`
    - 设置迭代次数`n_iterations`，建议进行10000000次
    - 运行`simulate.py`
```bash
python simulate.py
```


3. 查看结果
    - 模拟结果文件名为`distributions.txt`


4. 竞猜组合求解
    - 设置模拟结果的路径`path_distributions`
    - 运行`greedy.py`
```bash
python greedy.py
```

