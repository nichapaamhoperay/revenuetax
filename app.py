import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ตั้งค่าหน้าจอแอป
st.set_page_config(page_title="Smart Tax Planner Pro", layout="wide")
st.title("📊 Smart Tax Planner Pro")

# ==========================================
# 1. โซนรายได้ (Income Section)
# ==========================================
st.header("1. รายได้และภาษีหัก ณ ที่จ่าย")
tabs = st.tabs([
    '💰 เงินเดือน (40(1))', '🛡️ ค่าคอมฯ (40(2))', '📈 ค่า FA (40(2))', '🏠 ค่าเช่า (40(5))', '📊 เงินปันผล', 
    '💼 40(6)', '🏗️ 40(7)', '🏢 40(8)', '📈 ลงทุนอื่นๆ', '🏛️ มรดก', '🛡️ ยกเว้น'
])
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# เตรียมตารางข้อมูลเริ่มต้น
if 'df_sal' not in st.session_state:
    st.session_state.df_sal = pd.DataFrame({"เดือน": months, "รายได้": [150000]*12, "หัก ณ ที่จ่าย": [5000]*12})
    st.session_state.df_agt = pd.DataFrame({"เดือน": months, "รายได้": [0]*12, "หัก ณ ที่จ่าย": [0]*12})
    st.session_state.df_fa = pd.DataFrame({"เดือน": months, "รายได้": [0]*12, "หัก ณ ที่จ่าย": [0]*12})
    st.session_state.df_rent = pd.DataFrame({"เดือน": months, "รายได้": [25000]*12, "หัก ณ ที่จ่าย": [0]*12})
    
    div_data = [["KBANK", 20, 5000.0, 0.0, 0.0, 500.0]] + [["", 0, 0.0, 0.0, 0.0, 0.0] for _ in range(9)]
    st.session_state.df_div = pd.DataFrame(div_data, columns=["ชื่อหลักทรัพย์", "อัตราภาษี(%)", "เงินปันผล", "ไม่ได้รับเครดิต", "ยกเว้นภาษี", "หัก ณ ที่จ่าย"])

config = {"เดือน": st.column_config.TextColumn(disabled=True)}

# แท็บ 1-4: รายเดือน
with tabs[0]: 
    df_sal = st.data_editor(st.session_state.df_sal, use_container_width=True, hide_index=True, column_config=config, key="editor_sal")
    st.info(f"**รวมเงินเดือน:** {df_sal['รายได้'].sum():,.2f} บาท | **หัก ณ ที่จ่าย:** {df_sal['หัก ณ ที่จ่าย'].sum():,.2f} บาท")
with tabs[1]: 
    df_agt = st.data_editor(st.session_state.df_agt, use_container_width=True, hide_index=True, column_config=config, key="editor_agt")
    st.info(f"**รวมค่าคอมมิชชัน:** {df_agt['รายได้'].sum():,.2f} บาท | **หัก ณ ที่จ่าย:** {df_agt['หัก ณ ที่จ่าย'].sum():,.2f} บาท")
with tabs[2]: 
    df_fa  = st.data_editor(st.session_state.df_fa, use_container_width=True, hide_index=True, column_config=config, key="editor_fa")
    st.info(f"**รวมค่าตอบแทน FA:** {df_fa['รายได้'].sum():,.2f} บาท | **หัก ณ ที่จ่าย:** {df_fa['หัก ณ ที่จ่าย'].sum():,.2f} บาท")
with tabs[3]: 
    df_rent = st.data_editor(st.session_state.df_rent, use_container_width=True, hide_index=True, column_config=config, key="editor_rent")
    st.info(f"**รวมค่าเช่าบ้าน:** {df_rent['รายได้'].sum():,.2f} บาท | **หัก ณ ที่จ่าย:** {df_rent['หัก ณ ที่จ่าย'].sum():,.2f} บาท")

# แท็บ 5: เงินปันผล
with tabs[4]: 
    st.markdown("💡 *กรอกอัตราภาษีและเงินปันผล ระบบจะคำนวณเครดิตให้ตอนกดประมวลผลค่ะ*")
    df_div = st.data_editor(st.session_state.df_div, use_container_width=True, hide_index=True, key="editor_div")
