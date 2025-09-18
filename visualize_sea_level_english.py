import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import glob
import os

# Set style
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

def load_latest_data():
    """Load the latest sea level data"""
    # Find the latest CSV file
    csv_files = glob.glob("HKO_QUB_SeaLevel_Data_*.csv")
    if not csv_files:
        print("No data files found. Please run crawl_hko_sea_level.py first")
        return None
    
    latest_file = max(csv_files, key=os.path.getctime)
    print(f"Loading data file: {latest_file}")
    
    df = pd.read_csv(latest_file)
    return df

def create_comprehensive_analysis(df):
    """Create comprehensive sea level analysis"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Hong Kong Quarry Bay Station Sea Level Analysis (1954-2024)', 
                 fontsize=16, fontweight='bold')
    
    # 1. Long-term sea level trend
    ax1 = axes[0, 0]
    years = df['Year']
    sea_level = df['Mean_Sea_Level_m']
    
    ax1.plot(years, sea_level, 'b-', linewidth=2, alpha=0.7, label='Annual Mean Sea Level')
    
    # Add trend line
    z = np.polyfit(years, sea_level, 1)
    p = np.poly1d(z)
    ax1.plot(years, p(years), 'r--', linewidth=2, alpha=0.8, 
             label=f'Trend: {z[0]*10:.2f} cm/decade')
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Sea Level Height (m)')
    ax1.set_title('Long-term Sea Level Change')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Recent 30-year trend
    ax2 = axes[0, 1]
    recent_df = df[df['Year'] >= 1995].copy()
    
    if len(recent_df) > 0:
        ax2.plot(recent_df['Year'], recent_df['Mean_Sea_Level_m'], 'g-', 
                linewidth=3, marker='o', markersize=4, label='Recent 30 years')
        
        # Recent trend line
        z_recent = np.polyfit(recent_df['Year'], recent_df['Mean_Sea_Level_m'], 1)
        p_recent = np.poly1d(z_recent)
        ax2.plot(recent_df['Year'], p_recent(recent_df['Year']), 'r--', 
                linewidth=2, label=f'Recent trend: {z_recent[0]*10:.2f} cm/decade')
        
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Sea Level Height (m)')
        ax2.set_title('Recent 30-year Changes')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    # 3. Year-to-year changes
    ax3 = axes[0, 2]
    sea_level_change = sea_level.diff()
    
    colors = ['red' if x < 0 else 'blue' for x in sea_level_change]
    ax3.bar(years[1:], sea_level_change[1:], color=colors, alpha=0.6, width=0.8)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Annual Change (m)')
    ax3.set_title('Year-to-Year Changes (Blue=Rise, Red=Drop)')
    ax3.grid(True, alpha=0.3)
    
    # 4. Tidal range analysis (for years with complete data)
    ax4 = axes[1, 0]
    complete_data = df.dropna(subset=['Mean_Higher_High_Water_m', 'Mean_Lower_Low_Water_m'])
    
    if len(complete_data) > 0:
        tidal_range = complete_data['Mean_Higher_High_Water_m'] - complete_data['Mean_Lower_Low_Water_m']
        
        ax4.plot(complete_data['Year'], tidal_range, 'purple', linewidth=2, 
                marker='o', markersize=3, label='Tidal Range')
        
        # Tidal range trend
        z_range = np.polyfit(complete_data['Year'], tidal_range, 1)
        p_range = np.poly1d(z_range)
        ax4.plot(complete_data['Year'], p_range(complete_data['Year']), 'r--', 
                linewidth=2, alpha=0.8, label=f'Trend: {z_range[0]*10:.3f} m/decade')
        
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Tidal Range (m)')
        ax4.set_title('Tidal Range Changes')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    # 5. Decadal analysis
    ax5 = axes[1, 1]
    
    # Group by decades
    df['Decade'] = (df['Year'] // 10) * 10
    decade_stats = df.groupby('Decade')['Mean_Sea_Level_m'].agg(['mean', 'std', 'count']).reset_index()
    decade_stats = decade_stats[decade_stats['count'] >= 5]  # Only decades with 5+ years
    
    ax5.bar(decade_stats['Decade'], decade_stats['mean'], 
           yerr=decade_stats['std'], capsize=5, alpha=0.7, color='skyblue')
    ax5.set_xlabel('Decade')
    ax5.set_ylabel('Mean Sea Level (m)')
    ax5.set_title('Decadal Averages')
    ax5.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Statistics summary
    ax6 = axes[1, 2]
    
    # Calculate statistics
    stats_text = f"""Data Summary Statistics:

Time Period: {df['Year'].min()}-{df['Year'].max()} ({len(df)} years)

Mean Sea Level:
• Average: {sea_level.mean():.3f} m
• Std Dev: {sea_level.std():.3f} m
• Maximum: {sea_level.max():.3f} m ({df.loc[sea_level.idxmax(), 'Year']:.0f})
• Minimum: {sea_level.min():.3f} m ({df.loc[sea_level.idxmin(), 'Year']:.0f})

Long-term Trend:
• Total change: {z[0]*71:.2f} cm (71 years)
• Rate: {z[0]*10:.2f} cm/decade

Recent Changes:
• 2020: {df[df['Year']==2020]['Mean_Sea_Level_m'].iloc[0]:.3f} m
• 2024: {df[df['Year']==2024]['Mean_Sea_Level_m'].iloc[0]:.3f} m
• 4-year change: {(df[df['Year']==2024]['Mean_Sea_Level_m'].iloc[0] - df[df['Year']==2020]['Mean_Sea_Level_m'].iloc[0])*100:.1f} cm

Data Quality:
• Complete tide data: {len(complete_data)} years
• Data coverage: {len(df)/71*100:.1f}%
    """
    
    ax6.text(0.05, 0.95, stats_text, transform=ax6.transAxes, fontsize=9,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax6.set_xlim(0, 1)
    ax6.set_ylim(0, 1)
    ax6.axis('off')
    ax6.set_title('Statistical Summary')
    
    plt.tight_layout()
    return fig

def create_tide_components_analysis(df):
    """Create detailed tidal components analysis"""
    # Filter data with complete tidal measurements
    complete_data = df.dropna(subset=['Mean_Higher_High_Water_m', 'Mean_Lower_Low_Water_m'])
    
    if len(complete_data) == 0:
        print("No complete tidal data available")
        return None
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Hong Kong Quarry Bay Station - Detailed Tidal Analysis', 
                 fontsize=16, fontweight='bold')
    
    # 1. All tidal components over time
    ax1 = axes[0, 0]
    
    ax1.plot(complete_data['Year'], complete_data['Mean_Higher_High_Water_m'], 
             'r-', linewidth=2, label='Mean Higher High Water', alpha=0.8)
    ax1.plot(complete_data['Year'], complete_data['Mean_Lower_High_Water_m'], 
             'orange', linewidth=1.5, label='Mean Lower High Water', alpha=0.8)
    ax1.plot(complete_data['Year'], complete_data['Mean_Sea_Level_m'], 
             'b-', linewidth=2, label='Mean Sea Level', marker='o', markersize=2)
    ax1.plot(complete_data['Year'], complete_data['Mean_Higher_Low_Water_m'], 
             'lightgreen', linewidth=1.5, label='Mean Higher Low Water', alpha=0.8)
    ax1.plot(complete_data['Year'], complete_data['Mean_Lower_Low_Water_m'], 
             'g-', linewidth=2, label='Mean Lower Low Water', alpha=0.8)
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Water Level (m)')
    ax1.set_title('Tidal Components Long-term Changes')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. Tidal range and asymmetry
    ax2 = axes[0, 1]
    
    tidal_range = complete_data['Mean_Higher_High_Water_m'] - complete_data['Mean_Lower_Low_Water_m']
    high_water_range = complete_data['Mean_Higher_High_Water_m'] - complete_data['Mean_Lower_High_Water_m']
    low_water_range = complete_data['Mean_Higher_Low_Water_m'] - complete_data['Mean_Lower_Low_Water_m']
    
    ax2.plot(complete_data['Year'], tidal_range, 'purple', linewidth=2, 
             marker='o', markersize=3, label='Total Tidal Range')
    ax2.plot(complete_data['Year'], high_water_range, 'red', linewidth=1.5, 
             alpha=0.7, label='High Water Range')
    ax2.plot(complete_data['Year'], low_water_range, 'blue', linewidth=1.5, 
             alpha=0.7, label='Low Water Range')
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Range (m)')
    ax2.set_title('Tidal Range Components')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Distribution of tidal levels
    ax3 = axes[1, 0]
    
    tide_data = [
        complete_data['Mean_Higher_High_Water_m'],
        complete_data['Mean_Lower_High_Water_m'], 
        complete_data['Mean_Sea_Level_m'],
        complete_data['Mean_Higher_Low_Water_m'],
        complete_data['Mean_Lower_Low_Water_m']
    ]
    
    labels = ['MHHW', 'MLHW', 'MSL', 'MHLW', 'MLLW']
    colors = ['red', 'orange', 'blue', 'lightgreen', 'green']
    
    bp = ax3.boxplot(tide_data, tick_labels=labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    ax3.set_ylabel('Water Level (m)')
    ax3.set_title('Distribution of Tidal Levels')
    ax3.grid(True, alpha=0.3)
    
    # 4. Correlation matrix
    ax4 = axes[1, 1]
    
    # Select numeric columns for correlation
    corr_data = complete_data[['Mean_Sea_Level_m', 'Mean_Higher_High_Water_m', 
                              'Mean_Lower_High_Water_m', 'Mean_Higher_Low_Water_m', 
                              'Mean_Lower_Low_Water_m']].corr()
    
    # Create heatmap
    im = ax4.imshow(corr_data.values, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    
    # Set ticks and labels
    ax4.set_xticks(range(len(corr_data.columns)))
    ax4.set_yticks(range(len(corr_data.columns)))
    ax4.set_xticklabels(['MSL', 'MHHW', 'MLHW', 'MHLW', 'MLLW'], rotation=45)
    ax4.set_yticklabels(['MSL', 'MHHW', 'MLHW', 'MHLW', 'MLLW'])
    
    # Add correlation values
    for i in range(len(corr_data.columns)):
        for j in range(len(corr_data.columns)):
            text = ax4.text(j, i, f'{corr_data.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontsize=8)
    
    ax4.set_title('Tidal Components Correlation')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
    cbar.set_label('Correlation Coefficient')
    
    plt.tight_layout()
    return fig

def save_visualization(fig, filename_prefix):
    """Save visualization charts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Chart saved: {filename}")
    return filename

def generate_summary_report(df):
    """Generate a text summary report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"HKO_SeaLevel_Analysis_Report_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("Hong Kong Observatory - Quarry Bay Station Sea Level Analysis Report\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Data Period: {df['Year'].min()}-{df['Year'].max()} ({len(df)} years)\n")
        f.write(f"Station: Quarry Bay (QUB)\n\n")
        
        # Basic statistics
        sea_level = df['Mean_Sea_Level_m']
        f.write("BASIC STATISTICS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Mean Sea Level Average: {sea_level.mean():.3f} m\n")
        f.write(f"Standard Deviation: {sea_level.std():.3f} m\n")
        f.write(f"Maximum: {sea_level.max():.3f} m (Year: {df.loc[sea_level.idxmax(), 'Year']:.0f})\n")
        f.write(f"Minimum: {sea_level.min():.3f} m (Year: {df.loc[sea_level.idxmin(), 'Year']:.0f})\n")
        f.write(f"Range: {sea_level.max() - sea_level.min():.3f} m\n\n")
        
        # Trend analysis
        years = df['Year']
        z = np.polyfit(years, sea_level, 1)
        f.write("TREND ANALYSIS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Linear trend slope: {z[0]:.6f} m/year\n")
        f.write(f"Rate of change: {z[0]*10:.2f} cm/decade\n")
        f.write(f"Total change over {len(df)} years: {z[0]*len(df):.2f} cm\n\n")
        
        # Recent changes
        f.write("RECENT CHANGES (2020-2024)\n")
        f.write("-" * 30 + "\n")
        recent_data = df[df['Year'] >= 2020]
        for _, row in recent_data.iterrows():
            f.write(f"{row['Year']:.0f}: {row['Mean_Sea_Level_m']:.3f} m\n")
        
        if len(recent_data) >= 2:
            change_2020_2024 = recent_data.iloc[-1]['Mean_Sea_Level_m'] - recent_data.iloc[0]['Mean_Sea_Level_m']
            f.write(f"\nChange 2020-2024: {change_2020_2024*100:.1f} cm\n")
        
        f.write("\n")
        
        # Decadal analysis
        df_copy = df.copy()
        df_copy['Decade'] = (df_copy['Year'] // 10) * 10
        decade_stats = df_copy.groupby('Decade')['Mean_Sea_Level_m'].agg(['mean', 'std', 'count'])
        
        f.write("DECADAL AVERAGES\n")
        f.write("-" * 20 + "\n")
        for decade, stats in decade_stats.iterrows():
            if stats['count'] >= 5:
                f.write(f"{decade:.0f}s: {stats['mean']:.3f} ± {stats['std']:.3f} m ({stats['count']:.0f} years)\n")
        
        f.write("\n")
        
        # Data quality
        complete_data = df.dropna(subset=['Mean_Higher_High_Water_m', 'Mean_Lower_Low_Water_m'])
        f.write("DATA QUALITY\n")
        f.write("-" * 15 + "\n")
        f.write(f"Total records: {len(df)}\n")
        f.write(f"Complete tidal data: {len(complete_data)} years\n")
        f.write(f"Data completeness: {len(df)/71*100:.1f}%\n")
        f.write(f"Missing years: {71 - len(df)}\n\n")
        
        f.write("Note: Tidal information from 1954 to 1985 are based on North Point tide gauge data.\n")
        f.write("Mean Sea Levels are computed directly from on-site measurement data without\n")
        f.write("any post data corrections including land settlement.\n")
    
    print(f"✓ Summary report saved: {report_filename}")
    return report_filename

def main():
    """Main function"""
    print("Hong Kong Sea Level Data Visualization and Analysis")
    print("=" * 60)
    
    # Load data
    df = load_latest_data()
    if df is None:
        return
    
    print(f"✓ Successfully loaded {len(df)} years of data ({df['Year'].min()}-{df['Year'].max()})")
    
    # Create comprehensive analysis
    print("\nGenerating comprehensive sea level analysis charts...")
    fig1 = create_comprehensive_analysis(df)
    filename1 = save_visualization(fig1, "HKO_Comprehensive_SeaLevel_Analysis")
    
    # Create detailed tidal analysis
    print("\nGenerating detailed tidal components analysis...")
    fig2 = create_tide_components_analysis(df)
    if fig2:
        filename2 = save_visualization(fig2, "HKO_Detailed_Tidal_Analysis")
    
    # Generate summary report
    print("\nGenerating summary report...")
    report_file = generate_summary_report(df)
    
    # Show charts
    print("\nDisplaying charts...")
    plt.show()
    
    print("\n" + "=" * 60)
    print("✓ Analysis completed successfully!")
    print("\nGenerated files:")
    print(f"1. {filename1}")
    if fig2:
        print(f"2. {filename2}")
    print(f"3. {report_file}")
    
    print(f"\nKey findings:")
    sea_level = df['Mean_Sea_Level_m']
    years = df['Year']
    z = np.polyfit(years, sea_level, 1)
    print(f"• Sea level rising at {z[0]*10:.2f} cm per decade")
    print(f"• Total rise over 71 years: {z[0]*71:.1f} cm")
    print(f"• Current level (2024): {df[df['Year']==2024]['Mean_Sea_Level_m'].iloc[0]:.3f} m")
    print(f"• Data coverage: {len(df)} years from {df['Year'].min()}-{df['Year'].max()}")

if __name__ == "__main__":
    main()