# CUMCM24A题

## 文件目录

| 文件名 | 可能的功能描述 |
| --- | --- |
| boat.py | 板凳龙建模，包含板凳龙对象和板凳的对象 |
| map.py | 等距螺线对象 |
| q1.py, q2.py, q3.py, q4.py | 问题一至四的Python主程序 |
| q4_module.py | 问题四与五的Python模块，用于处理调头分段曲线，实际上是boat.py和map.py的整合并重写为以距离为标定的版本 |
| q4_pre.py | 问题四的预处理程序 |
| q4_visualization.py | 问题四的数据可视化程序 |
| q5_1_fix_boat_multicore.py | 问题五的Python程序之一，使用多核加快计算整条龙所有把手最大速度/单个把手速度随时间/距离变化关系，适用于MacOS或Linux（未测试） |
| q5_1_fix_boat_singlecore.py | 同上，适用于Windows |
| q5_2_fix_time.py | 问题五的Python程序之二，计算同一时刻不同把手的速度 |
| q5_3_find_max.py | 问题五的Python程序之三，寻找全过程最大值 |
| q1_plot_300s_v.py, q1_plot_300s_x.py, q1_plot_v.py, q1_plot_x.py, q2_plot.py, q3_plot.py, q4_plot_all_v.py, q4_plot_all_x.py | 作图文件 |
| Excel_output/ | Excel输出文件（用于保存最后结果数据）（文件夹） |
| q5_data/ | 问题五的数据（用于保存中间结果防止重复计算）（文件夹） |
| results/ | 结果文件（中间文件）（文件夹） |
| pics/ | 项目所绘制的图片 |
| README.md | 项目说明文档 |
| requirements.txt | 项目依赖库列表 |
| .gitignore | Git版本控制忽略文件 |

## 使用方法
### 安装依赖库
```bash
pip install -r requirements.txt
```

### 运行程序
举例
```bash
python -u q1.py
```

### 注意q4顺序
除了问题四代码以外所有代码均可直接运行（作图文件除外）
1. 先运行q4_pre.py
2. 再运行q4.py
3. 最后运行q4_visualization.py
