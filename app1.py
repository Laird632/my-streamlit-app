import streamlit as st
import matplotlib
import os
import pandas as pd
matplotlib.use('Agg')  # 在导入 pyplot 前设置
import matplotlib.pyplot as plt
from matplotlib import rcParams
from openai import OpenAI
import base64
import  json
import traceback
from scipy.interpolate import make_interp_spline
import numpy as np


rcParams['font.family'] = 'Microsoft YaHei'

# 全局设置：删除 X 轴上面的黑色横线和 Y 轴右边的黑色竖线
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False 

# 在图表库中直接设置支持的中文字体   暂定---------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置页面布局
st.set_page_config(layout="wide")
import streamlit as st

# 初始化 session_state 中的 product_type
if "product_type" not in st.session_state:
    st.session_state.product_type = "产品_扫地机器人"  # 或者 "产品_家用洗地机" 作为默认值
# 在页面最顶部注入 CSS
st.markdown("""·
<style>
/* Apple 风格整体基调 */
html, body, .stApp {
    font-family: 'SF Pro Display', 'San Francisco', 'Segoe UI', 'Arial', 'Microsoft YaHei', sans-serif !important;
    background: #F0F0F0 !important;  /* 浅色背景 */  
    color: #1d1d1f !important;  /* 深色文本 */
    letter-spacing: 0.01em;
}

/* 主标题 */
h1, .stMarkdown h1 {
    font-size: 3.8rem !important;
    font-weight: 900 !important;      /* 极粗 */
    color: #111 !important;           /* 更黑 */
    text-align: center;
    margin-top:-6.5rem !important;    /* 减小上间距 */
    margin-bottom: 0.5rem !important; /* 减小下间距 */
    letter-spacing: -0.02em;
    border: none !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.04); /* 微弱阴影 */
}

/* 副标题 */
h2, h3, .stMarkdown h2, .stMarkdown h3 {
    color: #222 !important;           /* 更黑 */
    font-weight: 800 !important;      /* 更粗 */
    padding-left: -5.5rem;             /* 减小左边距 */
    margin-top: -0.5rem !important;    /* 减小上间距 */
    margin-bottom: -2.5rem !important; /* 减小下间距 */
    background: none !important;
}

/* 按钮 */
.stButton > button {
    background: #f5f5f7 !important;  /* 按钮背景 */
    color: #1d1d1f !important;  /* 深色文本 */
    border: 1px solid #d2d2d7 !important;
    border-radius: 16px !important;
    font-size: 1.2rem !important;  /* 增大按钮字体 */
    font-weight: 600 !important;  /* 加粗按钮字体 */
    padding: 0.7rem 2.2rem !important;
    box-shadow: 0 2px 8px 0 rgba(60,60,67,0.07);
    transition: all 0.18s cubic-bezier(.4,0,.2,1);
    margin-top: -1rem !important;
}
.stButton > button:hover {
    background: #e5e5e7 !important;
    color: #0071e3 !important;  /* 悬停时的文本颜色 */
    border-color: #0071e3 !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 4px 16px 0 rgba(60,60,67,0.10);
}

/* 侧边栏 */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;  /* 白色 */
    color: #1d1d1f !important;  /* 深色文本 */
    border-right: 1px solid #e5e5e7 !important;
    /* border-radius: 0 24px 24px 0; */  // Removed rounded corners
    padding-top: 2rem !important;  /* 保持原有的 padding */
    /* 增加侧边栏字体设置 */
    font-family: 'Microsoft YaHei', 'SF Pro Display', 'San Francisco', 'Segoe UI', 'Arial', sans-serif !important;
    font-weight: 600 !important;  /* 加粗 */
    font-size: 1.1rem !important;  /* 增大字体 */
}
.sidebar .sidebar-content {
    padding: 2rem 1.2rem !important;
    font-weight: 600 !important;  /* 加粗 */
    font-size: 1.1rem !important;  /* 增大字体 */
}

/* 选择框、滑块等表单控件 */
.stSelectbox label,
.stSlider label {
    color: #1d1d1f !important;  /* 更深的颜色 */
    font-weight: 700 !important;  /* 更粗 */
    font-size: 1.15rem !important;  /* 更大 */
    margin-bottom: 0.2rem !important;
}
.stSelectbox, .stSlider, .stTextInput, .stNumberInput {
    background: #fff !important;
    border-radius: 12px !important;
    border: 1px solid #e5e5e7 !important;
    box-shadow: 0 1px 4px 0 rgba(60,60,67,0.04);
    padding: 0.5rem 1rem !important;
}

/* 苹果风格卡片阴影美化图表容器 */
.stPlotlyChart, .stDataFrame, .stTable, .stAltairChart, .stPyplot, .stImage {
    background: #fff !important;
    border-radius: 20px !important;  /* 这里是圆角半径 */
    box-shadow: 0 8px 32px 0 rgba(60,60,67,0.13), 0 1.5px 4px 0 rgba(60,60,67,0.06) !important;
    border: 1px solid #e5e5e7 !important;
    padding: 2.5rem 2.5rem 2rem 2.5rem !important;
    margin: 2.5rem 0 !important;
    transition: box-shadow 0.25s cubic-bezier(.4,0,.2,1);
}

/* 鼠标悬停时卡片阴影更明显 */
.stPlotlyChart:hover, .stDataFrame:hover, .stTable:hover, .stAltairChart:hover, .stPyplot:hover, .stImage:hover {
    box-shadow: 0 12px 40px 0 rgba(0,113,227,0.18), 0 2px 8px 0 rgba(60,60,67,0.10) !important;
    border-color: #0071e3 !important;
}

/* 数据表格优化 */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    font-size: 1.05rem !important;
}

/* 隐藏默认元素 */
footer, #MainMenu, .stDeployButton {display: none !important;}

/* 响应式优化 */
@media (max-width: 900px) {
    .stPlotlyChart, .stDataFrame, .stTable, .stAltairChart, .stPyplot {
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    h1, .stMarkdown h1 {
        font-size: 2rem !important;
    }
}

/* 顶部白色区域高度减小 */
.stApp > header {
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

/* 登录标题居中 */
.login-title {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* 登录界面输入框容器居中 */
div[data-testid="stTextInput"] {
    width: 500px !important;
    margin: 0 auto !important;
}

/* 登录按钮居中 */
div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}

/* 调整滚动条宽度 */
::-webkit-scrollbar {
    width: 14px; /* 设置滚动条的宽度 */
}

::-webkit-scrollbar-thumb {
    background-color: #888; /* 设置滚动条的颜色 */
    border-radius: 10px; /* 设置滚动条的圆角 */
}

::-webkit-scrollbar-thumb:hover {
    background-color: #555; /* 设置鼠标悬停时的颜色 */
}

/* 统一日期选择器外框 */
    .stDateInput > div {
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }

/* 产品系列多选框美化 */
.stMultiSelect > div > div {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%) !important;
    border: 2px solid #e3e6ea !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 48px !important;
}

.stMultiSelect > div > div:hover {
    border-color: #0071e3 !important;
    box-shadow: 0 6px 20px rgba(0,113,227,0.15) !important;
    transform: translateY(-1px) !important;
}

.stMultiSelect > div > div:focus-within {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 3px rgba(0,113,227,0.1) !important;
}

/* 多选框标签美化 */
.stMultiSelect label {
    color: #1d1d1f !important;  /* 更深的颜色 */
    font-weight: 700 !important;  /* 更粗 */
    font-size: 1.15rem !important;  /* 更大 */
    margin-bottom: 8px !important;
    letter-spacing: 0.01em !important;
}

/* 多选框选项美化 */
.stMultiSelect [data-baseweb="select"] {
    border-radius: 12px !important;
}

.stMultiSelect [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
}

/* 选项列表美化 */
.stMultiSelect [data-baseweb="popover"] {
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
    border: 1px solid #e9ecef !important;
}

/* 选项项美化 */
.stMultiSelect [data-baseweb="option"] {
    padding: 12px 16px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stMultiSelect [data-baseweb="option"]:hover {
    background: linear-gradient(135deg, #0071e3 0%, #0056b3 100%) !important;
    color: #ffffff !important;
}

/* 复选框标签字体增强 */
.stCheckbox label {
    color: #1d1d1f !important;  /* 更深的颜色 */
    font-weight: 700 !important;  /* 更粗 */
    font-size: 1.15rem !important;  /* 更大 */
}

/* AI质量专家报告部分的特殊样式 */
.stExpander {
    margin-bottom: 2rem !important;  /* 增加间距 */
}

/* 为AI报告中的subheader增加间距 */
.stExpander h3 {
    margin-bottom: 1.5rem !important;  /* 覆盖负边距 */
    margin-top: 1rem !important;  /* 增加上边距 */
}

/* 为AI报告中的markdown内容增加间距 */
.stExpander .stMarkdown {
    margin-bottom: 1rem !important;
    line-height: 1.6 !important;  /* 增加行高 */
}

/* 为AI报告中的问答内容增加间距 */
.stExpander p {
    margin-bottom: 0.8rem !important;
    line-height: 1.5 !important;
}

/* 为AI报告中的标题增加间距 */
.stExpander h1, .stExpander h2, .stExpander h3 {
    margin-bottom: 1rem !important;  /* 覆盖负边距 */
    margin-top: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# 在页面最顶部注入 CSS 和 HTML----------------------------------------------------------------------------
import base64

# 将图片转换为 Base64 编码
with open('C:\\\\Users\\\\Administrator\\\\Desktop\\\\PY\\\\logo.png', 'rb') as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

st.markdown(f"""
<style>
/* 图标容器样式 */
.logo-container {{
    position: absolute;
    top: -80px;
    right: 30px;
    z-index: 1000;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}}

/* 图标样式 */
.logo-img {{
    width: 100px;
    height: auto;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    transition: transform 0.3s ease;
}}
</style>

<!-- 图标容器 -->
<div class="logo-container">
    <img src="data:image/png;base64,{encoded_string}" 
         class="logo-img" 
         alt="Stone Tech Logo"
         title="点击返回首页">
</div>
""", unsafe_allow_html=True)



# 读取故障码查询文件--------------------------------------------------------------------------------------------------
fault_code_path = r"售后数据处理\故障码查询.xlsx"
@st.cache_data
def load_fault_codes():
    try:
        df_fault_codes = pd.read_excel(fault_code_path)
        return df_fault_codes
    except Exception as e:
        st.error(f"读取故障码查询文件时出错: {e}")
        return pd.DataFrame()

# 读取Excel文件
file_path = r"售后数据处理\数据处理.xlsx"

# 加载数据的函数
@st.cache_data
def load_data():
    try:
        df_robot = pd.read_excel(file_path, sheet_name="产品_扫地机器人")
        df_cleaner = pd.read_excel(file_path, sheet_name="产品_家用洗地机")
        return df_robot, df_cleaner
    except Exception as e:
        st.error(f"读取文件时出错: {e}")
        return None, None

df_robot, df_cleaner = load_data()

# 主标题样式
st.markdown("""
    <h1 style='font-family:"Microsoft YaHei"; color:red; font-size:40px; text-align:center;margin-top:0.5rem;'>
        国 内 售 后 数 据 一 览 
    </h1>
""", unsafe_allow_html=True)

# 在侧边栏增加产品类型选择
with st.sidebar:
    st.markdown("""
        <style>
        .custom-margin {
            margin-top: 10px;  /* Adjust this value for height */
        }
        .stButton > button {
            width: 100%;  /* Set button width to 100% */
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-margin"></div>', unsafe_allow_html=True)  # Add custom margin
    
    # 创建两列
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🤖扫地机"):
            st.session_state.product_type = "产品_扫地机器人"
    
    with col2:
        if st.button("🧼洗地机"):
            st.session_state.product_type = "产品_家用洗地机"

# 根据选择获取当前数据框
if st.session_state.product_type == "产品_扫地机器人":
    df = df_robot.copy()
else:
    df = df_cleaner.copy()

# 侧边栏筛选条件
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 产品系列筛选
    product_series_options = ['全选'] + sorted(df['产品系列'].unique().tolist())
    selected_series = st.selectbox("产品系列", product_series_options)
    
    # 根据产品系列筛选数据
    if selected_series != '全选':
        filtered_df = df[df['产品系列'] == selected_series]
    else:
        filtered_df = df.copy()
    
    # 故障部位标签筛选（按数量排序）
    fault_tag_options = ['全选'] + filtered_df['故障部位标签'].value_counts().index.tolist()
    selected_fault_tag = st.selectbox("故障部位标签", fault_tag_options)
    
    if selected_fault_tag != '全选':
        filtered_df = filtered_df[filtered_df['故障部位标签'] == selected_fault_tag]


    # 故障部位筛选（按数量排序）
    fault_location_options = ['全选'] + filtered_df['故障部位'].value_counts().index.tolist()
    selected_fault_location = st.selectbox("故障部位", fault_location_options)
    
    if selected_fault_location != '全选':
        filtered_df = filtered_df[filtered_df['故障部位'] == selected_fault_location]
        
    
    # 故障现象筛选（按数量排序）
    fault_phenomenon_options = ['全选'] + filtered_df['故障现象'].value_counts().index.tolist()
    selected_fault_phenomenon = st.selectbox("故障现象", fault_phenomenon_options)
    
    if selected_fault_phenomenon != '全选':
        filtered_df = filtered_df[filtered_df['故障现象'] == selected_fault_phenomenon]
    


   
with st.sidebar:
    # 获取所有日期并转换为日期类型（动态响应产品系列选择）
    date_series_df = df if selected_series == '全选' else df[df['产品系列'] == selected_series]
    valid_dates = pd.to_datetime(date_series_df['服务结束时间'].dropna()).dt.date.unique()
    
    # 排序日期（确保升序）
    sorted_dates = sorted(valid_dates)
    min_date, max_date = sorted_dates[0], sorted_dates[-1]

    # 使用 st.columns 布局（与原逻辑一致）
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "起始日期",
            min_date,  # 默认最小日期
            min_value=min_date,
            max_value=max_date
        )
    with col2:
        end_date = st.date_input(
            "结束日期",
            max_date,  # 默认最大日期
            min_value=min_date,
            max_value=max_date
        )

    # 隐式"全选"逻辑：当用户未修改默认值时视为选择全部日期
    is_all_selected = (start_date == min_date) and (end_date == max_date)

    # 筛选逻辑（完全复刻原周数筛选行为）
    if not is_all_selected:
        # 定义日期范围检查函数（对应原 is_within_range）
        def is_within_date_range(x):
            try:
                date = pd.to_datetime(x).date()
                return start_date <= date <= end_date
            except:
                return False

        # 应用筛选（与原逻辑完全一致）
        filtered_df = filtered_df[filtered_df['服务结束时间'].apply(is_within_date_range)]


# 在侧边栏增加故障码查询功能------------------新增---------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <style>
        /* 更具体的选择器来设置故障码查询输入框的宽度和居中 */
        .stSidebar div[data-testid="stTextInput"] {
            width: auto !important; /* 设置输入框宽度为自动 */
            max-width: 100% !important; /* 最大宽度为100% */
            margin: 0 auto !important; 
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 在侧边栏增加显示底表数据开关
    show_filtered_data = st.checkbox("数据表显示", value=False)
    
    # 在侧边栏增加故障码查询开关
    show_fault_code_query = st.checkbox("故障码查询", value=False)

    # 仅在复选框被选中时显示故障码查询功能
    if show_fault_code_query:
        fault_code_input = st.text_input("输入故障码（支持模糊查询）")
        if fault_code_input:
            df_fault_codes = load_fault_codes()
            if not df_fault_codes.empty:
                # 进行模糊查询
                filtered_codes = df_fault_codes[df_fault_codes['故障码'].astype(str).str.contains(fault_code_input, case=False, na=False)]
                if not filtered_codes.empty:
                    for _, row in filtered_codes.iterrows():
                        st.write(f"故障码: {row['故障码']}")
                        st.write(f"故障原理分析: {row['故障原理分析']}")
                        st.write("---")
                else:
                    st.warning("未找到匹配的故障码")

    # 在侧边栏增加质量分析报告查询开关
    show_quality_report = st.checkbox("质量报告查询", value=False)

    # 仅在复选框被选中时显示质量分析报告查询功能
    if show_quality_report:
        quality_report_path = r"产品质量报告"
        report_folders = [folder for folder in os.listdir(quality_report_path) if os.path.isdir(os.path.join(quality_report_path, folder))]
        selected_report = st.selectbox("报告查询", report_folders)

# 新增：在主页面显示质量报告
if show_quality_report:  # 仅在复选框被选中时显示
    report_images_path = os.path.join(quality_report_path, selected_report)
    # 获取所有 PNG 图片
    report_images = [img for img in os.listdir(report_images_path) if img.endswith('.png')]
    
    if report_images:
        for img in report_images:
            img_path = os.path.join(report_images_path, img)
            st.image(img_path, caption=img, use_container_width=True)
    else:
        st.warning("该报告文件夹中没有 PNG 图片。")

# 定义一个函数来统一设置图表样式--------------------------------------图表样式设定
def set_chart_style(ax1, ax2, title, xlabel, ylabel1, ylabel2):
    ax1.set_xlabel(xlabel, fontsize=16, fontweight='bold')  # 增加字体大小
    ax1.set_ylabel(ylabel1, color='tab:blue', fontsize=16)  # 增加字体大小
    ax2.set_ylabel(ylabel2, color='tab:red', fontsize=16)  # 增加字体大小
    plt.title(title, fontsize=18, fontweight='bold')  # 增加字体大小
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.tight_layout()
    ax1.grid(axis='y', linestyle='--', color='lightgray', alpha=0.5)  # 使用虚线

    # 添加箭头
    ax1.annotate('', xy=(1, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                 xycoords='axes fraction', textcoords='axes fraction')
    ax1.annotate('', xy=(0, 1), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                 xycoords='axes fraction', textcoords='axes fraction')



# 月度故障分析 ------------------------------------------------------------------------------------------------------
st.subheader("月度故障 - AFR")

# 直接使用过滤后的数据
filtered_df_no_ux = filtered_df

monthly_data = filtered_df_no_ux.groupby('创建时间').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
monthly_data['AFR'] = (monthly_data['故障数'] / monthly_data['累计销量']) * 100

# 计算累计故障数
monthly_data['累计故障数'] = monthly_data['故障数'].cumsum()

# 计算整体故障数的平均值
average_faults = monthly_data['故障数'].mean()

# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.3 else 'tab:blue' for count in monthly_data['故障数']]

fig1, ax1 = plt.subplots(figsize=(12, 5))   # 设置图表 长宽

# 绘制当前月故障数柱状图，调整颜色为蓝色
bars1 = ax1.bar([x - 0.2 for x in range(len(monthly_data['创建时间'].astype(str)))], monthly_data['故障数'], color='tab:blue', alpha=0.6, label=None, width=0.4)

# 绘制累计故障数柱状图
bars2 = ax1.bar([x + 0.2 for x in range(len(monthly_data['创建时间'].astype(str)))], monthly_data['累计故障数'], color='tab:orange', alpha=0.6, label=None, width=0.4)

# 为柱状图添加数据标签
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{int(height)}',
             ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

# 创建次坐标轴
ax2 = ax1.twinx()

# 绘制累计AFR曲线，调整颜色为浅蓝色
line = ax2.plot(monthly_data['创建时间'].astype(str), (monthly_data['累计故障数'] / monthly_data['累计销量']) * 100, color='#00BFFF', marker='o')

# 为折线图添加数据标签
for x, y in zip(monthly_data['创建时间'].astype(str), (monthly_data['累计故障数'] / monthly_data['累计销量']) * 100):
    ax2.text(x, y, f"{y:.2f}%", ha='center', va='bottom')  # 将标签位置调整为底部

# 更新图表标题
product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
chart_title = f"{product_name}-{selected_fault_tag if selected_fault_tag != '全选' else ''}{'-' + selected_fault_location if selected_fault_location != '全选' else ''} 累计AFR".strip()

# 设置图表样式
set_chart_style(ax1, ax2, chart_title, '', '', '')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))  # Format Y-axis as percentage

# 添加图例到图表底部
handles = [bars1, bars2, line[0]]
labels = ['当月返修', '累计返修', '累计AFR']
fig1.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=False)

st.pyplot(fig1)

# 周度故障分析 -----------------------------------------------------------------------------------------------------
# st.subheader("周度故障 - AFR")
weekly_data = filtered_df.groupby('故障周数').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
weekly_data['AFR'] = (weekly_data['故障数'] / weekly_data['累计销量']) * 100

# 计算累计故障数
weekly_data['累计故障数'] = weekly_data['故障数'].cumsum()

# 计算整体故障数的平均值
average_faults = weekly_data['故障数'].mean()

# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.3 else 'tab:blue' for count in weekly_data['故障数']]

fig2, ax1 = plt.subplots(figsize=(12, 5))

# 绘制当前周故障数柱状图
bars1 = ax1.bar([x - 0.2 for x in range(len(weekly_data['故障周数'].astype(str)))], weekly_data['故障数'], color='tab:blue', alpha=0.6, label=None, width=0.4)

# 绘制累计故障数柱状图
bars2 = ax1.bar([x + 0.2 for x in range(len(weekly_data['故障周数'].astype(str)))], weekly_data['累计故障数'], color='tab:orange', alpha=0.6, label=None, width=0.4)

# 为柱状图添加数据标签
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

# 创建次坐标轴
ax2 = ax1.twinx()

# 绘制累计AFR曲线
line = ax2.plot(weekly_data['故障周数'].astype(str), (weekly_data['累计故障数'] / weekly_data['累计销量']) * 100, color='#00BFFF', marker='o')

# 为折线图添加数据标签
for x, y in zip(weekly_data['故障周数'].astype(str), (weekly_data['累计故障数'] / weekly_data['累计销量']) * 100):
    ax2.text(x, y, f"{y:.2f}%", ha='center', va='bottom')  # 将标签位置调整为底部

# 更新图表标题
product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
chart_title_weekly = f"{product_name}-{selected_fault_tag if selected_fault_tag != '全选' else ''} 累计AFR".strip()

# 设置图表样式
set_chart_style(ax1, ax2, chart_title_weekly, '', '', '')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))  # Format Y-axis as percentage
ax1.set_xticklabels(weekly_data['故障周数'].astype(str), rotation=45, ha='right')  # Rotate 45°, right align
# st.pyplot(fig2)


# 单独处理"故障部位标签"和"故障现象"图表的数据--------------------------------------------------------------------------------------
# 仅根据产品系列和周数筛选数据
if selected_series != '全选':
    product_series_filtered_df = df[df['产品系列'] == selected_series]
else:
    product_series_filtered_df = df.copy()

# 应用日期筛选（替换原周数筛选）
if not is_all_selected:
    def is_within_date_range(x):
        try:
            date = pd.to_datetime(x).date()
            return start_date <= date <= end_date
        except:
            return False

    product_series_filtered_df = product_series_filtered_df[
        product_series_filtered_df['服务结束时间'].apply(is_within_date_range)
    ]

# 如果未选择故障部位标签，展示故障部位标签的 TOP10
if selected_fault_tag == '全选':
    st.subheader(f"{selected_series.split('(')[0]}  整机故障-Top10")

    # 过滤掉"用户体验"相关的故障部位标签
    filtered_df_exclude_ux = product_series_filtered_df[~product_series_filtered_df['故障部位标签'].str.contains('用户体验', case=False, na=False)]

    # 如果选择了扫地机器人，进一步排除包含"基站"的故障部位标签
    if st.session_state.product_type == "产品_扫地机器人":
        filtered_df_exclude_ux = filtered_df_exclude_ux[~filtered_df_exclude_ux['故障部位标签'].str.contains('基站', case=False, na=False)]

    # 按故障部位标签分组
    fault_tag_data = filtered_df_exclude_ux.groupby('故障部位标签').agg(
        故障数=('故障数', 'count'),
        累计销量=('累计销量', 'first')
    ).reset_index()

    # 计算AFR
    fault_tag_data['AFR'] = (fault_tag_data['故障数'] / fault_tag_data['累计销量']) * 100

    # 按故障数排序并取Top10
    fault_tag_data = fault_tag_data.sort_values(by='故障数', ascending=False).head(10)

    # 计算累计故障数
    total_faults = filtered_df_exclude_ux['故障数'].sum()

    # 计算累计百分比
    fault_tag_data['累计百分比'] = (fault_tag_data['故障数'].cumsum() / total_faults) * 100

    # 创建图表和主坐标轴
    fig3, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(fault_tag_data['故障部位标签'], fault_tag_data['故障数'], color='tab:blue', alpha=0.6, label=None)

    # 为柱状图添加数据标签 - 居中
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                 ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

    # 添加箭头
    ax1.annotate('', xy=(1, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                 xycoords='axes fraction', textcoords='axes fraction')
    ax1.annotate('', xy=(0, 1), xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                 xycoords='axes fraction', textcoords='axes fraction')

    # 在柱状图上方添加故障率数据
    for i, (fault_count, cumulative_sales) in enumerate(zip(fault_tag_data['故障数'], fault_tag_data['累计销量'])):
        fault_rate = (fault_count / cumulative_sales) * 100
        label_position = fault_count + (ax1.get_ylim()[1] * 0.02)
        ax1.text(i, label_position, f'{fault_rate:.2f}%', ha='center', va='bottom', color='red', fontfamily='Microsoft YaHei', fontweight='normal')

    # 创建次坐标轴
    ax2 = ax1.twinx()

    # 绘制累计百分比曲线
    ax2.plot(fault_tag_data['故障部位标签'], fault_tag_data['累计百分比'], color='darkgray', marker='o', label='累计百分比')

    # 为曲线添加数据标签
    for x, y in zip(fault_tag_data['故障部位标签'], fault_tag_data['累计百分比']):
        ax2.text(x, y, f"{y:.1f}%", ha='center', va='bottom')

    # 格式化
   
    ax2.set_ylabel('累计百分比 (%)', color='darkgray', fontsize=12)

    # 设置标题
    product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
    plt.title(f'{product_name} 整机故障 - Top10', fontsize=16)

    # 添加图例
    ax1.legend(frameon=False, loc='upper right')
    # ax2.legend(frameon=False)

    # 设置图表样式
    set_chart_style(ax1, ax2, f'{product_name} 整机故障 - Top10', '', '', '')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))  # Format Y-axis as percentage
    ax1.set_xticklabels(weekly_data['故障周数'].astype(str), rotation=45, ha='right')  # Rotate 45°, right align

    # 坐标轴45°设置
    plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
    ax1.set_xticks(range(len(fault_tag_data['故障部位标签'])))  # 确保 X 轴刻度正确
    ax1.set_xticklabels(fault_tag_data['故障部位标签'], rotation=45, ha='right')

    # 调整布局以适应图表
    plt.tight_layout()

    # 显示图表
    st.pyplot(fig3)

    # 新增桩故障-Top10图表--------------------------------------------------------------------------------------------------------------------------
    if st.session_state.product_type == "产品_扫地机器人":  # 仅在选择扫地机器人时显示
        st.subheader("桩故障-Top10")

        # 仅选择带有"基站"字段的故障部位标签
        filtered_df_base_station = product_series_filtered_df[product_series_filtered_df['故障部位标签'].str.contains('基站', case=False, na=False)]

        # 按故障现象分组
        fault_phenomenon_data = filtered_df_base_station.groupby('故障现象').agg(
            故障数=('故障数', 'count'),
            累计销量=('累计销量', 'first')
        ).reset_index()

        # 计算AFR
        fault_phenomenon_data['AFR'] = (fault_phenomenon_data['故障数'] / fault_phenomenon_data['累计销量']) * 100

        # 按故障数排序并取Top10
        fault_phenomenon_data = fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)

        # 计算累计故障数
        total_faults = filtered_df_base_station['故障数'].sum()

        # 计算累计百分比
        fault_phenomenon_data['累计百分比'] = (fault_phenomenon_data['故障数'].cumsum() / total_faults) * 100

        # 创建图表
        fig4, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(fault_phenomenon_data['故障现象'], fault_phenomenon_data['故障数'], color='tab:blue', alpha=0.6, label=None)

        # 为柱状图添加数据标签 - 居中
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                    ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

        # 添加箭头
        ax.annotate('', xy=(1, 0), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                    xycoords='axes fraction', textcoords='axes fraction')
        ax.annotate('', xy=(0, 1), xytext=(0, 0),
                    arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                    xycoords='axes fraction', textcoords='axes fraction')

        # 在柱状图上方添加故障率数据
        for i, (fault_count, cumulative_sales) in enumerate(zip(fault_phenomenon_data['故障数'], fault_phenomenon_data['累计销量'])):
            fault_rate = (fault_count / cumulative_sales) * 100
            label_position = fault_count + (ax.get_ylim()[1] * 0.02)
            ax.text(i, label_position, f'{fault_rate:.2f}%', ha='center', va='bottom', color='red', fontfamily='Microsoft YaHei', fontweight='normal')

        # 创建次坐标轴
        ax2 = ax.twinx()

        # 绘制累计百分比曲线
        ax2.plot(fault_phenomenon_data['故障现象'], fault_phenomenon_data['累计百分比'], color='darkgray', marker='o', label='累计百分比')

        # 为曲线添加数据标签
        for x, y in zip(fault_phenomenon_data['故障现象'], fault_phenomenon_data['累计百分比']):
            ax2.text(x, y, f"{y:.1f}%", ha='center', va='bottom')

        # 格式化
        ax2.set_ylabel('累计百分比 (%)', color='darkgray', fontsize=12)

        # 设置标题
        product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
        plt.title(f'{product_name} 桩故障 - Top10', fontsize=16)

        # 添加图例
        ax.legend(frameon=False, loc='upper right')
        # ax2.legend(frameon=False)

        # 设置图表样式
        set_chart_style(ax, ax2, f'{product_name} 桩故障 - Top10', '', '', '')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))  # Format Y-axis as percentage
        ax.set_xticks(range(len(fault_phenomenon_data['故障现象'])))  # 确保 X 轴刻度正确
        ax.set_xticklabels(fault_phenomenon_data['故障现象'], rotation=45, ha='right')

        # 调整布局以适应图表
        plt.tight_layout()

        # 显示图表
        st.pyplot(fig4)

# 如果选择了故障部位标签，展示故障现象的 TOP10
else:
    st.subheader("故障现象-Top10")

    # 根据故障部位标签筛选数据
    filtered_df_fault_tag = product_series_filtered_df[product_series_filtered_df['故障部位标签'] == selected_fault_tag]

    # 按故障现象分组
    fault_phenomenon_data = filtered_df_fault_tag.groupby('故障现象').agg(
        故障数=('故障数', 'count'),
        累计销量=('累计销量', 'first')
    ).reset_index()

    # 计算故障率
    fault_phenomenon_data['故障率'] = (fault_phenomenon_data['故障数'] / fault_phenomenon_data['累计销量']) * 100

    # 按故障数排序并取Top10
    fault_phenomenon_data = fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)

    # 计算累计故障数
    total_faults = filtered_df_fault_tag['故障数'].sum()

    # 计算累计百分比
    fault_phenomenon_data['累计百分比'] = (fault_phenomenon_data['故障数'].cumsum() / total_faults) * 100

    # 创建图表
    fig4, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(fault_phenomenon_data['故障现象'], fault_phenomenon_data['故障数'], color='tab:blue', alpha=0.6, label=None)

    # 为柱状图添加数据标签 - 居中
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

    # 在柱状图上方添加故障率数据
    for i, (fault_count, cumulative_sales) in enumerate(zip(fault_phenomenon_data['故障数'], fault_phenomenon_data['累计销量'])):
        fault_rate = (fault_count / cumulative_sales) * 100
        label_position = fault_count + (ax.get_ylim()[1] * 0.02)
        ax.text(i, label_position, f'{fault_rate:.2f}%', ha='center', va='bottom', color='red', fontfamily='Microsoft YaHei', fontweight='normal')

    # 创建次坐标轴
    ax2 = ax.twinx()

    # 绘制累计百分比曲线
    ax2.plot(fault_phenomenon_data['故障现象'], fault_phenomenon_data['累计百分比'], color='darkgray', marker='o', label='')

    # 为曲线添加数据标签
    for x, y in zip(fault_phenomenon_data['故障现象'], fault_phenomenon_data['累计百分比']):
        ax2.text(x, y, f"{y:.1f}%", ha='center', va='bottom')

    # 格式化
    ax.set_xlabel('故障现象', fontsize=12)
    ax.set_ylabel('故障数', color='tab:blue', fontsize=12)
    ax2.set_ylabel('累计百分比 (%)', color='darkgray', fontsize=12)


    # 设置标题
    product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
    plt.title(f'{product_name} 故障现象-Top10', fontsize=16)

    # 添加图例
    ax.legend(frameon=False, loc='upper right')
    ax2.legend(frameon=False, loc='upper left')

    # 坐标轴45°设置
    plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
    ax.set_xticks(range(len(fault_phenomenon_data['故障现象'])))  # 确保 X 轴刻度正确
    ax.set_xticklabels(fault_phenomenon_data['故障现象'], rotation=45, ha='right')

    set_chart_style(ax, ax2, f'{product_name} 故障现象 - Top10', '', '', '')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))  # Format Y-axis as percentage

    # 调整布局以适应图表
    plt.tight_layout()

    # 显示图表
    st.pyplot(fig4)

# 生产批次故障不良 --------------------------------------------------------------------------------------------------------
st.subheader("生产批次-不良监控")
production_batch_data = filtered_df.groupby('生产批次').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
production_batch_data['AFR'] = (production_batch_data['故障数'] / production_batch_data['累计销量']) * 100

# 计算整体故障数的平均值
average_faults = production_batch_data['故障数'].mean()
# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.7 else 'tab:blue' for count in production_batch_data['故障数']]

fig2, ax1 = plt.subplots(figsize=(12, 5))
bars = ax1.bar(production_batch_data['生产批次'].astype(str), production_batch_data['故障数'], color=colors, alpha=0.6, label=None)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='black', fontfamily='Microsoft YaHei', fontweight='normal')

# 将 X 轴刻度显式设置为唯一的生产批次
ax1.set_xticks(range(len(production_batch_data['生产批次'])))  # 确保 X 轴刻度正确
ax1.set_xticklabels(production_batch_data['生产批次'].astype(str), rotation=45, ha='right')  # 旋转 45°，右对齐

# 动态设置图表标题
product_name = selected_series.split('(')[0] if selected_series != '全选' else '全部产品'
chart_title = f"{product_name}-{selected_fault_tag if selected_fault_tag != '全选' else ''}{'-' + selected_fault_location if selected_fault_location != '全选' else ''} 批次不良图".strip()

set_chart_style(ax1, ax1, chart_title, '', '', '')

# 计算累计故障数的均值
mean_cumulative_faults = production_batch_data['故障数'].mean()

# 添加红色虚线表示累计故障数的均值
ax1.axhline(mean_cumulative_faults, color='darkgray', linestyle='--', label='批次不良均线')
ax1.legend(frameon=False)

proxy_production_batch = matplotlib.patches.Patch(color='tab:blue', alpha=0.6) # 代表蓝色柱子

# 图表底部图例的句柄和标签
fig_legend_handles = [proxy_production_batch]
fig_legend_labels = ['生产批次（周数）']

# 在图表的底部中心添加"-生产批次"的图例
fig2.legend(fig_legend_handles, fig_legend_labels, loc='lower center', ncol=1, bbox_to_anchor=(0.5, -0.05), frameon=False)
st.pyplot(fig2)




# 在侧边栏增加产品故障率/费用损失查询开关
with st.sidebar:
    show_fault_and_cost_analysis = st.checkbox("产品故障率/费用损失查询", value=False)

# 产品对比分析 ------------------------------------------------------------------------------------------------------
if show_fault_and_cost_analysis:
    st.subheader("故障率趋势图")
    
    # 获取所有产品系列
    all_product_series = sorted(df['产品系列'].unique().tolist())
    
    # 多选产品系列
    selected_products = st.multiselect(
        "",  # 这里设为空字符串
        options=all_product_series,
        default=all_product_series[:2] if len(all_product_series) >= 2 else all_product_series,
        help="选择2-4个产品进行对比"
    )
    
    # 创建三列布局用于筛选控件
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # 添加故障部位标签筛选 - 按故障数排序
        fault_tag_counts = df['故障部位标签'].value_counts()
        fault_tag_options = ['全选'] + fault_tag_counts.index.tolist()
        selected_fault_tag_comparison = st.selectbox(
            "故障部位标签筛选",
            options=fault_tag_options,
        )
    
    with col2:
        # 基于故障部位标签动态获取故障码选项 - 按故障数排序
        if selected_fault_tag_comparison != '全选':
            # 筛选出当前故障部位标签对应的数据
            filtered_by_tag = df[df['故障部位标签'] == selected_fault_tag_comparison]
            # 获取该故障部位下的所有故障码，按故障数排序
            fault_code_counts = filtered_by_tag['故障部位'].dropna().value_counts()
            fault_code_options = ['全选'] + fault_code_counts.index.tolist()
        else:
            # 如果选择全选，则显示所有故障码，按故障数排序
            fault_code_counts = df['故障部位'].dropna().value_counts()
            fault_code_options = ['全选'] + fault_code_counts.index.tolist()
        
        # 添加故障码筛选
        selected_fault_code_comparison = st.selectbox(
            "故障部位筛选", 
            options=fault_code_options,
        )
    
    with col3:
        # 基于故障部位标签和故障码动态获取故障现象选项 - 按故障数排序
        if selected_fault_tag_comparison != '全选':
            # 首先基于故障部位标签筛选
            filtered_by_tag = df[df['故障部位标签'] == selected_fault_tag_comparison]
            
            # 如果还选择了特定故障码，进一步筛选
            if selected_fault_code_comparison != '全选':
                filtered_by_tag = filtered_by_tag[filtered_by_tag['故障部位'] == selected_fault_code_comparison]
            
            # 获取筛选后的故障现象，按故障数排序
            fault_phenomenon_counts = filtered_by_tag['故障现象'].value_counts()
            fault_phenomenon_options = ['全选'] + fault_phenomenon_counts.index.tolist()
        else:
            # 如果故障部位标签选择全选，但选择了特定故障码
            if selected_fault_code_comparison != '全选':
                filtered_by_code = df[df['故障部位'] == selected_fault_code_comparison]
                fault_phenomenon_counts = filtered_by_code['故障现象'].value_counts()
                fault_phenomenon_options = ['全选'] + fault_phenomenon_counts.index.tolist()
            else:
                # 如果都选择全选，显示所有故障现象，按故障数排序
                fault_phenomenon_counts = df['故障现象'].value_counts()
                fault_phenomenon_options = ['全选'] + fault_phenomenon_counts.index.tolist()
        
        # 添加故障现象筛选
        selected_fault_phenomenon_comparison = st.selectbox(
            "故障现象筛选",
            options=fault_phenomenon_options,
        )
    
    if len(selected_products) >= 2:
        # 创建对比图表
        fig_comparison, ax = plt.subplots(figsize=(12, 6))
        
        # 定义颜色列表
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for i, product in enumerate(selected_products):
            # 筛选当前产品数据
            product_data = df[df['产品系列'] == product].copy()
            
            # 应用故障部位标签筛选
            if selected_fault_tag_comparison != '全选':
                product_data = product_data[product_data['故障部位标签'] == selected_fault_tag_comparison]
            
            # 应用故障部位筛选
            if selected_fault_code_comparison != '全选':
                product_data = product_data[product_data['故障部位'] == selected_fault_code_comparison]
            
            # 应用故障现象筛选
            if selected_fault_phenomenon_comparison != '全选':
                product_data = product_data[product_data['故障现象'] == selected_fault_phenomenon_comparison]
            
            # 应用日期筛选（如果设置了日期范围）
            if not is_all_selected:
                def is_within_date_range(x):
                    try:
                        date = pd.to_datetime(x).date()
                        return start_date <= date <= end_date
                    except:
                        return False
                product_data = product_data[product_data['服务结束时间'].apply(is_within_date_range)]
            
            # 按创建时间分组计算故障率
            monthly_product_data = product_data.groupby('创建时间').agg(
                故障数=('故障数', 'count'),
                累计销量=('累计销量', 'first')
            ).reset_index()
            
            if not monthly_product_data.empty:
                # 计算累计AFR
                monthly_product_data['累计故障数'] = monthly_product_data['故障数'].cumsum()
                monthly_product_data['累计AFR'] = (monthly_product_data['累计故障数'] / monthly_product_data['累计销量']) * 100
                
                # 创建相对月份（从1开始）
                monthly_product_data['相对月份'] = range(1, len(monthly_product_data) + 1)
                
                # 绘制平滑曲线
                x = monthly_product_data['相对月份']
                y = monthly_product_data['累计AFR']
                if len(x) > 2:
                    xnew = np.linspace(x.min(), x.max(), 200)
                    spl = make_interp_spline(x, y, k=3)
                    y_smooth = spl(xnew)
                    line = ax.plot(xnew, y_smooth,
                                   color=colors[i % len(colors)],
                                   linewidth=2.5,
                                   label=product,
                                   linestyle='-',
                                   solid_capstyle='round',
                                   solid_joinstyle='round')
                else:
                    # 点数太少时用原始线
                    line = ax.plot(x, y,
                                   color=colors[i % len(colors)],
                                   linewidth=2.5,
                                   label=product,
                                   linestyle='-',
                                   solid_capstyle='round',
                                   solid_joinstyle='round')
                
                 # 为数据点添加标签 - 只显示最后一个数值
                if len(monthly_product_data) > 0:
                    last_x = monthly_product_data['相对月份'].iloc[-1]
                    last_y = monthly_product_data['累计AFR'].iloc[-1]
                    ax.text(last_x, last_y, f'{last_y:.2f}%', 
                           ha='center', va='bottom', 
                           fontsize=12, 
                           fontfamily='Microsoft YaHei', 
                           fontweight='bold')
        
        # 动态设置图表标题
        title_parts = []
        if selected_fault_tag_comparison != '全选':
            title_parts.append(selected_fault_tag_comparison)
        if selected_fault_code_comparison != '全选':
            title_parts.append(selected_fault_code_comparison)
        if selected_fault_phenomenon_comparison != '全选':
            title_parts.append(selected_fault_phenomenon_comparison)
        
        if title_parts:
            chart_title = f"产品故障率趋势对比图-{'-'.join(title_parts)}"
        else:
            chart_title = "产品故障率趋势对比图"
        
        ax.set_title(chart_title, fontsize=16, fontweight='bold')
        
        # 设置X轴刻度
        max_months = max([len(df[df['产品系列'] == product].groupby('创建时间').size()) 
                         for product in selected_products])
        ax.set_xticks(range(1, max_months + 1))
        ax.set_xlim(0.5, max_months + 0.5)
        
        # 添加网格
        ax.grid(axis='y', linestyle='--', color='lightgray', alpha=0.5)
        
        # 添加图例
        ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        
        # 添加箭头
        ax.annotate('', xy=(1, 0), xytext=(0, 0),
                   arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                   xycoords='axes fraction', textcoords='axes fraction')
        ax.annotate('', xy=(0, 1), xytext=(0, 0),
                   arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                   xycoords='axes fraction', textcoords='axes fraction')
        
        plt.tight_layout()
        st.pyplot(fig_comparison)
    else:
        st.warning("请至少选择2个产品进行对比分析")

# 月度费用损失分析（整合到产品对比分析中） --------------------------------------------------------------------------------
# 在产品对比分析内部实现费用损失查询功能
if show_fault_and_cost_analysis and len(selected_products) >= 2:
    st.subheader("费用损失查询")
    
    # 添加空行来增加间距
    st.markdown("<br>", unsafe_allow_html=True)

    # 在费用损失预估后增加物料价格输入框
    material_cost = st.number_input("输入物料价格", min_value=0.0, value=0.0, step=0.01)

    # 修改数据处理逻辑
    def calculate_cost_loss(df, material_cost):
        # 检查服务工单类型是否包含"修"字符
        df['费用损失'] = df.apply(lambda row: row['费用损失'] + material_cost if '修' in row['服务工单类型'] else row['费用损失'], axis=1)
        return df

    # 初始化一个空的DataFrame用于存储所有产品的费用损失数据
    all_products_cost_data = pd.DataFrame()

    # 为每个选定的产品计算费用损失
    for product in selected_products:
        # 筛选当前产品数据
        product_data = df[df['产品系列'] == product].copy()
        
        # 应用产品故障率趋势查询中的筛选条件
        if selected_fault_tag_comparison != '全选':
            product_data = product_data[product_data['故障部位标签'] == selected_fault_tag_comparison]
        
        if selected_fault_code_comparison != '全选':
            product_data = product_data[product_data['故障部位'] == selected_fault_code_comparison]
        
        if selected_fault_phenomenon_comparison != '全选':
            product_data = product_data[product_data['故障现象'] == selected_fault_phenomenon_comparison]
        
        # 应用日期筛选（如果设置了日期范围）
        if not is_all_selected:
            def is_within_date_range(x):
                try:
                    date = pd.to_datetime(x).date()
                    return start_date <= date <= end_date
                except:
                    return False
            product_data = product_data[product_data['服务结束时间'].apply(is_within_date_range)]
        
        # 应用物料成本计算
        product_data = calculate_cost_loss(product_data, material_cost)
        
        # 按创建时间分组并计算费用损失的总和
        monthly_product_cost = product_data.groupby('创建时间').agg(
            费用损失=('费用损失', 'sum'),
            累计销量=('累计销量', 'first')
        ).reset_index()
        
        # 添加产品标识
        monthly_product_cost['产品系列'] = product
        
        # 合并到总数据中
        all_products_cost_data = pd.concat([all_products_cost_data, monthly_product_cost])

    # 按创建时间和产品系列分组，确保每个产品每个月都有数据
    all_products_cost_data = all_products_cost_data.groupby(['创建时间', '产品系列']).agg({
        '费用损失': 'sum',
        '累计销量': 'first'
    }).reset_index()

    # 计算每个产品的累计费用损失
    cumulative_data = []
    for product in selected_products:
        product_data = all_products_cost_data[all_products_cost_data['产品系列'] == product].copy()
        product_data = product_data.sort_values('创建时间')
        product_data['累计费用损失'] = product_data['费用损失'].cumsum()
        cumulative_data.append(product_data)

    cumulative_data = pd.concat(cumulative_data)

    # 计算每个产品的单台费用损失预估（1年）
    # 注：单台费用损失预估保持原单位，不做转换
    product_estimates = {}
    for product in selected_products:
        product_data = cumulative_data[cumulative_data['产品系列'] == product]
        if not product_data.empty and len(product_data) > 0:
            last_cumulative_cost = product_data['累计费用损失'].iloc[-1]
            last_sales = product_data['累计销量'].iloc[-1]
            sales_months = len(product_data['创建时间'].unique())
            if last_sales > 0 and sales_months > 0:
                product_estimates[product] = (last_cumulative_cost / last_sales) * (12 / sales_months)
            else:
                product_estimates[product] = 0
        else:
            product_estimates[product] = 0

    # 按创建时间累加所有产品的费用损失，用于绘制柱状图
    monthly_total_cost = all_products_cost_data.groupby('创建时间').agg({
        '费用损失': 'sum'
    }).reset_index()

    # 计算累计总费用损失
    monthly_total_cost = monthly_total_cost.sort_values('创建时间')
    monthly_total_cost['累计费用损失'] = monthly_total_cost['费用损失'].cumsum()

    # 创建图表
    fig_cost, ax1 = plt.subplots(figsize=(12, 5))
    
    # 创建次坐标轴
    ax2 = ax1.twinx()

    # 设置X轴标签为日期字符串
    x = range(len(monthly_total_cost['创建时间'].astype(str)))
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly_total_cost['创建时间'].astype(str), rotation=45, ha='right')


    # 为每个产品绘制月度累计费用损失曲线（右侧Y轴，万单位）
    for i, product in enumerate(selected_products):
        product_data = cumulative_data[cumulative_data['产品系列'] == product]
        if not product_data.empty:
            color = colors[i % len(colors)]
            # 按创建时间排序
            product_data = product_data.sort_values('创建时间')
            # 获取对应的x轴索引位置
            product_x = [x[list(monthly_total_cost['创建时间']).index(dt)] for dt in product_data['创建时间']]
            # 将累计费用损失转换为万单位
            product_data['累计费用损失（万）'] = product_data['累计费用损失'] / 10000
            # 绘制曲线图并添加产品系列图例标签
            ax2.plot(product_x, product_data['累计费用损失（万）'], 
                     color=color, linestyle='-', linewidth=2, 
                     marker='o', markersize=5, 
                     label=f'{product}')

            # 在最后一个数据点显示累计费用损失数值
            if len(product_data) > 0:
                last_point = product_data.iloc[-1]
                last_x = product_x[-1]
                last_y = last_point['累计费用损失（万）']
                ax2.text(last_x, last_y, f' {last_y:.2f}万', 
                        ha='left', va='bottom', color=color, fontsize=10,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 设置固定图表标题
    cost_chart_title = "产品费用损失对比图"

    # 设置图表样式
    plt.title(cost_chart_title, fontsize=16, fontweight='bold')
    
    # 添加X轴和Y轴箭头
    ax1.annotate('', xy=(1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                xycoords='axes fraction', textcoords='axes fraction')
    ax1.annotate('', xy=(0, 1), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='black', lw=0.8),
                xycoords='axes fraction', textcoords='axes fraction')
    
    # 为每个产品添加单台费用损失预估（1年）线（左侧Y轴）
    for i, (product, estimate) in enumerate(product_estimates.items()):
        color = colors[i % len(colors)]
        ax1.axhline(estimate, color=color, linestyle='--')
        
        # 在虚线上添加数值标签
        # 计算图表宽度的中间位置
        mid_x = (ax1.get_xlim()[1] - ax1.get_xlim()[0]) / 2 + ax1.get_xlim()[0]
        # 在虚线中间上方显示数值
        ax1.text(mid_x, estimate * 1.0, f' {estimate:.2f}', 
                ha='center', va='bottom', color=color, fontsize=12, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # 显示产品系列图例，放置在左侧，使用带边框阴影的样式
    ax2.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)

    plt.tight_layout()

    # 显示图表
    st.pyplot(fig_cost)

    # 添加服务工单类型饼状图
    st.subheader("服务工单类型分布")
    
    # 为每个选中的产品生成饼状图
    for i, product in enumerate(selected_products):
        # 筛选当前产品数据
        product_data = df[df['产品系列'] == product].copy()
        
        # 应用筛选条件
        if selected_fault_tag_comparison != '全选':
            product_data = product_data[product_data['故障部位标签'] == selected_fault_tag_comparison]
        
        if selected_fault_code_comparison != '全选':
            product_data = product_data[product_data['故障部位'] == selected_fault_code_comparison]
        
        if selected_fault_phenomenon_comparison != '全选':
            product_data = product_data[product_data['故障现象'] == selected_fault_phenomenon_comparison]
        
        # 应用日期筛选（如果设置了日期范围）
        if not is_all_selected:
            def is_within_date_range(x):
                try:
                    date = pd.to_datetime(x).date()
                    return start_date <= date <= end_date
                except:
                    return False
            product_data = product_data[product_data['服务结束时间'].apply(is_within_date_range)]
        
        # 检查是否有数据
        if not product_data.empty:
            # 按服务工单类型分组统计
            service_type_data = product_data.groupby('服务工单类型').agg({
                '故障数': 'count',
                '费用损失': 'sum'
            }).reset_index()
            
            # 计算总数
            total_count = service_type_data['故障数'].sum()
            
            # 计算百分比
            service_type_data['百分比'] = (service_type_data['故障数'] / total_count * 100).round(2)
            
            # 只显示有数据的类型
            service_type_data = service_type_data[service_type_data['故障数'] > 0]
            
            if not service_type_data.empty:
                # 创建饼状图
                fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
                
                # 设置颜色
                colors = plt.cm.Set3(np.linspace(0, 1, len(service_type_data)))
                
                # 绘制饼状图
                wedges, texts, autotexts = ax_pie.pie(
                    service_type_data['故障数'],
                    labels=service_type_data['服务工单类型'],
                    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*total_count)}件)',
                    colors=colors,
                    startangle=90,
                    counterclock=False
                )
                
                # 设置标题
                ax_pie.set_title(f"{product} 服务工单分布", fontsize=16, fontweight='bold')
                
                # 添加图例
                legend_labels = [
                    f"{row['服务工单类型']}: {row['故障数']}件 ({row['百分比']:.2f}%), 费用损失: {row['费用损失']/10000:.2f}万"
                    for _, row in service_type_data.iterrows()
                ]
                # 调整图例位置和样式
                ax_pie.legend(
                    wedges, 
                    legend_labels, 
                    title="服务工单类型", 
                    loc="upper left", 
                    bbox_to_anchor=(1, 1),
                    fontsize=10,
                    title_fontsize=12,
                    frameon=True,
                    shadow=True,
                    borderpad=1
                )
                
                plt.tight_layout()
                st.pyplot(fig_pie)
                plt.close(fig_pie)
            else:
                st.warning(f"{product} 在当前筛选条件下没有服务工单数据")
        else:
            st.warning(f"{product} 在当前筛选条件下没有数据")

# 显示筛选后的数据
if show_filtered_data:
    st.subheader("筛选后的数据")
    # 确保使用与主界面相同的筛选后数据
    if 'filtered_df' in globals():
        st.dataframe(filtered_df)
    else:
        # 如果filtered_df不存在，使用原始数据
        if st.session_state.product_type == "产品_扫地机器人":
            st.dataframe(df_robot)
        else:
            st.dataframe(df_cleaner)
    
    # 显示月度故障 - AFR图表的底表数据
    st.subheader("月度故障 - AFR 底表数据")
    # 确保使用与主界面相同的筛选后数据
    if 'filtered_df' in globals():
        ai_filtered_df = filtered_df.copy()
    else:
        # 如果filtered_df不存在，使用原始数据
        if st.session_state.product_type == "产品_扫地机器人":
            ai_filtered_df = df_robot.copy()
        else:
            ai_filtered_df = df_cleaner.copy()
    
    # 计算月度故障趋势数据
    monthly_data = ai_filtered_df.groupby('创建时间').agg(
        故障数=('故障数', 'count'),
        累计销量=('累计销量', 'first')
    ).reset_index()
    # 计算累计故障数
    monthly_data['累计故障数'] = monthly_data['故障数'].cumsum()
    # 计算累计AFR
    monthly_data['累计AFR(%)'] = (monthly_data['累计故障数'] / monthly_data['累计销量'] * 100)
    
    # 选择需要显示的列
    monthly_display_data = monthly_data[['创建时间', '故障数', '累计故障数', '累计AFR(%)']]
    st.dataframe(monthly_display_data)
    
    # 显示生产批次-不良监控图表的底表数据
    st.subheader("生产批次-不良监控 底表数据")
    # 计算生产批次故障分布数据
    production_batch_data = ai_filtered_df.groupby('生产批次').agg(
        故障数=('故障数', 'count'),
        累计销量=('累计销量', 'first')
    ).reset_index()
    
    # 选择需要显示的列
    production_batch_display_data = production_batch_data[['生产批次', '故障数']]
    st.dataframe(production_batch_display_data)
    
    # 显示故障现象-Top10图表的底表数据
    st.subheader("故障现象-Top10 底表数据")
    # 应用故障部位标签筛选
    if selected_fault_tag != '全选':
        filtered_df_fault_tag = ai_filtered_df[ai_filtered_df['故障部位标签'] == selected_fault_tag]
    else:
        filtered_df_fault_tag = ai_filtered_df.copy()
    
    # 按故障现象分组
    fault_phenomenon_data = filtered_df_fault_tag.groupby('故障现象').agg(
        故障数=('故障数', 'count'),
        累计销量=('累计销量', 'first')
    ).reset_index()

    # 计算故障率
    fault_phenomenon_data['故障率(%)'] = (fault_phenomenon_data['故障数'] / fault_phenomenon_data['累计销量']) * 100

    # 按故障数排序并取Top10
    fault_phenomenon_data = fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)

    # 计算累计故障数
    total_faults = filtered_df_fault_tag['故障数'].sum()

    # 计算累计百分比
    fault_phenomenon_data['累计百分比(%)'] = (fault_phenomenon_data['故障数'].cumsum() / total_faults) * 100
    
    # 选择需要显示的列
    fault_phenomenon_display_data = fault_phenomenon_data[['故障现象', '故障数', '故障率(%)', '累计百分比(%)']]
    st.dataframe(fault_phenomenon_display_data)
    
    # 一键导出筛选后的底表数据
    if st.button('一键导出筛选后的底表数据'):
        try:
            # 指定完整路径到桌面
            export_path = r'筛选后的底表数据.xlsx'
            # 创建Excel文件，指定编码格式以避免中文乱码
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                # 筛选后的数据
                if 'filtered_df' in globals():
                    filtered_df.to_excel(writer, sheet_name='筛选后的数据', index=False)
                else:
                    # 如果filtered_df不存在，使用原始数据
                    if st.session_state.product_type == "产品_扫地机器人":
                        df_robot.to_excel(writer, sheet_name='筛选后的数据', index=False)
                    else:
                        df_cleaner.to_excel(writer, sheet_name='筛选后的数据', index=False)
                
                # 月度故障 - AFR 底表数据
                monthly_display_data.to_excel(writer, sheet_name='月度故障 - AFR', index=False)
                
                # 生产批次-不良监控 底表数据
                production_batch_display_data.to_excel(writer, sheet_name='生产批次-不良监控', index=False)
                
                # 故障现象-Top10 底表数据
                fault_phenomenon_display_data.to_excel(writer, sheet_name='故障现象-Top10', index=False)
            
            st.success(f'数据已成功导出到 {export_path}')
        except Exception as e:
            st.error(f'导出数据时出错: {e}')


import requests
import json

# 腾讯混元大模型 API 客户端
class HunyuanClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, messages, model="tencent/hunyuan-a13b-instruct:free", timeout=30):
        try:
            response = requests.post(
                url=self.base_url,
                headers=self.headers,
                json={"model": model, "messages": messages},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API请求出错: {str(e)}")
            return {"error": str(e)}

# 缓存 腾讯混元大模型 API 客户端
@st.cache_resource
def get_hunyuan_client():
    return HunyuanClient("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")

client = get_hunyuan_client()

# ✅ AI 分析函数
def perform_ai_analysis(prompt=None, monthly_display_data=None, production_batch_display_data=None, fault_phenomenon_display_data=None):
    try:
        # 初始化会话历史
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        context = {
            "筛选条件": {
                "产品系列": st.session_state.get("product_type", "未选择"),
                "故障部位标签": selected_fault_tag if 'selected_fault_tag' in locals() else "未选择",
                "故障现象": selected_fault_location if 'selected_fault_location' in locals() else "未选择",
                "开始日期": start_date.strftime('%Y-%m-%d') if 'start_date' in globals() else "未选择",
                "结束日期": end_date.strftime('%Y-%m-%d') if 'end_date' in globals() else "未选择",
            },
            "图表数据": {}
        }

        # 填充图表数据
        # 月度故障趋势数据
        if monthly_display_data is not None and not monthly_display_data.empty:
            context["图表数据"]["月度故障趋势"] = {
                "说明": "展示每月故障数量、累计故障数量和累计故障率(AFR)的趋势变化，提示（图表中故障率/百分比数据如0.942代表0.942%，已包含百分数）",
                "时间序列": monthly_display_data['创建时间'].astype(str).tolist(),
                "当月故障数": monthly_display_data['故障数'].tolist(),
                "累计故障数": monthly_display_data['累计故障数'].tolist(),
                "累计故障率(%)": monthly_display_data['累计AFR(%)'].tolist(),
            }
        
        # 故障现象Top10数据
        if fault_phenomenon_display_data is not None and not fault_phenomenon_display_data.empty:
            context["图表数据"]["故障现象Top10"] = {
                "说明": "展示当前筛选条件下最常见的10种故障现象及其故障数、故障率和累计占比，提示（图表中故障率/百分比数据如0.942代表0.942%，已包含百分数）",
                "故障现象": fault_phenomenon_display_data['故障现象'].tolist(),
                "故障数": fault_phenomenon_display_data['故障数'].tolist(),
                "故障率(%)": fault_phenomenon_display_data['故障率(%)'].tolist(),
                "累计占比(%)": fault_phenomenon_display_data['累计百分比(%)'].tolist(),
            }
        
        # 构建请求消息
        system_msg = {"role": "system", "content": "你是资深质量分析专家，擅长从数据中发现产品问题"}
        user_msg_content = ""

        if prompt:
            # 针对用户问题的提示
            user_msg_content = f"""当前筛选条件：{json.dumps(context['筛选条件'], ensure_ascii=False, indent=2, default=str)}
图表数据：{json.dumps(context['图表数据'], ensure_ascii=False, indent=2, default=str)}
用户问题：{prompt}"""
        else:
            # 生成完整报告的提示
            user_msg_content = f"""你是一名高级产品质量专家，专注于消费类智能硬件，长期负责扫地机与洗地机产品的质量数据分析、风险管控和改进策略制定。
你将收到筛选条件与图表数据，请输出一份语言简洁、精准、专业的质量分析报告，供管理层或项目负责人参考。
提示：
1. 累计百分比数据如第一个数据36.9代表36.9%，第二个数据48.7代表累计48.7%。
【分析原则】
- 直达问题核心，提炼有价值的发现；
- 强调问题的业务影响和可执行建议；
- 风格冷静、专业，不使用口语化语气。
【筛选条件】
{json.dumps(context['筛选条件'], ensure_ascii=False, indent=2)}
【图表数据】"""
            for 名称, 数据 in context['图表数据'].items():
                if 数据:
                    user_msg_content += f"\n【{名称}】\n{json.dumps(数据, ensure_ascii=False, indent=2, default=str)}"
            user_msg_content += """
【输出格式】
请严格按照以下结构输出一份中文质量分析报告，语言简洁、逻辑清晰，不做冗余描述：
---
### 📌 数据分析报告：
1. ✅ 核心结论  
（高度提炼的1～3条核心问题，限300字内）
2. ⚠️ 风险聚焦  
（指出主要业务风险的故障模式、批次、产品系列，支持数据引用）
3. 🔧 改善建议 
（提出可执行的改进措施，优先级明确，数量不超过3条）
---
立即输出分析报告。"""
        
        # 调用AI模型
        response = client.chat(
            model="tencent/hunyuan-a13b-instruct:free",
            messages=[system_msg, {"role": "user", "content": user_msg_content}]
        )
        # 检查响应
        if "error" in response:
            error_msg = f"❌ AI分析失败: {response['error']}"
            st.error(error_msg)
        else:
            error_msg = None
            answer = response['choices'][0]['message']['content']
            # 保存到会话历史
            st.session_state.chat_history.append({
                "question": prompt if prompt else "自动分析",
                "answer": answer
            })
            return answer

    except Exception as e:
        import traceback
        error_msg = f"❌ 分析失败：{traceback.format_exc()}"
        st.error(error_msg)
        st.session_state.chat_history.append({
            "question": prompt if prompt else "自动分析",
            "answer": error_msg
        })
    
    return error_msg if error_msg else None

# ✅ 侧边栏分析按钮
with st.sidebar:
    st.markdown("---")
    with st.expander("💬AI 质量专家", expanded=False):
        preset_questions = [
            "基于当前数据做分析，给出具体的建议，以数据分析报告的形式",
            "基于当前数据做故障失效FMEA分析及改善建议",
            "基于当前数据做8D分析报告",
        ]
        selected_question = st.selectbox(
            "快捷提问建议",
            options=[""] + preset_questions,
            index=0,
            key="ai_question_select"
        )
        user_input = st.text_input(
            "输入您的问题",
            value=selected_question if selected_question else "",
            key="ai_question_input"
        )
        if user_input:
            with st.spinner("AI 思考中..."):
                # 执行perform_ai_analysis函数中的数据处理逻辑来获取最新数据
                # 月度故障趋势数据
                ai_filtered_df = filtered_df.copy() if 'filtered_df' in globals() else (df_robot.copy() if st.session_state.product_type == "产品_扫地机器人" else df_cleaner.copy())
                monthly_data = ai_filtered_df.groupby('创建时间').agg(
                    故障数=('故障数', 'count'),
                    累计销量=('累计销量', 'first')
                ).reset_index()
                monthly_data['累计故障数'] = monthly_data['故障数'].cumsum()
                monthly_data['累计AFR(%)'] = (monthly_data['累计故障数'] / monthly_data['累计销量'] * 100)
                latest_monthly_display_data = monthly_data[['创建时间', '故障数', '累计故障数', '累计AFR(%)']]
                
                # 故障现象Top10数据
                filtered_df_fault_tag = ai_filtered_df[ai_filtered_df['故障部位标签'] == selected_fault_tag] if selected_fault_tag != '全选' else ai_filtered_df.copy()
                fault_phenomenon_data = filtered_df_fault_tag.groupby('故障现象').agg(
                    故障数=('故障数', 'count'),
                    累计销量=('累计销量', 'first')
                ).reset_index()
                fault_phenomenon_data['故障率(%)'] = (fault_phenomenon_data['故障数'] / fault_phenomenon_data['累计销量']) * 100
                fault_phenomenon_data = fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)
                total_faults = filtered_df_fault_tag['故障数'].sum()
                fault_phenomenon_data['累计百分比(%)'] = (fault_phenomenon_data['故障数'].cumsum() / total_faults) * 100
                latest_fault_phenomenon_display_data = fault_phenomenon_data[['故障现象', '故障数', '故障率(%)', '累计百分比(%)']]
                
                # 传递最新的底表数据给AI分析函数
                perform_ai_analysis(
                    prompt=user_input,
                    monthly_display_data=latest_monthly_display_data,
                    fault_phenomenon_display_data=latest_fault_phenomenon_display_data
                )

# 主界面显示
if "chat_history" in st.session_state and st.session_state.chat_history:
    st.markdown("---")
    st.subheader("💬 AI 质量专家 - 数据分析报告")
    for item in st.session_state.chat_history:
        with st.expander(f"Q: {item['question']}", expanded=False):
            st.markdown(f"**A:** {item['answer']}")

# 应用底部信息栏
st.markdown("""
<style>
.footer {
    position: fixed;
    right: 10px;
    bottom: 10px;
    background-color: transparent;
    color: #666;
    font-size: 12px;
    z-index: 999;
    padding: 5px 10px;
    border-radius: 5px;
}
</style>
<div class='footer'>
    <p>Roborock: v1.0.0 | 2025 Stoney .</p>
</div>
""", unsafe_allow_html=True)
