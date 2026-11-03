# Week 3 Task: Advanced Data Analysis and Visualization in Logistics

This repository contains the complete empirical research study, data generation pipeline, exploratory data analysis (EDA), publication-grade statistical visualizations, and executive documentation for multimodal freight performance analysis.

---

## 📁 Repository Structure

```text
.
├── Week3_Logistics_Analysis_Report.docx      # Primary comprehensive Microsoft Word report
├── Week3_Logistics_Analysis_Report.doc       # Legacy-compatible Word document
├── README.md                                # Project overview and reproduction guide
│
├── data/
│   └── hypothetical_logistics_data.csv       # Simulated multimodal freight dataset (2,500 shipments, 16 features)
│
├── scripts/
│   └── logistics_analysis_visualization.py   # Complete Python analysis and visualization pipeline
│
└── visualizations/                          # High-resolution (200 DPI) generated figures
    ├── 1_delivery_time_distribution.png      # Delivery time histogram & modal delay boxplots
    ├── 2_cost_drivers_weight_distance.png    # Multivariate cost drivers (Weight, Distance, Mode)
    ├── 3_monthly_volume_seasonality.png      # Dual-axis monthly volume & freight expenditure trend
    ├── 4_correlation_matrix_heatmap.png      # Upper-triangular Pearson correlation heatmap
    ├── 5_carrier_leadtime_and_delay_analysis.png # Carrier SLA adherence & delay distribution violin plots
    └── 6_fleet_efficiency_cost_per_ton_km.png# Modal economic efficiency ($ / ton-km)
```

---

## 🎯 Project Objectives & Methodology

1. **Multimodal Logistics Simulation**:
   - Synthetic dataset of 2,500 domestic and cross-border shipments spanning calendar year 2024.
   - Multimodal coverage: Road (FTL), Road (LTL), Rail Freight, Air Cargo, and Maritime Shipping.
   - 16 realistic logistics features capturing distances, weights, lead times, delays, cross-dock dwell hours, base freight costs, fuel surcharges, and unit economics.

2. **Exploratory Data Analysis (EDA)**:
   - Central tendency (Mean, Median) and dispersion metrics (Std Dev, IQR).
   - Skewness and Kurtosis analysis identifying positive skew in freight spend and right-tailed delay distributions.
   - Pearson correlation analysis demonstrating key dependencies (e.g. Weight vs. Cost $r = 0.74$, Warehouse dwell time vs. Delivery delays $r = 0.38$).

3. **Statistical Visualizations (Seaborn & Matplotlib)**:
   - **Lead Time Dynamics**: Bimodal transit density contrasting rapid Road movements against long-haul Maritime schedules.
   - **Cost Structures**: Multi-attribute scatter plot proving steep Air Cargo premiums and bulk Rail/FTL economies of scale.
   - **Seasonality**: Dual-axis chart highlighting Q3 and Q4 peak-season demand surges and cost acceleration.
   - **Carrier Benchmarking**: Comparative SLA compliance revealing top performers (Apex Freight: 94.2% on-time) vs. severe operational bottlenecks (NationalExpress: 47.9% delayed).
   - **Unit Economic Benchmarking**: Cost per ton-km across modes ($0.04/ton-km Maritime vs. $4.20/ton-km Air Cargo).

---

## 🚀 How to Run the Analysis

### 1. Prerequisites
Ensure Python 3.10+ is installed along with the required libraries:
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 2. Execution
Run the end-to-end data generation, EDA calculations, and figure rendering:
```bash
python scripts/logistics_analysis_visualization.py
```
Generated plots will be saved directly into `visualizations/` and summary statistics will be logged to the console.

---

## 📄 Final Deliverable Document
For the complete, formatted report with embedded charts, styled tables, code documentation, and strategic recommendations, open:
* **`Week3_Logistics_Analysis_Report.docx`**
