import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import io

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
        font-size: 1.4rem;  /* 增大字体大小 */
    }
    .stTab[aria-selected="true"] {
        color: #ffffff;
        background-color: #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# 设置页面标题
st.markdown('<h1 class="stTitle">DGP ME Collabs Analysis Dashboard</h1>', unsafe_allow_html=True)

# 创建卡片函数
def create_card(title, content):
    return f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-content">{content}</div>
    </div>
    """

# Read Workload Analysis_PQ.csv file
@st.cache_data
def load_data():
    csv_path = "data/Workload Analysis_PQ.csv"
    df = pd.read_csv(csv_path)
    return df

df = load_data()

# 侧边栏
with st.sidebar:
    st.markdown('<h2 class="stSubheader">Controls</h2>', unsafe_allow_html=True)
    buyer_names = ['All'] + list(df['BUYER NAME'].unique())
    selected_buyer = st.selectbox('Select Buyer', buyer_names, key='buyer_select')

# 主页面使用选项卡布局
tab1, tab2, tab3 = st.tabs(["Source Data", "Profile Analysis & Results", "Multidimensional Analysis"])

# 添加 quick_stats 函数
def quick_stats(df):
    st.markdown('<h3 class="stSubheader">Quick Stats</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Buyers", df['BUYER NAME'].nunique())
    col2.metric("Total Suppliers", df['SUPPLIER NAME'].nunique())
    col3.metric("Total Platforms", df['Platform'].nunique())
    col4.metric("Total Collabs", df['Collabs'].sum())

with tab1:
    st.markdown('<h2 class="stSubheader">Source Data</h2>', unsafe_allow_html=True)
    st.dataframe(df)
    
    # 添加 quick_stats
    quick_stats(df)

with tab2:
    st.markdown('<h2 class="stSubheader">Profile Analysis</h2>', unsafe_allow_html=True)
    
    if selected_buyer != 'All':
        filtered_df = df[df['BUYER NAME'] == selected_buyer]
    else:
        filtered_df = df
    
    st.dataframe(filtered_df)
    
    st.markdown('<h2 class="stSubheader">Analysis Results</h2>', unsafe_allow_html=True)
    
    if selected_buyer != 'All':
        total_collabs = filtered_df['Collabs'].sum()
        unique_platforms = filtered_df['Platform'].nunique()
        unique_suppliers = filtered_df['SUPPLIER NAME'].nunique()
        dgp_item_count = filtered_df['DGP ITEM'].nunique()
        
        lifecycle_counts = filtered_df['Life Cycle'].value_counts()
        mp_count = lifecycle_counts.get('MP', 0)
        ltb_count = lifecycle_counts.get('LTB', 0)
        npi_count = lifecycle_counts.get('NPI', 0)
        
        total_ems_codes = filtered_df['EMS CODE'].nunique()
    else:
        total_collabs = df['Collabs'].sum()
        unique_platforms = df['Platform'].nunique()
        unique_suppliers = df['SUPPLIER NAME'].nunique()
        dgp_item_count = df['DGP ITEM'].nunique()
        
        lifecycle_counts = df['Life Cycle'].value_counts()
        mp_count = lifecycle_counts.get('MP', 0)
        ltb_count = lifecycle_counts.get('LTB', 0)
        npi_count = lifecycle_counts.get('NPI', 0)
        
        total_ems_codes = df['EMS CODE'].nunique()
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(create_card("Collaboration Metrics", f"""
        <div class='stInfo'>Total Collabs: <span class='stInfo-value'>{total_collabs}</span></div>
        <div class='stInfo'>Platforms: <span class='stInfo-value'>{unique_platforms}</span></div>
        <div class='stInfo'>Suppliers: <span class='stInfo-value'>{unique_suppliers}</span></div>
        <div class='stInfo'>Total EMS Codes: <span class='stInfo-value'>{total_ems_codes}</span></div>
        """), unsafe_allow_html=True)
        
        st.markdown(create_card("DPN and Lifecycle Counts", f"""
        <div class='stInfo'>DGP ITEM Count: <span class='stInfo-value'>{dgp_item_count}</span></div>
        <div class='stInfo'>MP Count: <span class='stInfo-value'>{mp_count}</span></div>
        <div class='stInfo'>LTB Count: <span class='stInfo-value'>{ltb_count}</span></div>
        <div class='stInfo'>NPI Count: <span class='stInfo-value'>{npi_count}</span></div>
        """), unsafe_allow_html=True)
    
    with col2:
        # 添加买家和合作次数的柱形图
        if selected_buyer == 'All':
            buyer_collabs = df.groupby('BUYER NAME')['Collabs'].sum().nlargest(10).sort_values(ascending=False)
        else:
            buyer_collabs = filtered_df.groupby('BUYER NAME')['Collabs'].sum().sort_values(ascending=False)
        
        fig_bar = px.bar(buyer_collabs, x=buyer_collabs.index, y='Collabs',
                         title='Top Buyers by Collabs',
                         color='Collabs',
                         color_continuous_scale=px.colors.sequential.Viridis)
        fig_bar.update_layout(
            title_font=dict(size=18, color='#3498db', family="Arial, sans-serif"),
            font=dict(size=14, color='#2c3e50', family="Arial, sans-serif"),
            height=650,  # 调整高度
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Buyer Name",
            yaxis_title="Collabs",
            coloraxis_showscale=False
        )
        fig_bar.update_traces(texttemplate='%{y}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.markdown('<h2 class="stSubheader">Multidimensional Analysis</h2>', unsafe_allow_html=True)
    
    # 将选择控件放在一行，并设置默认值
    col1, col2, col3 = st.columns(3)
    with col1:
        pivot_index = st.selectbox('Select Row', ['BUYER NAME', 'EMS CODE', 'Platform', 'Life Cycle'], index=0, key='pivot_row')
    with col2:
        pivot_columns = st.selectbox('Select Column', ['None', 'Platform', 'Life Cycle', 'BUYER NAME', 'EMS CODE'], index=1, key='pivot_col')
    with col3:
        pivot_values = st.selectbox('Select Value', ['TTL', 'Collabs'], index=1, key='pivot_val')
    
    try:
        # 数据处理部分保持不变
        if pivot_columns == 'None':
            pivot_table = df.groupby(pivot_index)[pivot_values].sum().reset_index()
        else:
            pivot_table = pd.pivot_table(df, 
                                         values=pivot_values, 
                                         index=pivot_index, 
                                         columns=pivot_columns, 
                                         aggfunc='sum', 
                                         fill_value=0)

        # 只显示有数据的部分
        pivot_table = pivot_table.loc[(pivot_table != 0).any(axis=1), (pivot_table != 0).any(axis=0)]

        # 创建两列，左侧放数据表，右侧放图表
        col1, col2 = st.columns([3, 7])
        
        with col1:
            st.markdown("<h3 style='text-align: center;'>Pivot Table</h3>", unsafe_allow_html=True)
            # 使用 st.dataframe 并设置高度，添加滚动条
            st.dataframe(pivot_table, height=400)
        
        with col2:
            st.markdown("<h3 style='text-align: center;'>Visualization</h3>", unsafe_allow_html=True)
            # 添加交互式图表
            if pivot_columns == 'None':
                fig = px.bar(pivot_table, x=pivot_index, y=pivot_values,
                             title=f'{pivot_index} vs {pivot_values}',
                             labels={pivot_index: pivot_index, pivot_values: pivot_values},
                             height=450,
                             color_discrete_sequence=px.colors.qualitative.Bold)
            else:
                pivot_data = pivot_table.reset_index()
                fig = px.bar(pivot_data, x=pivot_index, y=pivot_table.columns[1:], 
                             title=f'{pivot_index} vs {pivot_columns} ({pivot_values})',
                             labels={pivot_index: pivot_index, 'value': pivot_values},
                             height=450,
                             color_discrete_sequence=px.colors.qualitative.Bold)

            # 更新图表布局，优化数字显示
            fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2c3e50'),
                hovermode='closest',
                barmode='stack',  # 使用堆叠条形图
                showlegend=True,  # 显示图例
                legend=dict(
                    orientation="v",  # 垂直方向的图例
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02  # 将图例放在图表右侧
                ),
                margin=dict(r=150, t=100, b=100),  # 增加上下边距，为标签留出空间
                uniformtext=dict(mode="hide", minsize=8),  # 隐藏小于8px的标签
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("An error occurred while creating the pivot table. Please try different selections.")
        st.error(f"Error details: {str(e)}")

# 数据导出功能
st.markdown('<h2 class="stSubheader">Data Export</h2>', unsafe_allow_html=True)
export_format = st.selectbox("Select export format", ["CSV", "Excel"])
if st.button("Export Data"):
    if export_format == "CSV":
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="exported_data.csv", mime="text/csv")
    else:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
        st.download_button(label="Download Excel", data=output.getvalue(), file_name="exported_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 添加帮助信息
with st.expander("Help"):
    st.markdown("""
    - **Source Data**: 显示原始数据集。
    - **Profile Analysis & Results**: 根据选定的买家筛选数据,并显示分析结果和图表。
    - **Multidimensional Analysis**: 创建自定义数据透视表和图表。
    - **Data Export**: 将数据导出为CSV或Excel格式。
    """)
