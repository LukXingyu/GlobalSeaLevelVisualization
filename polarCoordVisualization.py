import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle

# Set font for better display
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_sea_level_data():
    """Load sea level data"""
    try:
        df = pd.read_csv('HKO_QUB_SeaLevel_Data_20250918_163225.csv')
        df = df.dropna(subset=['Mean_Sea_Level_m'])
        return df
    except FileNotFoundError:
        print("Data file not found!")
        return None

def create_animated_polar_chart():
    """Create animated polar chart"""
    df = load_sea_level_data()
    if df is None:
        return
    
    years = df['Year'].values
    sea_levels = df['Mean_Sea_Level_m'].values
    
    # Calculate angles based on 10-year cycles
    # Each year's angle within its decade (0 to 2π)
    angles = []
    radii = []
    
    for year, level in zip(years, sea_levels):
        year_in_decade = year % 10  # Position within decade (0-9)
        angle = (year_in_decade / 10) * 2 * np.pi
        angles.append(angle)
        
        # Radius = direct sea level height (scaled for better visibility)
        # Scale from 1.28-1.51m to radius 1-5 for better visualization
        min_level, max_level = sea_levels.min(), sea_levels.max()
        radius = 1 + ((level - min_level) / (max_level - min_level)) * 4
        radii.append(radius)
    
    angles = np.array(angles)
    radii = np.array(radii)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(projection='polar'))
    
    # Set polar chart style
    ax.set_ylim(0, 6)
    ax.set_title('Hong Kong Sea Level Animation (10-Year Cycles)\nAngle=Year in Decade, Radius=Sea Level Height', 
                 fontsize=16, pad=30)
    
    # Set angle labels (years within decade: Year 0, Year 1...Year 9)
    angle_labels = [f'Year {i}' for i in range(10)]
    angle_positions = [(i / 10) * 360 for i in range(10)]
    ax.set_thetagrids(angle_positions, angle_labels)
    
    # Add radius labels for sea level heights
    min_level, max_level = sea_levels.min(), sea_levels.max()
    radius_ticks = [1, 2, 3, 4, 5]
    radius_labels = []
    for r in radius_ticks:
        # Convert radius back to actual sea level
        actual_level = min_level + ((r - 1) / 4) * (max_level - min_level)
        radius_labels.append(f'{actual_level:.2f}m')
    
    ax.set_rgrids(radius_ticks, radius_labels)
    
    # Initialize plot elements
    line, = ax.plot([], [], 'b-', linewidth=2, alpha=0.7, label='Sea Level Connections')
    points = ax.scatter([], [], c=[], s=60, cmap='viridis', alpha=0.8, 
                       edgecolors='white', linewidth=1)
    
    # Year label list
    year_texts = []
    
    # Add start and current point markers
    start_point, = ax.plot([], [], 'ro', markersize=10, label=f'Start ({years[0]})')
    current_point, = ax.plot([], [], 'go', markersize=10, label='Current Point')
    
    # Add info text
    info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12,
                       verticalalignment='top', bbox=dict(boxstyle='round', 
                       facecolor='wheat', alpha=0.8))
    
    ax.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
    
    def animate(frame):
        """Animation function"""
        if frame == 0:
            # First frame, only show starting point
            start_point.set_data([angles[0]], [radii[0]])
            current_point.set_data([], [])
            line.set_data([], [])
            points.set_offsets(np.empty((0, 2)))
            
            # Clear previous year labels
            for text in year_texts:
                text.remove()
            year_texts.clear()
            
            info_text.set_text(f'Start Year: {years[0]}\nSea Level: {sea_levels[0]:.3f}m\nDecade: {int(years[0]//10)*10}s\nData Points: 1/{len(years)}')
            
        else:
            # Show connections from first point to current point
            current_idx = min(frame, len(years) - 1)
            
            # Update connections
            line_angles = angles[:current_idx + 1]
            line_radii = radii[:current_idx + 1]
            line.set_data(line_angles, line_radii)
            
            # Update all displayed points
            if current_idx >= 0:
                # Create color mapping (based on time progression)
                colors = []
                for i in range(current_idx + 1):
                    # Color based on year progression (0 to 1)
                    color_val = (years[i] - years[0]) / (years[-1] - years[0])
                    colors.append(color_val)
                
                offsets = np.column_stack([line_angles, line_radii])
                points.set_offsets(offsets)
                points.set_array(np.array(colors))
            
            # Clear previous year labels
            for text in year_texts:
                text.remove()
            year_texts.clear()
            
            # Add year labels next to each point
            for i in range(current_idx + 1):
                # Calculate label position (slightly offset to avoid overlap)
                label_angle = angles[i]
                label_radius = radii[i] + 0.15
                
                # Convert to Cartesian coordinates for text placement
                x = label_radius * np.cos(label_angle - np.pi/2)
                y = label_radius * np.sin(label_angle - np.pi/2)
                
                # Only show labels every 5 years to avoid crowding
                if i == 0 or i == current_idx or years[i] % 5 == 0:
                    text = ax.text(label_angle, label_radius, f'{years[i]}', 
                                 ha='center', va='center', fontsize=8, 
                                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))
                    year_texts.append(text)
            
            # Update current point
            current_point.set_data([angles[current_idx]], [radii[current_idx]])
            
            # Update start point
            start_point.set_data([angles[0]], [radii[0]])
            
            # Update info text
            current_year = years[current_idx]
            current_level = sea_levels[current_idx]
            current_decade = int(current_year // 10) * 10
            year_in_decade = current_year % 10
            progress = (current_idx + 1) / len(years) * 100
            
            info_text.set_text(
                f'Current Year: {current_year}\n'
                f'Decade: {current_decade}s (Year {year_in_decade})\n'
                f'Sea Level: {current_level:.3f}m\n'
                f'Radius: {radii[current_idx]:.2f}\n'
                f'Data Points: {current_idx + 1}/{len(years)}\n'
                f'Progress: {progress:.1f}%'
            )
        
        return [line, points, start_point, current_point, info_text] + year_texts
    
    # Create animation
    # Total frames = data points + pause frames
    total_frames = len(years) + 60  # End pause 60 frames
    
    anim = animation.FuncAnimation(
        fig, animate, frames=total_frames, interval=300,  # 300ms per frame, slower to see years clearly
        blit=False, repeat=True
    )
    
    print(f"\nAnimation Info:")
    print(f"Data Range: {years[0]}-{years[-1]} ({len(years)} years)")
    print(f"Sea Level Range: {sea_levels.min():.3f}-{sea_levels.max():.3f}m")
    print(f"Total Frames: {total_frames}")
    print(f"Frame Duration: 300ms")
    print(f"Display Logic: 10-year cycles, angle=position in decade, radius=sea level height")
    print(f"Radius Range: 1.00-5.00 (scaled from {sea_levels.min():.3f}-{sea_levels.max():.3f}m)")
    print(f"Year Labels: Every 5 years + start and end points")
    
    plt.show()

if __name__ == "__main__":
    print("Creating sea level animation...")
    print("Animation effect: 10-year cycles, angle=year in decade, radius=sea level height")
    print("Year labels: Displayed next to each point")
    create_animated_polar_chart()