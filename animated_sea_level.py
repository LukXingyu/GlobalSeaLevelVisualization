import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def load_sea_level_data():
    """加载海平面数据"""
    try:
        df = pd.read_csv('HKO_QUB_SeaLevel_Data_20250918_163225.csv')
        df = df.dropna(subset=['Mean_Sea_Level_m'])
        return df
    except FileNotFoundError:
        print("未找到数据文件！")
        return None

def create_animated_polar_chart():
    """创建动画极坐标图"""
    df = load_sea_level_data()
    if df is None:
        return
    
    years = df['Year'].values
    sea_levels = df['Mean_Sea_Level_m'].values
    
    # 按10年一个轮回计算角度
    # 每年在其所在的10年内的角度 (0到2π)
    angles = []
    decade_radii = []
    
    for year, level in zip(years, sea_levels):
        year_in_decade = year % 10  # 年份在年代内的位置 (0-9)
        angle = (year_in_decade / 10) * 2 * np.pi
        angles.append(angle)
        
        # 半径 = 年代数 + 海平面调节
        decade = int(year // 10) - 195  # 1950s=0, 1960s=1, ...
        level_offset = (level - 1.35) * 5  # 海平面偏移调节
        radius = decade + 1 + level_offset
        decade_radii.append(radius)
    
    angles = np.array(angles)
    radii = np.array(decade_radii)
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(projection='polar'))
    
    # 设置极坐标图样式
    max_radius = int(years[-1] // 10) - 195 + 3  # 最大半径
    ax.set_ylim(0, max_radius)
    ax.set_title('香港海平面变化动画 (按10年轮回)\n角度=年代内年份，半径=年代+海平面', 
                 fontsize=16, pad=30)
    
    # 设置角度标签 (年代内的年份: 0年、1年...9年)
    angle_labels = [f'{i}年' for i in range(10)]
    angle_positions = [(i / 10) * 360 for i in range(10)]
    ax.set_thetagrids(angle_positions, angle_labels)
    
    # 添加年代圆圈标记
    decade_colors = plt.cm.Set3(np.linspace(0, 1, 8))
    decade_labels = []
    decade_radii = []
    for decade_num in range(8):  # 1950s到2020s
        decade_year = 1950 + decade_num * 10
        radius = decade_num + 1
        if radius <= max_radius:
            circle = Circle((0, 0), radius, fill=False, linestyle='--', 
                           alpha=0.3, color=decade_colors[decade_num])
            ax.add_patch(circle)
            decade_labels.append(f'{decade_year}s')
            decade_radii.append(radius)
    
    # 设置半径标签
    if decade_radii:
        ax.set_rgrids(decade_radii, decade_labels)
    
    # 初始化绘图元素
    line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.7, label='海平面连线')
    points = ax.scatter([], [], c=[], s=60, cmap='viridis', alpha=0.8, 
                       edgecolors='white', linewidth=1)
    
    # 年份标签列表
    year_texts = []
    
    # 添加起始点标记
    start_point, = ax.plot([], [], 'ro', markersize=10, label=f'起点 ({years[0]}年)')
    current_point, = ax.plot([], [], 'go', markersize=10, label='当前点')
    
    # 添加信息文本
    info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12,
                       verticalalignment='top', bbox=dict(boxstyle='round', 
                       facecolor='wheat', alpha=0.8))
    
    ax.legend(loc='upper left', bbox_to_anchor=(1.15, 1))
    
    def animate(frame):
        """动画函数"""
        if frame == 0:
            # 第一帧，只显示起始点
            start_point.set_data([angles[0]], [radii[0]])
            current_point.set_data([], [])
            line.set_data([], [])
            points.set_offsets(np.empty((0, 2)))
            
            # 清除之前的年份标签
            for text in year_texts:
                text.remove()
            year_texts.clear()
            
            info_text.set_text(f'起始年份: {years[0]}\n海平面: {sea_levels[0]:.3f}m\n年代: {int(years[0]//10)*10}s\n数据点: 1/{len(years)}')
            
        else:
            # 显示从第一个点到当前点的连线
            current_idx = min(frame, len(years) - 1)
            
            # 更新连线
            line_angles = angles[:current_idx + 1]
            line_radii = radii[:current_idx + 1]
            line.set_data(line_angles, line_radii)
            
            # 更新所有已显示的点
            if current_idx >= 0:
                # 创建颜色映射（基于年代）
                colors = []
                for i in range(current_idx + 1):
                    decade = int(years[i] // 10) - 195
                    colors.append(decade / 7)  # 归一化到0-1
                
                offsets = np.column_stack([line_angles, line_radii])
                points.set_offsets(offsets)
                points.set_array(np.array(colors))
            
            # 清除之前的年份标签
            for text in year_texts:
                text.remove()
            year_texts.clear()
            
            # 添加年份标签到每个点旁边
            for i in range(current_idx + 1):
                # 计算标签位置（稍微偏移避免重叠）
                label_angle = angles[i]
                label_radius = radii[i] + 0.15
                
                # 转换为笛卡尔坐标来放置文本
                x = label_radius * np.cos(label_angle - np.pi/2)
                y = label_radius * np.sin(label_angle - np.pi/2)
                
                # 只显示每5年的标签，避免太拥挤
                if i == 0 or i == current_idx or years[i] % 5 == 0:
                    text = ax.text(label_angle, label_radius, f'{years[i]}', 
                                 ha='center', va='center', fontsize=8, 
                                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))
                    year_texts.append(text)
            
            # 更新当前点
            current_point.set_data([angles[current_idx]], [radii[current_idx]])
            
            # 更新起始点
            start_point.set_data([angles[0]], [radii[0]])
            
            # 更新信息文本
            current_year = years[current_idx]
            current_level = sea_levels[current_idx]
            current_decade = int(current_year // 10) * 10
            year_in_decade = current_year % 10
            progress = (current_idx + 1) / len(years) * 100
            
            info_text.set_text(
                f'当前年份: {current_year}\n'
                f'年代: {current_decade}s (第{year_in_decade}年)\n'
                f'海平面: {current_level:.3f}m\n'
                f'数据点: {current_idx + 1}/{len(years)}\n'
                f'进度: {progress:.1f}%'
            )
        
        return [line, points, start_point, current_point, info_text] + year_texts
    
    # 创建动画
    # 总帧数 = 数据点数 + 停顿帧
    total_frames = len(years) + 60  # 末尾停顿60帧
    
    anim = animation.FuncAnimation(
        fig, animate, frames=total_frames, interval=300,  # 每帧300ms，稍慢一些看清年份
        blit=False, repeat=True
    )
    
    print(f"\n动画信息:")
    print(f"数据范围: {years[0]}-{years[-1]} ({len(years)}年)")
    print(f"海平面范围: {sea_levels.min():.3f}-{sea_levels.max():.3f}米")
    print(f"总帧数: {total_frames}")
    print(f"每帧时长: 300ms")
    print(f"显示逻辑: 10年一个轮回，角度=年代内位置，半径=年代+海平面")
    print(f"年份标签: 每5年显示一次 + 起点和终点")
    
    plt.show()

if __name__ == "__main__":
    print("创建海平面动画...")
    print("动画效果：10年一个轮回，角度=年代内年份，半径=年代+海平面")
    print("年份标签：显示在每个点旁边")
    create_animated_polar_chart()