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


# 在图表库中直接设置支持的中文字体   暂定---------------------------------
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题



#####  运行 streamlit run C:\Users\11414\Desktop\PY\app1.py   --------------------------------------------------

# 设置页面布局
st.set_page_config(layout="wide")
import streamlit as st
# 在页面最顶部注入 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #ffffff !important;
    color: #1d1d1f !important;
}

/* 主标题样式 */
h1 {
    font-size: 32px !important;
    font-weight: 600 !important;
    color: #1d1d1f !important;
    margin-bottom: 24px !important;
    border-bottom: none !important;
    margin-top: -70px !important; --------------------图表移动
}

/* 按钮样式 */
.stButton > button {
    background: #007aff !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: background-color 0.2s ease;
}

.stButton > button:hover {
    background: #0063cc !important;
    transform: none !important;
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background: #f5f5f7 !important;
    border-right: 1px solid #e0e0e0 !important;
    box-shadow: none !important;
}

.sidebar .sidebar-content {
    padding: 16px !important;
}

/* 筛选框样式 */
.stSelectbox label,
.stSlider label {
    color: #1d1d1f !important;
    font-weight: 500 !important;
}

/* 图表容器样式 */
.stPlotlyChart,
.stDataFrame {
    background: white !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    border: 1px solid #e0e0e0 !important;
}

/* 数据表格样式 */
.stDataFrame {
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* 副标题样式 */
h3 {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1d1d1f !important;
    margin-top: 24px !important;
    border-left: none !important;
    padding-left: 0 !important;
}

/* 隐藏默认元素 */
footer {visibility: hidden;}
.stDeployButton {display:none;}
#MainMenu {visibility: hidden;}

/* 响应式布局优化 */
@media (max-width: 768px) {
    .stPlotlyChart {
        max-width: 100% !important;
        margin: 16px 0 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# 以下是你原有的代码...



# 读取Excel文件
file_path = r"C:\Users\Administrator\Desktop\PY\售后数据处理\数据处理.xlsx"

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

# 在侧边栏增加物料价格输入框------------------------输入物料价格
with st.sidebar:
    material_cost = st.number_input("输入物料价格", min_value=0.0, value=0.0, step=0.01)

# 修改数据处理逻辑
def calculate_cost_loss(df, material_cost):
    # 检查服务工单类型是否包含"修"字符
    df['费用损失'] = df.apply(lambda row: row['费用损失'] + material_cost if '修' in row['服务工单类型'] else row['费用损失'], axis=1)
    return df

# 在加载数据后调用该函数
df_robot = calculate_cost_loss(df_robot, material_cost)
df_cleaner = calculate_cost_loss(df_cleaner, material_cost)

# 主标题样式
st.markdown("""
    <h1 style='font-family:"Microsoft YaHei"; color:red; font-size:40px; text-align:center;'>
        《售后费用损失一览》
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

# 整体费用损失图表 -----------------------------------------------------------------------------------------
st.subheader("整体费用损失")

# 计算费用损失，排除 "用户体验"
cost_loss_data = filtered_df[~filtered_df['故障部位标签'].str.contains("用户体验")].groupby('创建时间').agg(
    费用损失=('费用损失', 'sum')  # 按创建时间求和费用损失
).reset_index()

# 创建费用损失图表
fig5, ax = plt.subplots(figsize=(12, 6))
cost_bars = ax.bar(cost_loss_data['创建时间'], cost_loss_data['费用损失'], color='tab:blue', alpha=0.6, label='费用损失')

# 为柱状图添加数据标签 - 居中
for bar in cost_bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height/2, f'{int(height)}',  # 显示整数
            ha='center', va='center', color='white', fontweight='bold')

# 格式化
ax.set_xlabel('故障月份', fontsize=12)
ax.set_ylabel('损失金额', color='tab:blue', fontsize=12)

# 设置标题
plt.title('费用损失-月度', fontsize=16)

# 添加图例
ax.legend(loc='upper right', fontsize=10)

# 坐标轴设置
ax.set_xticks(range(len(cost_loss_data['创建时间'])))  # 确保 X 轴刻度正确
ax.set_xticklabels(cost_loss_data['创建时间'], rotation=0, ha='center')  # 不旋转

# 调整布局以适应图表
plt.tight_layout()

# 显示图表
st.pyplot(fig5)

# 显示筛选后的数据选项
if st.checkbox('显示筛选后的数据'):
    st.dataframe(filtered_df)

# TOP故障部位损失图表 -----------------------------------------------------------------------------------------
st.subheader("整机-TOP故障部位损失")

# 使用经过筛选的数据
df = filtered_df.copy()  # 使用筛选后的数据

# 计算每个故障部位的数量，排除 "用户体验" 和 "基站"
top_fault_count_data = df[~df['故障部位标签'].str.contains("用户体验") & 
                           ~df['故障部位标签'].str.contains("基站")]['故障部位标签'].value_counts().reset_index()
top_fault_count_data.columns = ['故障部位标签', '故障数']  # 重命名列
top_fault_count_data = top_fault_count_data.head(10)  # 获取前 10 个故障部位

# 计算每个故障部位的费用损失
cost_loss_data = df.groupby('故障部位标签').agg(
    总费用损失=('费用损失', 'sum')  # 计算每个故障部位的总费用损失
).reindex(top_fault_count_data['故障部位标签']).fillna(0)  # 重新索引以确保顺序一致

# 创建 TOP故障部位损失图表
fig_top_fault, ax_top = plt.subplots(figsize=(12, 6))
top_fault_bars = ax_top.bar(top_fault_count_data['故障部位标签'], top_fault_count_data['故障数'], color='tab:green', alpha=0.6, label='故障数')

# 为柱状图添加数据标签 - 居中
for bar in top_fault_bars:
    height = bar.get_height()
    ax_top.text(bar.get_x() + bar.get_width()/2., height/2, f'{int(height)}',  # 显示整数
                 ha='center', va='center', color='white', fontweight='bold')

# 创建折线图
ax2 = ax_top.twinx()  # 创建共享X轴的第二个Y轴
ax2.plot(top_fault_count_data['故障部位标签'], cost_loss_data['总费用损失'], color='tab:red', marker='o', label='费用损失', linewidth=2)

# 为折线图添加数据标签
for i, value in enumerate(cost_loss_data['总费用损失']):
    ax2.text(i, value, f'{int(value)}', ha='center', va='bottom', color='tab:red', fontweight='bold')

# 格式化
ax_top.set_xlabel('故障部位', fontsize=12)
ax_top.set_ylabel('故障数', color='tab:green', fontsize=12)
ax2.set_ylabel('费用损失', color='tab:red', fontsize=12)

# 设置标题
plt.title('TOP故障部位损失', fontsize=16)

# 添加图例
ax_top.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)

# 坐标轴设置
ax_top.set_xticks(range(len(top_fault_count_data['故障部位标签'])))  # 确保 X 轴刻度正确
ax_top.set_xticklabels(top_fault_count_data['故障部位标签'], rotation=45, ha='right')  # 旋转以适应标签

# 调整布局以适应图表
plt.tight_layout()

# 显示图表
st.pyplot(fig_top_fault)



# 桩-TOP故障部位损失图表 -----------------------------------------------------------------------------------------
st.subheader("桩-TOP故障部位损失")

# 使用经过筛选的数据
df = filtered_df.copy()  # 使用筛选后的数据

# 计算每个故障部位的数量，只带 基站
top_fault_count_data = df[df['故障部位标签'].str.contains("基站")]['故障部位'].value_counts().reset_index()
top_fault_count_data.columns = ['故障部位', '故障数']  # 重命名列
top_fault_count_data = top_fault_count_data.head(10)  # 获取前 10 个故障部位

# 计算每个故障部位的费用损失
cost_loss_data = df.groupby('故障部位').agg(
    总费用损失=('费用损失', 'sum')  # 计算每个故障部位的总费用损失
).reindex(top_fault_count_data['故障部位']).fillna(0)  # 重新索引以确保顺序一致

# 创建 TOP故障部位损失图表
fig_top_fault, ax_top = plt.subplots(figsize=(12, 6))
top_fault_bars = ax_top.bar(top_fault_count_data['故障部位'], top_fault_count_data['故障数'], color='tab:green', alpha=0.6, label='故障数')

# 为柱状图添加数据标签 - 居中
for bar in top_fault_bars:
    height = bar.get_height()
    ax_top.text(bar.get_x() + bar.get_width()/2., height/2, f'{int(height)}',  # 显示整数
                 ha='center', va='center', color='white', fontweight='bold')

# 创建折线图
ax2 = ax_top.twinx()  # 创建共享X轴的第二个Y轴
ax2.plot(top_fault_count_data['故障部位'], cost_loss_data['总费用损失'], color='tab:red', marker='o', label='费用损失', linewidth=2)

# 为折线图添加数据标签
for i, value in enumerate(cost_loss_data['总费用损失']):
    ax2.text(i, value, f'{int(value)}', ha='center', va='bottom', color='tab:red', fontweight='bold')

# 格式化
ax_top.set_xlabel('故障部位', fontsize=12)
ax_top.set_ylabel('故障数', color='tab:green', fontsize=12)
ax2.set_ylabel('费用损失', color='tab:red', fontsize=12)

# 设置标题
plt.title('基站相关故障部位TOP10及费用损失', fontsize=16)

# 添加图例
ax_top.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)

# 坐标轴设置
ax_top.set_xticks(range(len(top_fault_count_data['故障部位'])))  # 确保 X 轴刻度正确
ax_top.set_xticklabels(top_fault_count_data['故障部位'], rotation=45, ha='right')  # 旋转以适应标签

# 调整布局以适应图表
plt.tight_layout()

# 显示图表
st.pyplot(fig_top_fault)

