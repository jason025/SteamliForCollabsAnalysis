import io
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# 设置页面为宽屏模式
st.set_page_config(layout="wide", page_title="DGP ME Collabs Analysis Dashboard", page_icon="📊")

# 自定义CSS样式
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTitle {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background-color: #3498db;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stSubheader {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0.5rem;
        background-color: #2c3e50;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .card {
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .card-title {
        color: #3498db;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .card-content {
        color: #2c3e50;
    }
    .stInfo {
        background-color: #e8f4f8;
        color: #2c3e50;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
    }
    .stInfo-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e74c3c;
    }
    .module {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
    }
    .pivot-options {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    .pivot-option {
        flex: 1;
        margin-right: 1rem;
    }
    .pivot-option:last-child {
        margin-right: 0;
    }
    .module-divider {
        border-top: 2px solid #3498db;
        margin: 2rem 0;
    }
    .help-tip {
        color: #3498db;
        font-size: 1rem;
        cursor: pointer;
    }
    .stTabs {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTab {
        color: #3498db;
        font-weight: bold;
        font-size: 1.4rem;
    }
    .stTab[aria-selected="true"] {
        color: #ffffff;
        background-color: #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="stTitle">DGP ME Collabs Analysis Dashboard</h1>', unsafe_allow_html=True)


def create_card(title, content):
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-content">{content}</div>
    </div>
    """


@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "data", "Workload Analysis_PQ.csv")
    # utf-8-sig strips the BOM so the first column is "SUPPLIER NAME"
    return pd.read_csv(csv_path, encoding="utf-8-sig")


@st.cache_data
def filter_by_buyer(df, selected_buyer):
    if selected_buyer == "All":
        return df
    return df[df["BUYER NAME"] == selected_buyer]


@st.cache_data
def compute_profile_metrics(df):
    lifecycle_counts = df["Life Cycle"].value_counts()
    return {
        "total_collabs": int(df["Collabs"].sum()),
        "unique_platforms": int(df["Platform"].nunique()),
        "unique_suppliers": int(df["SUPPLIER NAME"].nunique()),
        "dgp_item_count": int(df["DGP ITEM"].nunique()),
        "mp_count": int(lifecycle_counts.get("MP", 0)),
        "ltb_count": int(lifecycle_counts.get("LTB", 0)),
        "npi_count": int(lifecycle_counts.get("NPI", 0)),
        "total_ems_codes": int(df["EMS CODE"].nunique()),
    }


@st.cache_data
def build_pivot_table(df, pivot_index, pivot_columns, pivot_values):
    if pivot_columns == "None":
        pivot_table = df.groupby(pivot_index, as_index=False)[pivot_values].sum()
    else:
        pivot_table = pd.pivot_table(
            df,
            values=pivot_values,
            index=pivot_index,
            columns=pivot_columns,
            aggfunc="sum",
            fill_value=0,
        )
        # Keep only non-zero rows/columns for readability
        pivot_table = pivot_table.loc[(pivot_table != 0).any(axis=1), (pivot_table != 0).any(axis=0)]
    return pivot_table


def quick_stats(df):
    st.markdown('<h3 class="stSubheader">Quick Stats</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Buyers", df["BUYER NAME"].nunique())
    col2.metric("Total Suppliers", df["SUPPLIER NAME"].nunique())
    col3.metric("Total Platforms", df["Platform"].nunique())
    col4.metric("Total Collabs", int(df["Collabs"].sum()))


def export_dataframe(df, export_format, file_stem="exported_data"):
    if export_format == "CSV":
        return {
            "label": "Download CSV",
            "data": df.to_csv(index=False).encode("utf-8-sig"),
            "file_name": f"{file_stem}.csv",
            "mime": "text/csv",
        }

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    return {
        "label": "Download Excel",
        "data": output.getvalue(),
        "file_name": f"{file_stem}.xlsx",
        "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }


df = load_data()

with st.sidebar:
    st.markdown('<h2 class="stSubheader">Controls</h2>', unsafe_allow_html=True)
    buyer_names = ["All"] + sorted(df["BUYER NAME"].dropna().astype(str).unique().tolist())
    selected_buyer = st.selectbox("Select Buyer", buyer_names, key="buyer_select")
    st.caption("Buyer filter applies to Profile, Multidimensional Analysis, and Export.")

filtered_df = filter_by_buyer(df, selected_buyer)
active_scope = "All buyers" if selected_buyer == "All" else f"Buyer: {selected_buyer}"
st.info(f"Current filter — {active_scope} ({len(filtered_df):,} rows)")

tab1, tab2, tab3 = st.tabs(["Source Data", "Profile Analysis & Results", "Multidimensional Analysis"])

with tab1:
    st.markdown('<h2 class="stSubheader">Source Data</h2>', unsafe_allow_html=True)
    st.caption("Full dataset (not affected by buyer filter).")
    st.dataframe(df, use_container_width=True)
    quick_stats(df)

with tab2:
    st.markdown('<h2 class="stSubheader">Profile Analysis</h2>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown('<h2 class="stSubheader">Analysis Results</h2>', unsafe_allow_html=True)
    metrics = compute_profile_metrics(filtered_df)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(create_card("Collaboration Metrics", f"""
        <div class='stInfo'>Total Collabs: <span class='stInfo-value'>{metrics['total_collabs']}</span></div>
        <div class='stInfo'>Platforms: <span class='stInfo-value'>{metrics['unique_platforms']}</span></div>
        <div class='stInfo'>Suppliers: <span class='stInfo-value'>{metrics['unique_suppliers']}</span></div>
        <div class='stInfo'>Total EMS Codes: <span class='stInfo-value'>{metrics['total_ems_codes']}</span></div>
        """), unsafe_allow_html=True)

        st.markdown(create_card("DPN and Lifecycle Counts", f"""
        <div class='stInfo'>DGP ITEM Count: <span class='stInfo-value'>{metrics['dgp_item_count']}</span></div>
        <div class='stInfo'>MP Count: <span class='stInfo-value'>{metrics['mp_count']}</span></div>
        <div class='stInfo'>LTB Count: <span class='stInfo-value'>{metrics['ltb_count']}</span></div>
        <div class='stInfo'>NPI Count: <span class='stInfo-value'>{metrics['npi_count']}</span></div>
        """), unsafe_allow_html=True)

    with col2:
        if selected_buyer == "All":
            buyer_collabs = (
                filtered_df.groupby("BUYER NAME", as_index=False)["Collabs"]
                .sum()
                .nlargest(10, "Collabs")
                .sort_values("Collabs", ascending=False)
            )
            chart_title = "Top Buyers by Collabs"
        else:
            buyer_collabs = (
                filtered_df.groupby("BUYER NAME", as_index=False)["Collabs"]
                .sum()
                .sort_values("Collabs", ascending=False)
            )
            chart_title = f"Collabs for {selected_buyer}"

        fig_bar = px.bar(
            buyer_collabs,
            x="BUYER NAME",
            y="Collabs",
            title=chart_title,
            color="Collabs",
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        fig_bar.update_layout(
            title_font=dict(size=18, color="#3498db", family="Arial, sans-serif"),
            font=dict(size=14, color="#2c3e50", family="Arial, sans-serif"),
            height=650,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Buyer Name",
            yaxis_title="Collabs",
            coloraxis_showscale=False,
        )
        fig_bar.update_traces(texttemplate="%{y}", textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.markdown('<h2 class="stSubheader">Multidimensional Analysis</h2>', unsafe_allow_html=True)
    st.caption("Uses the current buyer filter from the sidebar.")

    col1, col2, col3 = st.columns(3)
    with col1:
        pivot_index = st.selectbox(
            "Select Row",
            ["BUYER NAME", "EMS CODE", "Platform", "Life Cycle"],
            index=0,
            key="pivot_row",
        )
    with col2:
        pivot_columns = st.selectbox(
            "Select Column",
            ["None", "Platform", "Life Cycle", "BUYER NAME", "EMS CODE"],
            index=1,
            key="pivot_col",
        )
    with col3:
        pivot_values = st.selectbox(
            "Select Value",
            ["TTL", "Collabs"],
            index=1,
            key="pivot_val",
        )

    if pivot_columns == pivot_index:
        st.warning("Row and Column dimensions should be different. Showing row aggregation only.")
        pivot_columns = "None"

    try:
        pivot_table = build_pivot_table(filtered_df, pivot_index, pivot_columns, pivot_values)

        col1, col2 = st.columns([3, 7])

        with col1:
            st.markdown("<h3 style='text-align: center;'>Pivot Table</h3>", unsafe_allow_html=True)
            st.dataframe(pivot_table, height=400, use_container_width=True)

        with col2:
            st.markdown("<h3 style='text-align: center;'>Visualization</h3>", unsafe_allow_html=True)
            if pivot_columns == "None":
                fig = px.bar(
                    pivot_table,
                    x=pivot_index,
                    y=pivot_values,
                    title=f"{pivot_index} vs {pivot_values}",
                    labels={pivot_index: pivot_index, pivot_values: pivot_values},
                    height=450,
                    color_discrete_sequence=px.colors.qualitative.Bold,
                )
            else:
                pivot_data = pivot_table.reset_index()
                value_columns = [c for c in pivot_data.columns if c != pivot_index]
                fig = px.bar(
                    pivot_data,
                    x=pivot_index,
                    y=value_columns,
                    title=f"{pivot_index} vs {pivot_columns} ({pivot_values})",
                    labels={pivot_index: pivot_index, "value": pivot_values},
                    height=450,
                    color_discrete_sequence=px.colors.qualitative.Bold,
                )

            fig.update_traces(texttemplate="%{y:.0f}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#2c3e50"),
                hovermode="closest",
                barmode="stack",
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                ),
                margin=dict(r=150, t=100, b=100),
                uniformtext=dict(mode="hide", minsize=8),
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("An error occurred while creating the pivot table. Please try different selections.")
        st.error(f"Error details: {e}")

st.markdown('<h2 class="stSubheader">Data Export</h2>', unsafe_allow_html=True)
st.caption(f"Exports the currently filtered dataset ({active_scope}).")
export_format = st.selectbox("Select export format", ["CSV", "Excel"])
export_payload = export_dataframe(
    filtered_df,
    export_format,
    file_stem="exported_data_all" if selected_buyer == "All" else f"exported_data_{selected_buyer.replace(', ', '_').replace(' ', '_')}",
)
st.download_button(
    label=export_payload["label"],
    data=export_payload["data"],
    file_name=export_payload["file_name"],
    mime=export_payload["mime"],
)

with st.expander("Help"):
    st.markdown("""
    - **Source Data**: 显示原始完整数据集。
    - **Profile Analysis & Results**: 根据侧边栏选定的买家筛选数据，并显示分析结果和图表。
    - **Multidimensional Analysis**: 在当前买家筛选下创建自定义数据透视表和图表。
    - **Data Export**: 导出当前筛选后的数据（CSV 或 Excel）。
    """)
