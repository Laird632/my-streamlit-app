import matplotlib  # 导入 matplotlib 模块
matplotlib.use('Agg')  # 在导入 pyplot 前设置
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from matplotlib import rcParams
rcParams['font.family'] = 'Microsoft YaHei'
# 全局设置：删除 X 轴上面的黑色横线和 Y 轴右边的黑色竖线
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

#####  运行 streamlit run C:\Users\11414\Desktop\PY\app1.py   --------------------------------------------------

# 设置页面布局
st.set_page_config(layout="wide")
import streamlit as st
# 在页面最顶部注入 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400&display=swap');
html, body, .stApp {
    font-family: 'Microsoft YaHei', sans-serif !important;  /* 设置整体字体为微软雅黑 */
    background: #f8f9fa;  /* 设置背景为浅灰色 */
}
            
/* 主标题强化 */
h1 {
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);  /* 设置阴影 */
    border-bottom: 3px solid #e74c3c;  /* 设置下划线颜色 */
    margin-bottom: 3rem !important;  /* 设置下划线间距 */
    margin-top: -80px !important;  # 关键调整  --------------------------------------------------------------------------------------------------------------------
}

/* 按钮美化 */
.stButton > button {
    background: linear-gradient(45deg, #e74c3c, #c0392b) !important;  /* 设置渐变色 */
    border: none !important;  /* 设置无边框 */
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);  /* 设置阴影 */
    transition: all 0.3s ease;  /* 设置过渡效果 */
    border-radius: 8px !important;  /* 设置圆角 */
    margin-top: -5px !important;  # 关键调整  ------------------------------------------------------------------------------
}

.stButton > button:hover {
    transform: translateY(-2px);  /* 设置悬停效果 */
    box-shadow: 0 6px 8px rgba(0,0,0,0.2);  /* 设置阴影 */
}

/* 侧边栏深度美化 */
[data-testid="stSidebar"] {
    background: linear-gradient(145deg, #2c3e50, #34495e) !important;  /* 设置渐变色 */
    color: white !important;  /* 设置文本颜色 */
    box-shadow: 5px 0 15px rgba(0,0,0,0.1);  /* 设置阴影 */
    margin-top: -30px !important;   # 关键调整  ------------------------------------------------------------------------------
}

.sidebar .sidebar-content {
    padding: 2rem 1rem !important;  /* 设置侧边栏内边距 */
}

/* 筛选框样式 */
.stSelectbox label,
.stSlider label {
    color: #ecf0f1 !important;  /* 设置文本颜色 */
    font-weight: 600 !important;  /* 设置字体粗细 */
}

/* 图表容器美化 */
.stPlotlyChart,
.stDataFrame {
    background: white;       /* 设置背景为纯白色 */
    border-radius: 12px;     /* 设置圆角 */
    padding: 1.5rem;        /* 设置内边距 */
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 设置阴影 */
    margin: 1.5rem 0;       /* 设置外边距 */
    border: 1px solid #dee2e6; /* 设置边框 */
}

/* 数据表格优化 */
.stDataFrame {
    border-radius: 8px;       /* 设置圆角 */
    overflow: hidden;         /* 隐藏超出容器的内容 */
}

/* 副标题样式 */
h3 {
    color: #2c3e50 !important;  /* 设置文本颜色 */
    margin-top: 2rem !important;  /* 设置上边距 */
    padding-left: 1rem;          /* 设置左边距 */
    border-left: 4px solid #e74c3c;  /* 设置左边框颜色 */
}

/* 隐藏默认元素 */
footer {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}

/* 响应式布局优化 */
@media (max-width: 768px) {
    .stPlotlyChart {
        max-width: 95%;  /* 设置最大宽度 */
        margin: 1rem auto;  /* 设置自动居中 */
    }
}
      


/* 减小顶部白色区域的高度 */
.stApp > header {
    height: 1px; /* 调整为你想要的高度 */
    padding: 10px 0; /* 调整内边距 */
}                                 
            
""", unsafe_allow_html=True)

# 以下是你原有的代码...



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
    <h1 style='font-family:"Microsoft YaHei"; color:red; font-size:40px; text-align:center;'>
        《石头售后质量一览》
    </h1>
""", unsafe_allow_html=True)

# 产品类型选择
col1, col2 = st.columns(2)
with col1:
    robot_btn = st.button("📦 扫地机器人", use_container_width=True)
with col2:
    cleaner_btn = st.button("🧹 家用洗地机", use_container_width=True)

# 初始化会话状态中的产品类型
if 'product_type' not in st.session_state:
    st.session_state.product_type = "产品_扫地机器人"

if robot_btn:
    st.session_state.product_type = "产品_扫地机器人"
if cleaner_btn:
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
    
    # Update the header based on the selected product type
    if st.session_state.product_type == "产品_扫地机器人":
        st.header("扫地机-产品系列")
    else:
        st.header("洗地机-产品系列")
    
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
    st.header("周数筛选")
    
    # 获取所有周数并排序
    # 首先过滤掉空值
    valid_weeks = df['故障周数'].dropna().unique()
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




# 定义一个函数来统一设置图表样式

def set_chart_style(ax1, ax2, title, xlabel, ylabel1, ylabel2):
    ax1.set_xlabel(xlabel, fontsize=12)
    ax1.set_ylabel(ylabel1, color='tab:blue', fontsize=12)
    ax2.set_ylabel(ylabel2, color='tab:red', fontsize=12)
    plt.title(title, fontsize=16)
    ax1.legend(loc='upper left', fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

# 使用统一的图表样式函数

# 月度故障分析 ------------------------------------------------------------------------------------------------------
st.subheader("月度故障 - AFR")
monthly_data = filtered_df.groupby('创建时间').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
monthly_data['AFR'] = (monthly_data['故障数'] / monthly_data['累计销量']) * 100

# 计算整体故障数的平均值
average_faults = monthly_data['故障数'].mean()
# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.3 else 'tab:blue' for count in monthly_data['故障数']]

fig1, ax1 = plt.subplots(figsize=(12, 5))
bars = ax1.bar(monthly_data['创建时间'].astype(str), monthly_data['故障数'], color=colors, alpha=0.6, label='故障数')
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='white', fontweight='bold')
ax2 = ax1.twinx()
line = ax2.plot(monthly_data['创建时间'].astype(str), monthly_data['AFR'], color='tab:red', marker='o', label='AFR (%)')
for x, y in zip(monthly_data['创建时间'].astype(str), monthly_data['AFR']):
    ax2.text(x, y, f"{y:.3f}%", ha='center', va='bottom')  # 修改为3位小数
set_chart_style(ax1, ax2, '月度故障 - AFR', '故障数（月份）', '故障数', 'AFR (%)')
st.pyplot(fig1)


# 周度故障分析
st.subheader("周度故障 - AFR")
weekly_data = filtered_df.groupby('故障周数').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
weekly_data['AFR'] = (weekly_data['故障数'] / weekly_data['累计销量']) * 100

# 计算整体故障数的平均值
average_faults = weekly_data['故障数'].mean()

# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.3 else 'tab:blue' for count in weekly_data['故障数']]

fig2, ax1 = plt.subplots(figsize=(12, 5))
bars = ax1.bar(weekly_data['故障周数'].astype(str), weekly_data['故障数'], color=colors, alpha=0.6, label='故障数')
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='white', fontweight='bold')
ax2 = ax1.twinx()
line = ax2.plot(weekly_data['故障周数'].astype(str), weekly_data['AFR'], color='tab:red', marker='o', label='AFR (%)')
for x, y in zip(weekly_data['故障周数'].astype(str), weekly_data['AFR']):
    ax2.text(x, y, f"{y:.3f}%", ha='center', va='bottom')  # 修改为3位小数
set_chart_style(ax1, ax2, '周度故障 - AFR', '故障数（周度）', '故障数', 'AFR (%)')
ax1.set_xticklabels(weekly_data['故障周数'].astype(str), rotation=45, ha='right')  # Rotate 45°, right align
st.pyplot(fig2) 


# 生产批次故障不良 - AFR--------------------------------------------------------------------------------------------------------
st.subheader("生产批次故障不良 - AFR")
weekly_data = filtered_df.groupby('生产批次').agg(
    故障数=('故障数', 'count'),
    累计销量=('累计销量', 'first')
).reset_index()
weekly_data['AFR'] = (weekly_data['故障数'] / weekly_data['累计销量']) * 100

# 计算整体故障数的平均值
average_faults = weekly_data['故障数'].mean()
# 设置柱子的颜色
colors = ['tab:red' if count > average_faults * 1.7 else 'tab:blue' for count in weekly_data['故障数']]

fig2, ax1 = plt.subplots(figsize=(12, 5))
bars = ax1.bar(weekly_data['生产批次'].astype(str), weekly_data['故障数'], color=colors, alpha=0.6, label='故障数')
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
             ha='center', va='center', color='white', fontweight='bold')
ax2 = ax1.twinx()
line = ax2.plot(weekly_data['生产批次'].astype(str), weekly_data['AFR'], color='tab:red', marker='o', label='AFR (%)')
for x, y in zip(weekly_data['生产批次'].astype(str), weekly_data['AFR']):
    ax2.text(x, y, f"{y:.2f}%", ha='center', va='bottom')

# Set X-axis ticks explicitly to the unique production batches
ax1.set_xticks(range(len(weekly_data['生产批次'])))  # Ensure X-axis ticks are correct
ax1.set_xticklabels(weekly_data['生产批次'].astype(str), rotation=45, ha='right')  # Rotate 45°, right align

set_chart_style(ax1, ax2, '生产故障批次 - AFR', '批次故障（生产周数）', '故障数', 'AFR (%)')
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
    st.subheader("整机故障-Top10")  # 修改标题

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

    # 创建图表和主坐标轴
    fig3, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(fault_tag_data['故障部位标签'], fault_tag_data['故障数'], color='tab:blue', alpha=0.6, label='故障数')

    # 为柱状图添加数据标签 - 居中
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                 ha='center', va='center', color='white', fontweight='bold')

    # 创建次坐标轴
    ax2 = ax1.twinx()
    line = ax2.plot(fault_tag_data['故障部位标签'], fault_tag_data['AFR'], color='tab:red', marker='o', label='AFR (%)')

    # 为折线图添加数据标签
    for x, y in zip(fault_tag_data['故障部位标签'], fault_tag_data['AFR']):
        ax2.text(x, y, f"{y:.2f}%", ha='center', va='bottom')

    # 格式化
    ax1.set_xlabel('故障部位', fontsize=12)
    ax1.set_ylabel('故障数', color='tab:blue', fontsize=12)
    ax2.set_ylabel('AFR (%)', color='tab:red', fontsize=12)

    # 设置标题
    plt.title('整机故障 - Top10', fontsize=16)  # 修改标题

    # 添加图例
    ax1.legend(loc='upper left', fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)

    # 坐标轴45°设置
    plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
    ax1.set_xticks(range(len(fault_tag_data['故障部位标签'])))  # 确保 X 轴刻度正确
    ax1.set_xticklabels(fault_tag_data['故障部位标签'], rotation=45, ha='right')
    ax2.set_xticks(range(len(fault_tag_data['故障部位标签'])))  # 确保 X 轴刻度正确
    ax2.set_xticklabels(fault_tag_data['故障部位标签'], rotation=45, ha='right')

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

        # 创建图表
        fig4, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(fault_phenomenon_data['故障现象'], fault_phenomenon_data['故障数'], color='tab:blue', alpha=0.6, label='故障数')

        # 为柱状图添加数据标签 - 居中
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                    ha='center', va='center', color='white', fontweight='bold')

        # 创建次坐标轴
        ax2 = ax.twinx()
        line = ax2.plot(fault_phenomenon_data['故障现象'], fault_phenomenon_data['AFR'], color='tab:red', marker='o', label='AFR (%)')

        # 为折线图添加数据标签
        for x, y in zip(fault_phenomenon_data['故障现象'], fault_phenomenon_data['AFR']):
            ax2.text(x, y, f"{y:.2f}%", ha='center', va='bottom')

        # 格式化
        ax.set_xlabel('故障现象', fontsize=12)
        ax.set_ylabel('故障数', color='tab:blue', fontsize=12)
        ax2.set_ylabel('AFR (%)', color='tab:red', fontsize=12)

        # 设置标题
        plt.title('桩故障 - Top10', fontsize=16)

        # 添加图例
        ax.legend(loc='upper left', fontsize=10)
        ax2.legend(loc='upper right', fontsize=10)

        # 坐标轴45°设置
        plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
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
        故障数=('故障数', 'count')
    ).reset_index()

    # 按故障数排序并取Top10
    fault_phenomenon_data = fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)

    # 创建图表
    fig4, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(fault_phenomenon_data['故障现象'], fault_phenomenon_data['故障数'], color='tab:blue', alpha=0.6, label='故障数')

    # 为柱状图添加数据标签 - 居中
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
                ha='center', va='center', color='white', fontweight='bold')

    # 格式化
    ax.set_xlabel('故障现象', fontsize=12)
    ax.set_ylabel('故障数', color='tab:blue', fontsize=12)

    # 设置标题
    plt.title('故障现象-Top10', fontsize=16)

    # 添加图例
    ax.legend(loc='upper right', fontsize=10)

    # 坐标轴45°设置
    plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
    ax.set_xticks(range(len(fault_phenomenon_data['故障现象'])))  # 确保 X 轴刻度正确
    ax.set_xticklabels(fault_phenomenon_data['故障现象'], rotation=45, ha='right')

    # 调整布局以适应图表
    plt.tight_layout()

    # 显示图表
    st.pyplot(fig4)




# 用户体验故障现象Top10分析 -----------------------------------------------------------------------------------------
st.subheader("用户体验-Top10")

# 过滤出"用户体验"相关的故障部位标签
filtered_df_ux = product_series_filtered_df[product_series_filtered_df['故障部位标签'].str.contains('用户体验', case=False, na=False)]

# 按故障现象分组
ux_fault_phenomenon_data = filtered_df_ux.groupby('故障现象').agg(
    故障数=('故障数', 'count')
).reset_index()

# 按故障数排序并取Top10
ux_fault_phenomenon_data = ux_fault_phenomenon_data.sort_values(by='故障数', ascending=False).head(10)

# 创建图表
fig4, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(ux_fault_phenomenon_data['故障现象'], ux_fault_phenomenon_data['故障数'], color='tab:blue', alpha=0.6, label='故障数')

# 为柱状图添加数据标签 - 居中
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{height}',
            ha='center', va='center', color='white', fontweight='bold')

# 格式化
ax.set_xlabel('故障现象', fontsize=12)
ax.set_ylabel('故障数', color='tab:blue', fontsize=12)

# 设置标题
plt.title('用户体验-Top10', fontsize=16)

# 添加图例
ax.legend(loc='upper right', fontsize=10)

# 坐标轴45°设置
plt.xticks(rotation=45, ha='right')  # 旋转 45°，并右对齐
ax.set_xticks(range(len(ux_fault_phenomenon_data['故障现象'])))  # 确保 X 轴刻度正确
ax.set_xticklabels(ux_fault_phenomenon_data['故障现象'], rotation=45, ha='right')

# 调整布局以适应图表
plt.tight_layout()

# 显示图表
st.pyplot(fig4)


# 显示筛选后的数据选项
if st.checkbox('显示筛选后的数据'):
    st.dataframe(filtered_df)
