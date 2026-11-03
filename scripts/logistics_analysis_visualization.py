"""
Week 3: Advanced Data Analysis and Visualization in Logistics
============================================================
Script: logistics_analysis_visualization.py
Author: Antigravity AI & Senior Logistics Analytics Engineer
Description:
    This script performs end-to-end Exploratory Data Analysis (EDA)
    and visualization on a hypothetical logistics dataset consisting of
    2,500 multimodal shipments.

Modules Used:
    - pandas: Data manipulation, grouping, aggregations
    - numpy: Numerical operations and vector calculations
    - matplotlib.pyplot: Base plotting and multi-axis configurations
    - seaborn: Statistical data visualizations and thematic styling
    - scipy.stats: Skewness, kurtosis, and correlation inference
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional aesthetics for publication-grade logistics charts
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 15,
    'figure.dpi': 200
})

def main():
    # Base paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "data")
    vis_dir = os.path.join(project_dir, "visualizations")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "hypothetical_logistics_data.csv")

    # 1. LOAD OR SIMULATE DATASET
    if os.path.exists(csv_path):
        print(f"Loading existing dataset from {csv_path}...")
        df = pd.read_csv(csv_path, parse_dates=["Shipment_Date"])
    else:
        print("Generating 2,500 synthetic multimodal shipment records...")
        np.random.seed(42)
        n_samples = 2500

        dates = pd.date_range(start="2024-01-01", end="2024-12-31", periods=n_samples)
        origins = ["Chicago Hub", "Atlanta Gateway", "Dallas Distribution", "Los Angeles Port", "New York Terminal"]
        destinations = ["Seattle Depot", "Denver Hub", "Miami Gateway", "Boston Center", "Houston Terminal"]
        modes = ["Road (FTL)", "Road (LTL)", "Rail Freight", "Air Cargo", "Maritime"]
        carriers = ["Apex Freight", "SwiftLogistics", "TransGlobal", "NationalExpress", "PacificMovers"]

        mode_props = [0.40, 0.25, 0.15, 0.10, 0.10]
        carrier_props = [0.30, 0.25, 0.20, 0.15, 0.10]

        assigned_modes = np.random.choice(modes, size=n_samples, p=mode_props)
        assigned_carriers = np.random.choice(carriers, size=n_samples, p=carrier_props)
        assigned_origins = np.random.choice(origins, size=n_samples)
        assigned_dest = np.random.choice(destinations, size=n_samples)

        distances = np.random.normal(loc=1200, scale=450, size=n_samples)
        distances = np.clip(distances, 200, 3500).round(1)

        weights = []
        for m in assigned_modes:
            if m == "Air Cargo":
                w = np.random.exponential(scale=600) + 50
            elif m == "Road (LTL)":
                w = np.random.normal(loc=2500, scale=800)
            elif m == "Road (FTL)":
                w = np.random.normal(loc=14000, scale=2500)
            elif m == "Rail Freight":
                w = np.random.normal(loc=24000, scale=4000)
            else:  # Maritime
                w = np.random.normal(loc=28000, scale=5000)
            weights.append(max(50, w))
        weights = np.array(weights).round(1)

        promised_lead_times = []
        for m, d in zip(assigned_modes, distances):
            if m == "Air Cargo":
                plt_val = 1 + int(d / 1500)
            elif m in ["Road (FTL)", "Road (LTL)"]:
                plt_val = 2 + int(d / 600)
            elif m == "Rail Freight":
                plt_val = 4 + int(d / 400)
            else:
                plt_val = 10 + int(d / 300)
            promised_lead_times.append(plt_val)
        promised_lead_times = np.array(promised_lead_times)

        delays = []
        delivery_times = []
        for carrier, m, plt_val in zip(assigned_carriers, assigned_modes, promised_lead_times):
            carrier_delay_bias = {
                "Apex Freight": -0.2, "SwiftLogistics": 0.1, 
                "TransGlobal": 0.6, "NationalExpress": 1.2, "PacificMovers": 0.3
            }[carrier]
            mode_volatility = {
                "Air Cargo": 0.4, "Road (FTL)": 0.8, 
                "Road (LTL)": 1.4, "Rail Freight": 1.8, "Maritime": 2.5
            }[m]
            disruption = np.random.exponential(scale=2.5) if np.random.rand() < 0.15 else 0.0
            delay = np.random.normal(loc=carrier_delay_bias, scale=mode_volatility) + disruption
            actual_time = max(0.5, plt_val + delay)
            delays.append(round(actual_time - plt_val, 2))
            delivery_times.append(round(actual_time, 2))

        delays = np.array(delays)
        delivery_times = np.array(delivery_times)

        costs = []
        fuel_surcharges = []
        for m, d, w in zip(assigned_modes, distances, weights):
            if m == "Air Cargo":
                base = 250; cost_dist = 0.85 * d; cost_weight = 2.10 * w; fuel_rate = 0.22
            elif m == "Road (FTL)":
                base = 400; cost_dist = 1.40 * d; cost_weight = 0.08 * w; fuel_rate = 0.15
            elif m == "Road (LTL)":
                base = 180; cost_dist = 1.10 * d; cost_weight = 0.25 * w; fuel_rate = 0.16
            elif m == "Rail Freight":
                base = 500; cost_dist = 0.65 * d; cost_weight = 0.04 * w; fuel_rate = 0.12
            else:
                base = 700; cost_dist = 0.45 * d; cost_weight = 0.03 * w; fuel_rate = 0.10
                
            raw_cost = base + cost_dist + cost_weight
            fuel = raw_cost * fuel_rate + np.random.normal(0, 20)
            total_cost = raw_cost + fuel + np.random.normal(0, 50)
            costs.append(round(max(150, total_cost), 2))
            fuel_surcharges.append(round(max(20, fuel), 2))

        warehouse_hrs = np.random.gamma(shape=3.0, scale=4.0, size=n_samples).round(1)
        on_time_status = ["On-Time" if d <= 0.2 else "Delayed" for d in delays]
        ton_km = (weights / 1000.0) * distances
        cost_per_ton_km = np.round(np.array(costs) / np.maximum(ton_km, 1.0), 3)

        df = pd.DataFrame({
            "Shipment_ID": [f"SHP-2024-{10000+i}" for i in range(n_samples)],
            "Shipment_Date": dates,
            "Origin_Hub": assigned_origins,
            "Destination_Hub": assigned_dest,
            "Transport_Mode": assigned_modes,
            "Carrier_Name": assigned_carriers,
            "Distance_km": distances,
            "Weight_kg": weights,
            "Promised_Lead_Time_days": promised_lead_times,
            "Delivery_Time_days": delivery_times,
            "Delay_days": delays,
            "Warehouse_Handling_hrs": warehouse_hrs,
            "Transportation_Cost_usd": costs,
            "Fuel_Surcharge_usd": fuel_surcharges,
            "Cost_per_Ton_km_usd": cost_per_ton_km,
            "Delivery_Status": on_time_status
        })
        df.to_csv(csv_path, index=False)
        print(f"Dataset saved to {csv_path}")

    # 2. STATISTICAL EXPLORATORY DATA ANALYSIS (EDA)
    print("\n--- Summary Statistics (Central Tendency & Dispersion) ---")
    num_cols = [
        "Distance_km", "Weight_kg", "Delivery_Time_days", "Delay_days", 
        "Warehouse_Handling_hrs", "Transportation_Cost_usd", 
        "Fuel_Surcharge_usd", "Cost_per_Ton_km_usd"
    ]
    summary_df = df[num_cols].describe().T
    summary_df["median"] = df[num_cols].median()
    summary_df["skewness"] = df[num_cols].skew()
    summary_df["kurtosis"] = df[num_cols].kurt()
    print(summary_df[["mean", "median", "std", "min", "50%", "max", "skewness", "kurtosis"]])

    corr = df[num_cols].corr()

    # 3. PRODUCTION VISUALIZATIONS

    # Visualization 1: Distribution of Delivery Times & Delays
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["Delivery_Time_days"], kde=True, color="#2b5c8f", ax=ax[0], bins=30)
    ax[0].axvline(df["Delivery_Time_days"].median(), color="red", linestyle="--", label=f"Median ({df['Delivery_Time_days'].median():.1f} d)")
    ax[0].axvline(df["Delivery_Time_days"].mean(), color="orange", linestyle="-", label=f"Mean ({df['Delivery_Time_days'].mean():.1f} d)")
    ax[0].set_title("Distribution of Delivery Times (Days)", fontweight="bold")
    ax[0].set_xlabel("Delivery Time (Days)")
    ax[0].set_ylabel("Shipment Count")
    ax[0].legend()

    sns.boxplot(x="Transport_Mode", y="Delay_days", data=df, hue="Transport_Mode", palette="Blues_r", legend=False, ax=ax[1])
    ax[1].axhline(0, color="gray", linestyle="--", alpha=0.7)
    ax[1].set_title("Delivery Delays by Transport Mode", fontweight="bold")
    ax[1].set_xlabel("Transport Mode")
    ax[1].set_ylabel("Delay (Days)")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "1_delivery_time_distribution.png"), dpi=200)
    plt.close()

    # Visualization 2: Cost Drivers (Weight, Distance, Transport Mode)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="Weight_kg",
        y="Transportation_Cost_usd",
        hue="Transport_Mode",
        size="Distance_km",
        sizes=(30, 220),
        alpha=0.75,
        palette="tab10",
        ax=ax
    )
    ax.set_title("Transportation Cost Drivers: Weight, Distance & Mode", fontweight="bold")
    ax.set_xlabel("Shipment Weight (kg)")
    ax.set_ylabel("Total Transportation Cost ($ USD)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "2_cost_drivers_weight_distance.png"), dpi=200)
    plt.close()

    # Visualization 3: Monthly Volume & Total Expenditure Seasonality
    df["YearMonth"] = df["Shipment_Date"].dt.to_period("M")
    monthly = df.groupby("YearMonth").agg(
        Shipment_Count=("Shipment_ID", "count"),
        Total_Cost=("Transportation_Cost_usd", "sum")
    ).reset_index()
    monthly["Month_Str"] = monthly["YearMonth"].astype(str)

    fig, ax1 = plt.subplots(figsize=(11, 5))
    color = '#1f77b4'
    ax1.set_xlabel("Month (2024)")
    ax1.set_ylabel("Shipment Volume (Count)", color=color, fontweight="bold")
    sns.barplot(data=monthly, x="Month_Str", y="Shipment_Count", color=color, alpha=0.6, ax=ax1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(range(len(monthly)))
    ax1.set_xticklabels(monthly["Month_Str"], rotation=45)

    ax2 = ax1.twinx()
    color2 = '#d62728'
    ax2.set_ylabel("Total Freight Cost ($ USD)", color=color2, fontweight="bold")
    sns.lineplot(data=monthly, x=range(len(monthly)), y="Total_Cost", color=color2, marker="o", linewidth=2.5, ax=ax2)
    ax2.tick_params(axis='y', labelcolor=color2)
    plt.title("2024 Monthly Shipment Volume & Freight Expenditure Trend", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "3_monthly_volume_seasonality.png"), dpi=200)
    plt.close()

    # Visualization 4: Correlation Matrix Heatmap
    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=.5,
        cbar_kws={"shrink": .8},
        ax=ax
    )
    ax.set_title("Correlation Heatmap of Logistics Performance Variables", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "4_correlation_matrix_heatmap.png"), dpi=200)
    plt.close()

    # Visualization 5: Carrier SLA Performance & Delay Variance
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    carrier_perf = df.groupby(["Carrier_Name", "Delivery_Status"]).size().unstack(fill_value=0)
    carrier_perf_pct = carrier_perf.div(carrier_perf.sum(axis=1), axis=0) * 100
    carrier_perf_pct[["On-Time", "Delayed"]].plot(
        kind="bar",
        stacked=True,
        color=["#2ca02c", "#d62728"],
        ax=ax[0]
    )
    ax[0].set_title("Carrier SLA Adherence Rate (% On-Time vs Delayed)", fontweight="bold")
    ax[0].set_ylabel("Percentage (%)")
    ax[0].set_xlabel("Carrier Name")
    ax[0].set_xticks(range(len(carrier_perf_pct)))
    ax[0].set_xticklabels(carrier_perf_pct.index, rotation=30)
    ax[0].legend(loc="upper right")

    sns.violinplot(data=df, x="Carrier_Name", y="Delay_days", hue="Carrier_Name", palette="Set2", legend=False, ax=ax[1])
    ax[1].axhline(0, color="red", linestyle="--", alpha=0.7)
    ax[1].set_title("Carrier Delay Dispersion & Volatility (Days)", fontweight="bold")
    ax[1].set_xlabel("Carrier Name")
    ax[1].set_ylabel("Delay (Days)")
    ax[1].set_xticks(range(len(carrier_perf_pct)))
    ax[1].set_xticklabels(carrier_perf_pct.index, rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "5_carrier_leadtime_and_delay_analysis.png"), dpi=200)
    plt.close()

    # Visualization 6: Fleet Efficiency - Cost per Ton-Km
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="Transport_Mode", y="Cost_per_Ton_km_usd", hue="Transport_Mode", palette="viridis", legend=False, showfliers=False, ax=ax)
    ax.set_title("Transport Mode Economic Efficiency ($ USD per Ton-Km)", fontweight="bold")
    ax.set_xlabel("Transport Mode")
    ax.set_ylabel("Unit Cost ($ / Ton-Km)")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "6_fleet_efficiency_cost_per_ton_km.png"), dpi=200)
    plt.close()

    print("\n[SUCCESS] Pipeline executed successfully! All visual assets and datasets generated.")

if __name__ == "__main__":
    main()

