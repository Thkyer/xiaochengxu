import streamlit as st
import math

# 页面标题
st.title("计量标准计算工具")
st.markdown("---")

# 侧边栏选择计算类型
calc_type = st.sidebar.selectbox("选择计算类型", ["稳定性考核 (Stability)", "重复性试验 (Repeatability)"])

if calc_type == "稳定性考核 (Stability)":
    st.header("稳定性考核记录计算器")
    st.write("输入 10 次测量值，自动计算 min、max、变化量 Δ 和平均值 ȳ")

    # 输入测量值
    measurements = []
    for i in range(1, 11):
        value = st.number_input(f"第 {i} 次测量值", value=0.0, step=0.01, format="%.4f")
        measurements.append(value)

    # 计算按钮
    if st.button("计算稳定性"):
        if measurements:
            min_val = min(measurements)
            max_val = max(measurements)
            delta = max_val - min_val
            mean_y = sum(measurements) / len(measurements)

            st.subheader("计算结果")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("最小值 (min)", min_val)
            col2.metric("最大值 (max)", max_val)
            col3.metric("变化量 (Δ = max - min)", delta)
            col4.metric("平均值 (ȳ)", mean_y)

            allow_delta = st.number_input("允许变化量", value=0.0, step=0.01)
            if delta <= allow_delta:
                st.success("结论: 稳定性合格")
            else:
                st.error("结论: 稳定性不合格")
        else:
            st.warning("请输入至少一个值！")

elif calc_type == "重复性试验 (Repeatability)":
    st.header("重复性试验记录计算器")
    st.write("输入 10 次测量值 y_i，自动计算平均值 ȳ 和标准差 s")

    # 输入测量值
    measurements = []
    for i in range(1, 11):
        value = st.number_input(f"第 {i} 次测量值 y_{i}", value=0.0, step=0.01, format="%.4f")
        measurements.append(value)

    # 计算按钮
    if st.button("计算重复性"):
        n = len(measurements)
        if n > 1:
            mean_y = sum(measurements) / n
            variance_sum = sum((y - mean_y) ** 2 for y in measurements)
            sample_variance = variance_sum / (n - 1)
            std_dev_s = math.sqrt(sample_variance)

            st.subheader("计算结果")
            col1, col2 = st.columns(2)
            col1.metric("平均值 (ȳ = Σ y_i / n)", mean_y)
            col2.metric("重复性标准差 s", std_dev_s)

            conclusion = st.text_input("结论 (例如: 合格/不合格)")
            if conclusion:
                st.info(f"结论: {conclusion}")
        else:
            st.warning("至少需要 2 个数据点！")

# 页脚
st.markdown("---")
st.caption("基于 Python + Streamlit 构建 | 手机浏览器访问最佳")