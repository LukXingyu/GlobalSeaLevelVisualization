# Hong Kong Sea Level Visualization

An interactive data visualization project that crawls and analyzes sea level data from the Hong Kong Observatory (HKO) Quarry Bay station, featuring an innovative animated polar chart with 10-year cycle patterns.

## 🌊 Data Source
- **Station**: Hong Kong Observatory Quarry Bay (QUB) Station
- **Period**: 1954-2024 (71 years of continuous data)
- **Source**: HKO XML Data Interface
- **Data Range**: 1.280m - 1.510m mean sea level

## 🎯 Key Features

### 📊 Animated Polar Visualization
- **10-Year Cycles**: Data organized in decade-based angular patterns
- **Intuitive Mapping**: Angle = year position within decade, Radius = sea level height
- **Real-time Animation**: Progressive data connection from 1954 to 2024
- **Year Labels**: Smart labeling system showing key years
- **Color Coding**: Time-based gradient visualization

### 📈 Traditional Analysis
- Comprehensive statistical analysis
- Trend analysis with regression lines
- Decade-by-decade comparisons
- Data quality reports

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Animation (Recommended)
```bash
python animated_sea_level.py
```

This creates an animated polar chart showing:
- **71 years of data** progressively connecting from start to end
- **10-year cycle patterns** with intuitive angle/radius mapping
- **Real-time information** displaying current year, sea level, and progress
- **Interactive visualization** with pause and replay functionality

### Alternative Analysis
```bash
python visualize_sea_level_english.py  # Traditional charts
python crawl_hko_sea_level.py          # Re-crawl latest data
```

## 📁 Project Structure

```
GlobalSeaLevelVisualization/
├── animated_sea_level.py              # Main animated visualization
├── crawl_hko_sea_level.py             # Data crawler
├── visualize_sea_level_english.py     # Traditional analysis
├── requirements.txt                   # Dependencies
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── HKO_QUB_SeaLevel_Data_*.csv        # Complete dataset
├── HKO_QUB_MeanSeaLevel_Simple_*.csv  # Simplified dataset
└── HKO_QUB_SeaLevel_Metadata_*.json   # Data metadata
```

## 🎨 Visualization Design

### Polar Chart Innovation
The animated polar chart uses a unique **10-year cycle approach**:

- **Angular Position**: Each year's position within its decade (0°-360°)
  - Year 0 → 0°, Year 1 → 36°, Year 2 → 72°, ..., Year 9 → 324°
- **Radial Position**: Direct sea level height (scaled 1-5 for visibility)
  - 1.28m → radius 1.0, 1.51m → radius 5.0
- **Color Progression**: Time-based gradient from blue to yellow
- **Connection Pattern**: Progressive line drawing from 1954 to 2024

### Advantages
1. **Pattern Recognition**: Easily spot recurring patterns within decades
2. **Trend Visualization**: Long-term sea level rise clearly visible
3. **Comparative Analysis**: Same decade positions across different eras
4. **Intuitive Understanding**: Direct radius-to-height mapping

## 📊 Data Insights

### Key Statistics
- **Total Duration**: 71 years (1954-2024)
- **Data Coverage**: Complete annual records
- **Sea Level Range**: 230mm variation over 71 years
- **Trend**: Overall rising trend with decade-scale variations
- **Data Quality**: High-quality HKO official measurements

### Observable Patterns
- Long-term sea level rise trend
- Decade-scale cyclical variations
- Year-to-year fluctuations within decades
- Correlation with climate patterns

## 🛠️ Technical Details

### Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Visualization and animation
- **requests**: HTTP data fetching
- **beautifulsoup4**: XML/HTML parsing

### Data Processing
1. **Web Scraping**: Automated HKO XML endpoint discovery
2. **Data Cleaning**: Missing value handling and validation
3. **Normalization**: Scaling for optimal visualization
4. **Time Series**: Chronological data organization

### Animation Features
- **Frame Control**: 300ms per frame for clear viewing
- **Smart Labeling**: Every 5 years + start/end points
- **Progress Tracking**: Real-time progress and statistics
- **Responsive Design**: Adaptive layout and sizing

## 🔄 Data Updates

To fetch the latest data:
```bash
python crawl_hko_sea_level.py
```

The crawler automatically:
- Discovers current HKO data endpoints
- Parses XML response format
- Validates data integrity
- Updates CSV files with new records
- Generates metadata reports

## 📈 Future Enhancements

- [ ] Interactive web dashboard
- [ ] Multiple station comparisons
- [ ] Climate correlation analysis
- [ ] Prediction modeling
- [ ] Export capabilities (GIF, MP4)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hong Kong Observatory**: For providing comprehensive sea level data
- **Scientific Community**: For open data sharing principles
- **Matplotlib Community**: For excellent visualization tools

## 📧 Contact

**Project**: [GlobalSeaLevelVisualization](https://github.com/LukXingyu/GlobalSeaLevelVisualization)  
**Author**: LukXingyu  
**Data Source**: Hong Kong Observatory

---

*Visualizing 71 years of Hong Kong sea level changes through innovative polar animation*