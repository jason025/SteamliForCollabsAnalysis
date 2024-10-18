# DGP ME Collabs Analysis Dashboard

这是一个基于 Streamlit 的 Web 应用程序，用于分析 DGP ME Collabs 数据。

## 功能描述

该应用程序提供以下功能：

- 显示原始数据集
- 根据选定的买家筛选数据并显示分析结果
- 创建自定义数据透视表和图表
- 数据导出功能（CSV 和 Excel 格式）
- 交互式图表和数据可视化
- 多维度数据分析

## 安装

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/dgp-me-collabs-analysis.git
   cd dgp-me-collabs-analysis
   ```

2. 创建并激活虚拟环境：
   ```
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 运行应用

1. 确保您在项目目录中并且虚拟环境已激活

2. 运行 Streamlit 应用：
   ```
   streamlit run app.py
   ```

3. 在浏览器中访问显示的本地 URL（通常是 `http://localhost:8501`）

## 项目结构

```
.
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── Workload Analysis_PQ.csv
```

- `app.py`: 主应用文件
- `requirements.txt`: 项目依赖
- `data/`: 数据文件目录
  - `Workload Analysis_PQ.csv`: 分析所需的数据文件

## 使用指南

1. **Source Data**: 显示原始数据集。
2. **Profile Analysis & Results**: 根据选定的买家筛选数据，并显示分析结果和图表。
3. **Multidimensional Analysis**: 创建自定义数据透视表和图表。
4. **Data Export**: 将数据导出为 CSV 或 Excel 格式。

## 依赖

- streamlit
- pandas
- numpy
- plotly
- xlsxwriter

## 贡献

如果您想为这个项目做出贡献，请遵循以下步骤：

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

[在此处添加您的许可证信息]

## 联系方式

[您的姓名] - [您的邮箱]

项目链接: [https://github.com/your-username/dgp-me-collabs-analysis](https://github.com/your-username/dgp-me-collabs-analysis)
