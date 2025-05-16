import pandas as pd
import streamlit as st
import matplotlib
import os
matplotlib.use('Agg')  # 在导入 pyplot 前设置
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager as fm

# 指定字体路径
font_path = 'msyh.ttf'  # 确保路径正确，如果文件在子目录中，请提供相对路径

# 加载字体
fm.fontManager.addfont(font_path)

# 全局设置：删除 X 轴上面的黑色横线和 Y 轴右边的黑色竖线
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

# 设置全局字体
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

# 在图表库中直接设置支持的中文字体   暂定---------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


#####  运行 streamlit run C:\Users\11414\Desktop\PY\app1.py   --------------------------------------------------
#####  运行 streamlit run C:\Users\Administrator\Desktop\PY\Streamlit苹果界面.py

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
    font-weight: 700 !important;
    color: #003366 !important;  /* 更深的黑色 */
    text-align: center;
    margin-top: -100px !important;  /* 调整为更小的负值 */
    margin-bottom: 0em !important;  /* 调整为更小的值 */
    letter-spacing: -0.02em;
    border: none !important;
    text-shadow: none !important;
}

/* 副标题 */
h2, h3, .stMarkdown h2, .stMarkdown h3 {
    color: #333333 !important;  /* 深灰色 */
    font-weight: 600 !important;
    border-left: 4px solid #e5e5e7;
    padding-left: 1rem;
    background: none !important;
    margin-top: 1rem !important;
    margin-bottom: 1.2rem !important;
}

/* 按钮 */
.stButton > button {
    background: #f5f5f7 !important;  /* 按钮背景 */
    color: #1d1d1f !important;  /* 深色文本 */
    border: 1px solid #d2d2d7 !important;
    border-radius: 16px !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
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
}
.sidebar .sidebar-content {
    padding: 2rem 1.2rem !important;
}

/* 选择框、滑块等表单控件 */
.stSelectbox label,
.stSlider label {
    color: #333333 !important;  /* 深灰色 */
    font-weight: 500 !important;
    font-size: 1.05rem !important;
    margin-bottom: 0.2rem !important;
}
.stSelectbox, .stSlider, .stTextInput, .stNumberInput {
    background: #fff !important;
    border-radius: 12px !important;
    border: 1px solid #e5e5e7 !important;
    box-shadow: 0 1px 4px 0 rgba(60,60,67,0.04);
    padding: 0.5rem 1rem !important;
}

/* 图表和表格容器 */
.stPlotlyChart, .stDataFrame, .stTable, .stAltairChart, .stPyplot {
    background: #fff !important;
    border-radius: 18px !important;
    padding: 2rem 2rem 1.5rem 2rem !important;
    box-shadow: 0 4px 24px 0 rgba(60,60,67,0.08);
    border: 1px solid #e5e5e7 !important;
    margin: 2rem 0 !important;
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
</style>
""", unsafe_allow_html=True)

# 在页面最顶部注入 CSS 和 HTML----------------------------------------------------------------------------
import base64

# 将图片转换为 Base64 编码
with open('logo.png', 'rb') as img_file:
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
fault_code_path = r"故障码查询.xlsx"
@st.cache_data
def load_fault_codes():
    try:
        df_fault_codes = pd.read_excel(fault_code_path)
        return df_fault_codes
    except Exception as e:
        st.error(f"读取故障码查询文件时出错: {e}")
        return pd.DataFrame()

# 读取Excel文件
file_path = r"数据处理.xlsx"

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
    
    # 故障现象筛选（按数量排序）
    fault_location_options = ['全选'] + filtered_df['故障现象'].value_counts().index.tolist()
    selected_fault_location = st.selectbox("故障现象", fault_location_options)
    
    if selected_fault_location != '全选':
        filtered_df = filtered_df[filtered_df['故障现象'] == selected_fault_location]
    


    # 在侧边栏增加周数筛选框
with st.sidebar:
    # 获取所有周数并排序
    # 首先过滤掉空值
    valid_weeks = df['故障周数'].dropna().unique()
    
    # 根据选择的产品系列过滤周数
    if selected_series != '全选':
        product_series_filtered_df = df[df['产品系列'] == selected_series]
        valid_weeks = product_series_filtered_df['故障周数'].dropna().unique()
    
    try:
        # 修改排序逻辑，先按年份后按周数
        all_weeks = sorted(valid_weeks, key=lambda x: (
            int(x.split('-')[0]) if isinstance(x, str) and '-' in x else 0,  # 年份排序
            int(x.split('-')[1]) if isinstance(x, str) and '-' in x else 0   # 周数排序
        ))
        all_weeks = ['全选'] + all_weeks  # 添加"全选"选项
    except Exception as e:
        st.error(f"周数排序出错：{e}")
        all_weeks = ['全选'] + list(valid_weeks)  # 如果排序失败，直接使用原始顺序
    
    # 使用 st.columns 将两个选择框放在同一行
    col1, col2 = st.columns(2)
    
    with col1:
        start_week = st.selectbox("开始周数", all_weeks, index=0)  # 默认选择第一个选项
    with col2:
        end_week = st.selectbox("结束周数", all_weeks, index=len(all_weeks) - 1)  # 默认选择最后一个选项
    
    # 根据选择的周数范围筛选数据
    if start_week == '全选' or end_week == '全选':
        filtered_df = filtered_df.copy()  # 如果选择"全选"，则不筛选
    else:
        # 提取年份和周数进行比较
        start_year, start_week_num = map(int, start_week.split('-'))
        end_year, end_week_num = map(int, end_week.split('-'))
        
        # 筛选出在范围内的周数
        def is_within_range(x):
            try:
                year, week = map(int, x.split('-'))
                # 先比较年份，如果年份相同再比较周数
                if year < start_year or year > end_year:
                    return False
                if year == start_year and year == end_year:
                    return start_week_num <= week <= end_week_num
                if year == start_year:
                    return week >= start_week_num
                if year == end_year:
                    return week <= end_week_num
                return True
            except:
                return False
        
        filtered_df = filtered_df[filtered_df['故障周数'].apply(is_within_range)]


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

    # 在侧边栏增加产品质量报告查询按钮
    # Keep the dropdown for selecting the report in the sidebar
    quality_report_path = r"产品质量报告"
    report_folders = ['关闭查询'] + [folder for folder in os.listdir(quality_report_path) if os.path.isdir(os.path.join(quality_report_path, folder))]
    selected_report = st.selectbox("质量分析报告查询", report_folders)

# 新增：在主页面显示质量报告
if selected_report != '关闭查询':  # Check if a report is selected and not the empty option
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
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
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
chart_title = f"{selected_series.split('(')[0]}-{selected_fault_tag if selected_fault_tag != '全选' else ''} 累计AFR".strip()

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
chart_title_weekly = f"{selected_series.split('(')[0]}-{selected_fault_tag if selected_fault_tag != '全选' else ''} 累计AFR".strip()

# 设置图表样式
set_chart_style(ax1, ax2, chart_title_weekly, '', '', '')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}%'))  # Format Y-axis as percentage
ax1.set_xticklabels(weekly_data['故障周数'].astype(str), rotation=45, ha='right')  # Rotate 45°, right align
# st.pyplot(fig2)


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
# 在柱状图上方添加故障率数据
for i, row in production_batch_data.iterrows():
    fault_count = row['故障数']
    cumulative_sales = row['累计销量']
    if cumulative_sales > 0:  # 避免除以零
        fault_rate = (fault_count / cumulative_sales) * 100
        # 获取当前柱子的高度
        bar_artist = bars[i]
        bar_height = bar_artist.get_height()
        # 将标签放置在柱子略上方，确保可见
        label_position = bar_height + (ax1.get_ylim()[1] * 0.02 if ax1.get_ylim()[1] > 0 else 0.02) # 如果y轴上限为0则调整
        ax1.text(i, label_position, f'{fault_rate:.2f}%', ha='center', va='bottom', color='red', fontfamily='Microsoft YaHei', fontweight='normal')

# 将 X 轴刻度显式设置为唯一的生产批次
ax1.set_xticks(range(len(production_batch_data['生产批次'])))  # 确保 X 轴刻度正确
ax1.set_xticklabels(production_batch_data['生产批次'].astype(str), rotation=45, ha='right')  # 旋转 45°，右对齐

# 动态设置图表标题
chart_title = f"{selected_series.split('(')[0]}-{selected_fault_tag if selected_fault_tag != '全选' else ''} 批次不良图".strip()
set_chart_style(ax1, ax1, chart_title, '', '', '')

# 计算累计故障数的均值
mean_cumulative_faults = production_batch_data['故障数'].mean()

# 添加红色虚线表示累计故障数的均值
ax1.axhline(mean_cumulative_faults, color='darkgray', linestyle='--', label='批次不良均线')
ax1.legend(frameon=False)

proxy_production_batch = matplotlib.patches.Patch(color='tab:blue', alpha=0.6) # 代表蓝色柱子
proxy_fault_rate_text = matplotlib.lines.Line2D([], [], color='red', linestyle='None', marker='_', markersize=10, markeredgewidth=1.5) # 代表红色故障率文本

# 图表底部图例的句柄和标签
fig_legend_handles = [proxy_production_batch, proxy_fault_rate_text]
fig_legend_labels = ['生产批次（周数）', '批次故障率']

# 在图表的底部中心添加“-生产批次”和“-批次故障率”的图例
fig2.legend(fig_legend_handles, fig_legend_labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.05), frameon=False)
st.pyplot(fig2)



# 单独处理"故障部位标签"和"故障现象"图表的数据--------------------------------------------------------------------------------------
# 仅根据产品系列和周数筛选数据
if selected_series != '全选':
    product_series_filtered_df = df[df['产品系列'] == selected_series]
else:
    product_series_filtered_df = df.copy()

# 应用周数筛选
if start_week != '全选' and end_week != '全选':
    # 提取年份和周数进行比较
    start_year, start_week_num = map(int, start_week.split('-'))
    end_year, end_week_num = map(int, end_week.split('-'))

    def is_within_range(x):
        try:
            year, week = map(int, x.split('-'))
            if year < start_year or year > end_year:
                return False
            if year == start_year and year == end_year:
                return start_week_num <= week <= end_week_num
            if year == start_year:
                return week >= start_week_num
            if year == end_year:
                return week <= end_week_num
            return True
        except:
            return False

    product_series_filtered_df = product_series_filtered_df[product_series_filtered_df['故障周数'].apply(is_within_range)]

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
    plt.title(f'{selected_series.split("(")[0]} 整机故障 - Top10', fontsize=16)

    # 添加图例
    ax1.legend(frameon=False, loc='upper right')
    # ax2.legend(frameon=False)

    # 设置图表样式
    set_chart_style(ax1, ax2, f'{selected_series.split("(")[0]} 整机故障 - Top10', '', '', '')
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
        plt.title(f'{selected_series.split("(")[0]} 桩故障 - Top10', fontsize=16)

        # 添加图例
        ax.legend(frameon=False, loc='upper right')
        # ax2.legend(frameon=False)

        # 设置图表样式
        set_chart_style(ax, ax2, f'{selected_series.split("(")[0]} 桩故障 - Top10', '', '', '')
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
    plt.title(f'{selected_series.split("(")[0]} 故障现象-Top10', fontsize=16)

    # 添加图例
    ax.legend(frameon=False, loc='upper right')
    ax2.legend(frameon=False, loc='upper left')

    # 坐标轴45°设置
    plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
    ax.set_xticks(range(len(fault_phenomenon_data['故障现象'])))  # 确保 X 轴刻度正确
    ax.set_xticklabels(fault_phenomenon_data['故障现象'], rotation=45, ha='right')

    set_chart_style(ax, ax2, f'{selected_series.split("(")[0]} 故障现象 - Top10', '', '', '')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}%'))  # Format Y-axis as percentage

    # 调整布局以适应图表
    plt.tight_layout()

    # 显示图表
    st.pyplot(fig4)




# 显示筛选后的数据选项
if st.checkbox('显示筛选后的数据'):
    st.dataframe(filtered_df)
    if st.button('下载筛选后的数据'):
        try:
            export_path = r'C:\Users\Administrator\Desktop\筛选后的数据_data.xlsx'
            filtered_df.to_excel(export_path, index=False)
            st.success(f'筛选后的数据已成功导出到 {export_path}')
        except Exception as e:
            st.error(f'导出数据时出错: {e}')

# 数据一键导出按钮
if st.button('数据一键导出'):
    try:
        # 指定完整路径
        export_path = r'C:\Users\Administrator\Desktop\数据信息_data.xlsx'
        # 创建Excel文件
        with pd.ExcelWriter(export_path) as writer:
            # 月度故障 - AFR
            if 'monthly_data' in globals():
                monthly_data.to_excel(writer, sheet_name='月度故障 - AFR', index=False)
            # 周度故障 - AFR
            if 'weekly_data' in globals():
                weekly_data.to_excel(writer, sheet_name='周度故障 - AFR', index=False)
            # 生产批次故障不良 - AFR
            if 'production_batch_data' in globals():
                production_batch_data.to_excel(writer, sheet_name='生产批次故障不良 - AFR', index=False)
            # 整机故障-Top10
            if 'fault_tag_data' in globals():
                fault_tag_data.to_excel(writer, sheet_name='整机故障-Top10', index=False)
        st.success(f'数据已成功导出到 {export_path}')
    except Exception as e:
        st.error(f'导出数据时出错: {e}')

