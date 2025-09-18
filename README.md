# 香港天文台海平面数据可视化

这个项目从香港天文台爬取了鲗鱼涌站(QUB)的海平面数据，并创建了多种可视化图表。

## 数据来源
- **数据站点**: 香港天文台鲗鱼涌站 (QUB)
- **数据范围**: 1954-2024年 (71年)
- **数据源**: HKO XML数据接口

## 主要文件

### 数据文件
- `HKO_QUB_SeaLevel_Data_20250918_163225.csv` - 完整海平面数据
- `HKO_QUB_MeanSeaLevel_Simple_20250918_163225.csv` - 简化的年均海平面数据
- `HKO_QUB_SeaLevel_Metadata_20250918_163225.json` - 数据元信息

### 程序文件
- `crawl_hko_sea_level.py` - 数据爬取程序
- `animated_sea_level.py` - **主要可视化程序** (动画极坐标图)
- `visualize_sea_level_english.py` - 传统2D分析图表

### 生成的图表
- `HKO_SeaLevel_Animation_*.gif` - **动画可视化** (主要输出)
- `HKO_Comprehensive_SeaLevel_Analysis_*.png` - 综合分析图
- 其他传统分析图表

## 使用方法

### 运行动画可视化 (推荐)
```bash
python animated_sea_level.py
```

这会生成：
1. **动画GIF** - 从1954年第一个点开始，逐年向外连线到2024年
   - 极坐标展示
   - 71年完整数据动画
   - 实时信息显示
   - 颜色渐变效果

### 运行传统分析
```bash
python visualize_sea_level_english.py
```

### 重新爬取数据
```bash
python crawl_hko_sea_level.py
```

## 数据特点

- **时间跨度**: 71年完整记录
- **海平面范围**: 1.28-1.51米
- **长期趋势**: 总体上升趋势
- **年代变化**: 按10年周期分析显示明显的阶段性变化

## 可视化特色

### 动画效果
- **逐年连线**: 从1954年第一个点开始，逐年向外连线
- **极坐标展示**: 角度表示时间，半径表示海平面高度
- **实时信息**: 显示当前年份、海平面高度、进度
- **颜色渐变**: 基于时间的颜色映射
- **20秒动画**: 完整展示71年数据变化

### 传统图表
- 详细的统计分析
- 趋势线和回归分析
- 分年代的箱型图
- 完整的数据报告

## 环境要求
```
pandas
numpy
matplotlib
requests
beautifulsoup4
```

## 作者
数据来源：香港天文台
处理分析：海平面数据可视化项目