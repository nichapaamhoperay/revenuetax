import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

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

# เตรียมตารางข้อมูลเริ่มต้น (ถ้าโหลดจากไฟล์ Draft จะใช้ตัวเลขใหม่แทน)
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
    
    tot_div_amt = pd.to_numeric(df_div["เงินปันผล"], errors='coerce').sum()
    tot_div_wht = pd.to_numeric(df_div["หัก ณ ที่จ่าย"], errors='coerce').sum()
    st.info(f"**รวมเงินปันผล:** {tot_div_amt:,.2f} บาท | **หัก ณ ที่จ่าย:** {tot_div_wht:,.2f} บาท")

# แท็บ 6: 40(6)
with tabs[5]:
    st.markdown("##### 💼 เงินได้ 40(6) วิชาชีพอิสระ (หมอ, ทนายความ, บัญชี ฯลฯ)")
    inc_6 = st.number_input("รวมรายได้ 40(6) ทั้งปี", min_value=0, value=0, step=10000, key="inc_6")
    wht_6 = st.number_input("ภาษีหัก ณ ที่จ่าย 40(6)", min_value=0, value=0, step=1000, key="wht_6")
    st.info(f"**รวมรายได้ 40(6):** {inc_6:,.2f} บาท | **หัก ณ ที่จ่าย:** {wht_6:,.2f} บาท")

# แท็บ 7: 40(7)
with tabs[6]:
    st.markdown("##### 🏗️ เงินได้ 40(7) รับเหมา (ลงทุนสัมภาระ)")
    inc_7 = st.number_input("รวมรายได้ 40(7) ทั้งปี", min_value=0, value=0, step=10000, key="inc_7")
    wht_7 = st.number_input("ภาษีหัก ณ ที่จ่าย 40(7)", min_value=0, value=0, step=1000, key="wht_7")
    st.info(f"**รวมรายได้ 40(7):** {inc_7:,.2f} บาท | **หัก ณ ที่จ่าย:** {wht_7:,.2f} บาท")

# แท็บ 8: 40(8)
with tabs[7]:
    st.markdown("##### 🏢 เงินได้ 40(8) ธุรกิจอื่นๆ (พาณิชย์, เกษตร, ขายของออนไลน์ ฯลฯ)")
    inc_8 = st.number_input("รวมรายได้ 40(8) ทั้งปี", min_value=0, value=0, step=10000, key="inc_8")
    wht_8 = st.number_input("ภาษีหัก ณ ที่จ่าย 40(8)", min_value=0, value=0, step=1000, key="wht_8")
    st.info(f"**รวมรายได้ 40(8):** {inc_8:,.2f} บาท | **หัก ณ ที่จ่าย:** {wht_8:,.2f} บาท")

# แท็บ 9: ลงทุนอื่นๆ
with tabs[8]:
    st.markdown("##### 📈 เงินได้จากการลงทุนอื่นๆ")
    col1, col2 = st.columns(2)
    
    inc_inv_1 = col1.number_input("ดอกเบี้ย", min_value=0, value=0, step=1000, key="inc_inv_1")
    wht_inv_1 = col2.number_input("หัก ณ ที่จ่าย ดอกเบี้ย", min_value=0, value=0, step=100, key="wht_inv_1")
    
    inc_inv_2 = col1.number_input("เงินเทียบเท่าปันผล", min_value=0, value=0, step=1000, key="inc_inv_2")
    wht_inv_2 = col2.number_input("หัก ณ ที่จ่าย เงินเทียบเท่าปันผล", min_value=0, value=0, step=100, key="wht_inv_2")
    
    inc_inv_3 = col1.number_input("Cryptocurrency / Digital Token", min_value=0, value=0, step=1000, key="inc_inv_3")
    wht_inv_3 = col2.number_input("หัก ณ ที่จ่าย Crypto", min_value=0, value=0, step=100, key="wht_inv_3")
    
    inc_inv_4 = col1.number_input("กำไรจากการขาย RMF", min_value=0, value=0, step=1000, key="inc_inv_4")
    wht_inv_4 = col2.number_input("หัก ณ ที่จ่าย RMF", min_value=0, value=0, step=100, key="wht_inv_4")
    
    inc_inv_5 = col1.number_input("กำไรจากการขาย LTF", min_value=0, value=0, step=1000, key="inc_inv_5")
    wht_inv_5 = col2.number_input("หัก ณ ที่จ่าย LTF", min_value=0, value=0, step=100, key="wht_inv_5")
    
    inc_inv_6 = col1.number_input("กำไรจากการขาย SSF", min_value=0, value=0, step=1000, key="inc_inv_6")
    wht_inv_6 = col2.number_input("หัก ณ ที่จ่าย SSF", min_value=0, value=0, step=100, key="wht_inv_6")
    
    inc_inv = inc_inv_1 + inc_inv_2 + inc_inv_3 + inc_inv_4 + inc_inv_5 + inc_inv_6
    wht_inv = wht_inv_1 + wht_inv_2 + wht_inv_3 + wht_inv_4 + wht_inv_5 + wht_inv_6
    
    st.info(f"**รวมรายได้ลงทุนอื่นๆ:** {inc_inv:,.2f} บาท | **หัก ณ ที่จ่าย:** {wht_inv:,.2f} บาท")

# แท็บ 10: มรดก
with tabs[9]:
    st.markdown("##### 🏛️ รายได้จากมรดก / รับให้")
    col1, col2 = st.columns(2)
    inc_inherit = col1.number_input("ยอดเงินมรดกที่ได้รับ", min_value=0, value=0, step=50000, key="inc_inherit")
    wht_inherit = col2.number_input("ภาษีหัก ณ ที่จ่าย มรดก", min_value=0, value=0, step=1000, key="wht_inherit")
    st.info(f"**รวมรายได้มรดก:** {inc_inherit:,.2f} บาท | **หัก ณ ที่จ่าย:** {wht_inherit:,.2f} บาท")

# แท็บ 11: ยกเว้น
with tabs[10]:
    st.markdown("##### 🛡️ เงินได้ที่ได้รับการยกเว้นภาษี")
    col1, col2 = st.columns(2)
    
    inc_ex_1 = col1.number_input("PVD (ส่วนที่เกิน 10,000 บาท)", min_value=0, value=0, step=1000, key="inc_ex_1")
    inc_ex_2 = col2.number_input("กบข. / สงเคราะห์ครูโรงเรียนเอกชน", min_value=0, value=0, step=1000, key="inc_ex_2")
    
    inc_ex_3 = col1.number_input("ค่าชดเชยที่ได้รับตามกฎหมาย", min_value=0, value=0, step=1000, key="inc_ex_3")
    inc_ex_4 = col2.number_input("เงินได้ยกเว้นอื่นๆ", min_value=0, value=0, step=1000, key="inc_ex_4")
    
    inc_exempt = inc_ex_1 + inc_ex_2 + inc_ex_3 + inc_ex_4
    st.info(f"**รวมเงินได้ยกเว้นภาษี:** {inc_exempt:,.2f} บาท")

# ==========================================
# 2. โซนกราฟ (Live Chart)
# ==========================================
st.header("2. กราฟสรุปรายได้รายเดือน")
st.caption("*(กราฟแสดงผลเฉพาะรายได้รายเดือน 40(1), 40(2) และ 40(5) จากแท็บ 1-4)*")
sal_arr, agt_arr, fa_arr, rent_arr = df_sal["รายได้"].values, df_agt["รายได้"].values, df_fa["รายได้"].values, df_rent["รายได้"].values
total_monthly = sal_arr + agt_arr + fa_arr + rent_arr

fig, ax = plt.subplots(figsize=(10, 4), facecolor='#f8f9fa')
ax.bar(months, sal_arr, label='Salary', color='#007bff')
ax.bar(months, agt_arr, bottom=sal_arr, label='Commission', color='#28a745')
ax.bar(months, fa_arr, bottom=sal_arr+agt_arr, label='FA', color='#ffc107')
ax.bar(months, rent_arr, bottom=sal_arr+agt_arr+fa_arr, label='Rent', color='#17a2b8')

max_y = max(total_monthly) if len(total_monthly) > 0 and max(total_monthly) > 0 else 100000
for i, v in enumerate(total_monthly):
    if v > 0: ax.text(i, v + (max_y * 0.02), f"{v:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.legend(bbox_to_anchor=(1, 1))
st.pyplot(fig)

# ==========================================
# 3. โซนค่าลดหย่อน (Deductions)
# ==========================================
st.markdown("---")
st.header("3. สิทธิลดหย่อนและบริจาค")
ded_tabs = st.tabs(['1. ครอบครัว/ส่วนตัว', '2. ประกัน/ลงทุน', '3. ดอกเบี้ยบ้าน', '4. E-Receipt', '5. บริจาค'])

with ded_tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        w_self = st.number_input("ลดหย่อนผู้มีเงินได้ (60,000 บาท)", value=60000, disabled=True)
        w_is_65 = st.checkbox("ผู้มีเงินได้อายุ 65 ปีขึ้นไป (ได้รับยกเว้น 190,000 บาท)", key="w_is_65")
        w_is_disabled_self = st.checkbox("ผู้มีเงินได้เป็นคนพิการ (ได้รับยกเว้น 190,000 บาท)", key="w_is_disabled_self")
        w_spouse = st.checkbox("คู่สมรสไม่มีรายได้ (60,000 บาท)", key="w_spouse")
        w_child_total = st.number_input("จำนวนบุตรทั้งหมด", min_value=0, value=2, key="w_child_total")
        w_child_after61 = st.number_input("บุตรที่เกิดปี 2561 เป็นต้นไป", min_value=0, value=2, key="w_child_after61")
        w_child_adopt = st.number_input("จำนวนบุตรบุญธรรม", min_value=0, value=0, key="w_child_adopt")
    with c2:
        w_parent = st.number_input("เลี้ยงดูบิดามารดา (คนละ 30k)", min_value=0, max_value=4, value=0, key="w_parent")
        w_parent_hlth = st.number_input("เบี้ยประกันสุขภาพบิดามารดา (Max 15k)", min_value=0, value=0, step=1000, key="w_parent_hlth")
        w_disable = st.number_input("เลี้ยงดูคนพิการ (คนละ 60k)", min_value=0, value=0, key="w_disable")
    
    alw_child = 0
    if w_child_total > 0:
        if w_child_total == w_child_after61: alw_child = 30000 + max(0, (w_child_after61 - 1) * 60000)
        else: alw_child = (max(0, w_child_total - w_child_after61) * 30000) + (w_child_after61 * 60000)
    t1 = 60000 + (60000 if w_spouse else 0) + alw_child + (min(w_parent, 4) * 30000) + min(w_parent_hlth, 15000) + (w_disable * 60000)
    
    # คำนวณเงินได้ที่ได้รับยกเว้น (กรณี 65+ และคนพิการ)
    self_exempt = (190000 if w_is_65 else 0) + (190000 if w_is_disabled_self else 0)
    
    if self_exempt > 0:
        st.success(f"**รวมมูลค่าลดหย่อนหมวดครอบครัว:** {t1:,.0f} บาท | 🌟 **ได้รับสิทธิยกเว้นเงินได้:** {self_exempt:,.0f} บาท")
    else:
        st.success(f"**รวมมูลค่าลดหย่อนหมวดครอบครัว:** {t1:,.0f} บาท")

with ded_tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        w_life = st.number_input("ประกันชีวิตทั่วไป (Max 100k)", min_value=0, value=100000, step=5000, key="w_life")
        w_hlth = st.number_input("ประกันสุขภาพ (Max 25k)", min_value=0, value=25000, step=1000, key="w_hlth")
        w_soc = st.number_input("ประกันสังคม (Max 9k)", min_value=0, value=9000, step=500, key="w_soc")
    with c2:
        st.markdown("**กลุ่มเกษียณ (รวมกันไม่เกิน 500,000)**")
        w_pvd = st.number_input("Provident Fund (PVD)", min_value=0, value=120000, step=5000, key="w_pvd")
        w_rmf = st.number_input("กองทุน RMF", min_value=0, value=50000, step=5000, key="w_rmf")
        w_pension = st.number_input("ประกันชีวิตแบบบำนาญ", min_value=0, value=0, step=5000, key="w_pension")
        st.markdown("**แยกวงเงิน**")
        w_tesg = st.number_input("กองทุน ThaiESG (Max 300k)", min_value=0, value=30000, step=5000, key="w_tesg")

with ded_tabs[2]: w_home = st.number_input("ดอกเบี้ยบ้าน (Max 100k)", min_value=0, value=100000, step=5000, key="w_home")
with ded_tabs[3]: w_easy = st.number_input("Easy E-Receipt (Max 50k)", min_value=0, value=0, step=1000, key="w_easy")
with ded_tabs[4]:
    c1, c2 = st.columns(2)
    with c1:
        w_don_edu = st.number_input("บริจาคการศึกษา/รพ. (ได้ x2)", min_value=0, value=0, step=1000, key="w_don_edu")
        w_don_gen = st.number_input("บริจาคทั่วไป", min_value=0, value=10000, step=1000, key="w_don_gen")
    with c2:
        w_don_pol = st.number_input("บริจาคพรรคการเมือง (Max 10k)", min_value=0, value=0, step=500, key="w_don_pol")

# ==========================================
# 4. ประมวลผลภาษี
# ==========================================
st.markdown("---")
if st.button("🧮 ประมวลผลภาษี", type="primary", use_container_width=True):
    # 1. จัดการรายได้
    inc_1 = df_sal["รายได้"].sum()
    inc_2_agt = df_agt["รายได้"].sum()
    inc_2_fa = df_fa["รายได้"].sum()
    inc_2 = inc_2_agt + inc_2_fa
    inc_5 = df_rent["รายได้"].sum()
    
    wht_1 = df_sal["หัก ณ ที่จ่าย"].sum()
    wht_2 = df_agt["หัก ณ ที่จ่าย"].sum() + df_fa["หัก ณ ที่จ่าย"].sum()
    wht_5 = df_rent["หัก ณ ที่จ่าย"].sum()
    
    tot_div_c = 0
    for _, row in df_div.iterrows():
        rate = pd.to_numeric(row["อัตราภาษี(%)"], errors='coerce')
        amt = pd.to_numeric(row["เงินปันผล"], errors='coerce')
        if pd.notna(rate) and pd.notna(amt) and 0 < rate < 100 and amt > 0:
            tot_div_c += amt * (rate / (100.0 - rate))
    
    # รวมฐานภาษีพึงประเมิน 
    total_income = inc_1 + inc_2 + inc_5 + inc_6 + inc_7 + inc_8 + inc_inv + tot_div_amt + tot_div_c
    wht_base = wht_1 + wht_2 + wht_5 + wht_6 + wht_7 + wht_8 + wht_inv
    wht_total = wht_base + tot_div_wht
    
    # คำนวณค่าใช้จ่าย
    exp_1_2 = min((inc_1 + inc_2) * 0.5, 100000)
    exp_5 = inc_5 * 0.30
    exp_6 = inc_6 * 0.30
    exp_7 = inc_7 * 0.60
    exp_8 = inc_8 * 0.60
    exp_total = exp_1_2 + exp_5 + exp_6 + exp_7 + exp_8
    
    # หักเงินได้ที่ได้รับยกเว้น (กรณี 65+ และคนพิการ) ออกจากฐานรายได้พึงประเมิน
    inc_after_exp = max(0, total_income - exp_total - self_exempt)

    # Scenario A (ลงทุน)
    cap_life_hlth_A = min(w_life + min(w_hlth, 25000), 100000)
    cap_retire_A = min(min(w_pension, total_income * 0.15, 200000) + min(w_pvd, total_income * 0.15, 500000) + min(w_rmf, total_income * 0.30, 500000), 500000)
    alw_tesg_A = min(w_tesg, total_income * 0.30, 300000)
    alw_soc_capped = min(w_soc, 9000)
    
    tot_allowance_A = t1 + alw_soc_capped + min(w_home, 100000) + min(w_easy, 50000) + cap_life_hlth_A + cap_retire_A + alw_tesg_A
    net_pre_don_A = max(0, inc_after_exp - tot_allowance_A - min(w_don_pol, 10000))
    don_A = min(w_don_edu * 2, net_pre_don_A * 0.1) + min(w_don_gen, (net_pre_don_A - min(w_don_edu * 2, net_pre_don_A * 0.1)) * 0.1)
    net_inc_A = net_pre_don_A - don_A

    # Scenario B (ไม่ลงทุน)
    tot_allowance_B = t1 + alw_soc_capped + min(w_home, 100000) + min(w_easy, 50000) + min(w_pvd, total_income * 0.15, 500000)
    net_pre_don_B = max(0, inc_after_exp - tot_allowance_B - min(w_don_pol, 10000))
    don_B = min(w_don_edu * 2, net_pre_don_B * 0.1) + min(w_don_gen, (net_pre_don_B - min(w_don_edu * 2, net_pre_don_B * 0.1)) * 0.1)
    net_inc_B = net_pre_don_B - don_B

    # คิดภาษี
    tax_A = tax_B = prev = 0
    rem_A, rem_B = net_inc_A, net_inc_B
    
    # สร้างตาราง HTML แบบตัดปัญหาการเว้นบรรทัด
    bracket_html = ""
    for lim, rate in [(150000, 0), (300000, 0.05), (500000, 0.1), (750000, 0.15), (1000000, 0.2), (2000000, 0.25), (5000000, 0.3), (float('inf'), 0.35)]:
        t_A, t_B = max(0, min(rem_A, lim - prev)), max(0, min(rem_B, lim - prev))
        tax_in_A, tax_in_B = t_A * rate, t_B * rate
        tax_A += tax_in_A; tax_B += tax_in_B
        if t_B > 0 or t_A > 0 or lim == 150000:
            lim_text = f"{lim:,.0f}" if lim != float('inf') else ""
            bracket_html += f'<tr><td style="border: 1px solid #dee2e6; padding: 5px;">{lim_text}</td><td style="border: 1px solid #dee2e6; padding: 5px;">{rate*100:.2f}%</td><td style="border: 1px solid #dee2e6; padding: 5px; text-align: right;">{t_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px; text-align: right;">{t_B:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px; text-align: right;">{tax_in_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px; text-align: right;">{tax_in_B:,.2f}</td></tr>'
        rem_A -= t_A; rem_B -= t_B; prev = lim
        if rem_A <= 0 and rem_B <= 0 and lim > net_inc_B: break

    final_tax_A = tax_A - wht_total - tot_div_c
    eff_A = (tax_A / total_income * 100) if total_income > 0 else 0
    eff_B = (tax_B / total_income * 100) if total_income > 0 else 0
    
    if final_tax_A < 0: final_class, final_label = "background-color: #155724; color: white;", "= มีภาษีที่ชำระไว้เกิน (ได้คืน)"
    else: final_class, final_label = "background-color: #8b0000; color: white;", "= มีภาษีที่ต้องชำระ"

    # ==========================================
    # แสดงผล Breakdown
    # ==========================================
    st.markdown("---")
    st.markdown("### 📋 สรุปรายละเอียดการคำนวณ (Breakdown)")
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        st.markdown("#### 1️⃣ สรุปรายได้และค่าใช้จ่าย")
        html_rows = []
        exp_1_2_shown = False
        
        if inc_1 > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>เงินเดือน 40(1):</b> {inc_1:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>หักค่าใช้จ่าย 40(1)+(2): {exp_1_2:,.2f} บาท</td></tr>")
            exp_1_2_shown = True
        if inc_2 > 0:
            exp_text = f"หักค่าใช้จ่าย 40(1)+(2): {exp_1_2:,.2f} บาท" if not exp_1_2_shown else ""
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>ค่าตอบแทน 40(2):</b> {inc_2:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>{exp_text}</td></tr>")
        if inc_5 > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>ค่าเช่า 40(5):</b> {inc_5:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>หักค่าใช้จ่าย 40(5) (30%): {exp_5:,.2f} บาท</td></tr>")
        if inc_6 > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>วิชาชีพอิสระ 40(6):</b> {inc_6:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>หักค่าใช้จ่าย 40(6) (30%): {exp_6:,.2f} บาท</td></tr>")
        if inc_7 > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>รับเหมา 40(7):</b> {inc_7:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>หักค่าใช้จ่าย 40(7) (60%): {exp_7:,.2f} บาท</td></tr>")
        if inc_8 > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>ธุรกิจ 40(8):</b> {inc_8:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #495057;'>หักค่าใช้จ่าย 40(8) (60%): {exp_8:,.2f} บาท</td></tr>")
        if inc_inv > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>ลงทุนอื่นๆ:</b> {inc_inv:,.2f} บาท</td><td style='padding: 4px 0; border: none;'></td></tr>")
        if tot_div_amt > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none;'>&#8226; <b>เงินปันผล 40(4):</b> {tot_div_amt:,.2f} บาท</td><td style='padding: 4px 0; border: none;'></td></tr>")
        
        # เพิ่มบรรทัดยกเว้นเงินได้สำหรับผู้สูงอายุและคนพิการ (แบบเน้นสีตัวอักษร)
        if self_exempt > 0:
            html_rows.append(f"<tr><td style='padding: 4px 0; border: none; color: #0c5460;'>&#8226; <b>ยกเว้น (65ปี/คนพิการ):</b> {self_exempt:,.2f} บาท</td><td style='padding: 4px 0; border: none; color: #0c5460;'>หักออกจากฐานรายได้</td></tr>")

        if html_rows: st.markdown(f"<table style='width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 15px;'>{''.join(html_rows)}</table>", unsafe_allow_html=True)
        
        st.info(f"**รวมเงินได้พึงประเมิน:** {total_income:,.2f} บาท\n\n**รวมค่าใช้จ่ายที่หักได้:** {exp_total:,.2f} บาท" + (f"\n\n**ได้รับสิทธิยกเว้น (65ปี/คนพิการ):** {self_exempt:,.2f} บาท" if self_exempt > 0 else ""))
        
        st.markdown("#### 4️⃣ ภาษีหัก ณ ที่จ่าย และ เครดิตปันผล")
        if wht_1 > 0: st.write(f"- หัก ณ ที่จ่าย 40(1): {wht_1:,.2f} บาท")
        if wht_2 > 0: st.write(f"- หัก ณ ที่จ่าย 40(2): {wht_2:,.2f} บาท")
        if wht_inv > 0: st.write(f"- หัก ณ ที่จ่าย ลงทุนอื่นๆ: {wht_inv:,.2f} บาท")
        if wht_5 > 0: st.write(f"- หัก ณ ที่จ่าย 40(5): {wht_5:,.2f} บาท")
        if wht_6 > 0: st.write(f"- หัก ณ ที่จ่าย 40(6): {wht_6:,.2f} บาท")
        if wht_7 > 0: st.write(f"- หัก ณ ที่จ่าย 40(7): {wht_7:,.2f} บาท")
        if wht_8 > 0: st.write(f"- หัก ณ ที่จ่าย 40(8): {wht_8:,.2f} บาท")
        if tot_div_wht > 0: st.write(f"- หัก ณ ที่จ่าย ปันผล: {tot_div_wht:,.2f} บาท")
        if wht_inherit > 0: st.write(f"- หัก ณ ที่จ่าย มรดก: {wht_inherit:,.2f} บาท")
        if tot_div_c > 0: st.write(f"- เครดิตภาษีปันผล: {tot_div_c:,.2f} บาท")
        st.success(f"**รวมภาษีที่จ่ายล่วงหน้าแล้ว:** {wht_total + wht_inherit + tot_div_c:,.2f} บาท")

    with b_col2:
        st.markdown("#### 2️⃣ สรุปค่าลดหย่อน")
        if t1 > 0: st.write(f"- หมวดครอบครัว: {t1:,.2f} บาท")
        if cap_life_hlth_A > 0: st.write(f"- ประกันชีวิต/สุขภาพ: {cap_life_hlth_A:,.2f} บาท")
        if cap_retire_A > 0: st.write(f"- กลุ่มเกษียณ (PVD+RMF+บำนาญ): {cap_retire_A:,.2f} บาท")
        if alw_tesg_A > 0: st.write(f"- ThaiESG: {alw_tesg_A:,.2f} บาท")
        if alw_soc_capped > 0: st.write(f"- ประกันสังคม: {alw_soc_capped:,.2f} บาท")
        if min(w_home, 100000) > 0: st.write(f"- ดอกเบี้ยบ้าน: {min(w_home, 100000):,.2f} บาท")
        if min(w_easy, 50000) > 0: st.write(f"- Easy E-Receipt: {min(w_easy, 50000):,.2f} บาท")
        st.info(f"**รวมค่าลดหย่อนทั้งหมด:** {tot_allowance_A:,.2f} บาท")
        
        st.markdown("#### 3️⃣ สรุปเงินบริจาค")
        if w_don_edu > 0: 
            st.write(f"- บริจาคการศึกษา/รพ. (x2): {min(w_don_edu * 2, net_pre_don_A * 0.1):,.2f} บาท")
            st.caption(f"*(จ่ายจริง {w_don_edu:,.0f} บาท)*")
        if w_don_gen > 0: st.write(f"- บริจาคทั่วไป: {min(w_don_gen, (net_pre_don_A - min(w_don_edu * 2, net_pre_don_A * 0.1)) * 0.1):,.2f} บาท")
        if w_don_pol > 0: st.write(f"- บริจาคพรรคการเมือง: {min(w_don_pol, 10000):,.2f} บาท")
        st.info(f"**รวมเงินบริจาคที่หักได้:** {don_A + min(w_don_pol, 10000):,.2f} บาท")

    # ==========================================
    # แสดงผลตารางสรุปสุดท้าย
    # ==========================================
    st.markdown("---")
    
    net_after_exp_label = "= เงินได้หลังหักค่าใช้จ่ายและยกเว้น" if self_exempt > 0 else "= เงินได้หลังหักค่าใช้จ่าย"
    
    # ต่อ String HTML แบบไร้รอยต่อ ป้องกัน Markdown Parser Error
    summary_html = f"""
    <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 15px; margin-top: 10px; border: 1px solid #dee2e6;">
        <tr style="background-color: #f8f9fa; font-weight: bold;"><td colspan="3" style="padding: 10px;">ตารางสรุปภาษี</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">+ เงินได้พึงประเมิน</td><td style="text-align: right; width: 150px; font-weight: bold;">{total_income:,.2f}</td><td style="width: 50px; padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ค่าใช้จ่าย</td><td style="text-align: right; font-weight: bold;">{exp_total:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>"""
    
    if self_exempt > 0:
        summary_html += f'\n        <tr><td style="padding: 5px 10px 5px 60px;">- เงินได้ยกเว้น (65ปี/คนพิการ)</td><td style="text-align: right; font-weight: bold;">{self_exempt:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>'

    summary_html += f"""
        <tr><td style="padding: 5px 10px 5px 60px; font-weight: bold;">{net_after_exp_label}</td><td style="text-align: right; font-weight: bold;">{inc_after_exp:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ค่าลดหย่อน</td><td style="text-align: right; font-weight: bold;">{tot_allowance_A:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- เงินบริจาค</td><td style="text-align: right; font-weight: bold;">{don_A + min(w_don_pol, 10000):,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr style="background-color: #cce5ff;"><td style="padding: 5px 10px 5px 60px; font-weight: bold;">= เงินได้สุทธิ</td><td style="text-align: right; font-weight: bold;">{net_inc_A:,.2f}</td><td style="padding-left: 10px; font-weight: bold;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">ภาษีที่ประเมิน</td><td style="text-align: right; font-weight: bold;">{tax_A:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ภาษีหัก ณ ที่จ่าย และ เครดิตปันผล</td><td style="text-align: right; font-weight: bold;">{wht_total + wht_inherit + tot_div_c:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr style="{final_class}"><td style="padding: 10px 10px 10px 60px; font-weight: bold;">{final_label}</td><td style="text-align: right; font-weight: bold; font-size: 18px;">{abs(final_tax_A):,.2f}</td><td style="padding-left: 10px; font-weight: bold;">บาท</td></tr>
    </table>
    <br>
    <h3 style='color:#343a40;'>📊 เปรียบเทียบผลการประหยัดภาษี (Scenario Analysis)</h3>
    <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; border: 1px solid #dee2e6;">
        <tr style="background-color: #e9ecef; font-weight: bold;">
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px; text-align: center;">ตารางอัตราภาษี</td>
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px; text-align: center;">เงินได้ในแต่ละขั้นภาษี</td>
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px; text-align: center;">ภาษีเงินได้</td>
        </tr>
        <tr style="background-color: #f8f9fa; font-weight: bold; text-align: center;">
            <td style="border: 1px solid #dee2e6; padding: 5px;">ขั้นเงินได้ (บาท)</td><td style="border: 1px solid #dee2e6; padding: 5px;">อัตรา</td>
            <td style="border: 1px solid #dee2e6; padding: 5px; color:#28a745;">มีการลงทุน</td><td style="border: 1px solid #dee2e6; padding: 5px; color:#dc3545;">ไม่มีการลงทุน</td>
            <td style="border: 1px solid #dee2e6; padding: 5px; color:#28a745;">มีการลงทุน</td><td style="border: 1px solid #dee2e6; padding: 5px; color:#dc3545;">ไม่มีการลงทุน</td>
        </tr>
        {bracket_html}
        <tr style="background-color: #cce5ff; font-weight: bold;">
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px; text-align: center;">รวม</td>
            <td style="border: 1px solid #dee2e6; padding: 10px; text-align: right;">{net_inc_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 10px; text-align: right;">{net_inc_B:,.2f}</td>
            <td style="border: 1px solid #dee2e6; padding: 10px; text-align: right; color:#28a745;">{tax_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 10px; text-align: right; color:#dc3545;">{tax_B:,.2f}</td>
        </tr>
        <tr style="background-color: #d4edda; font-weight: bold;">
            <td colspan="4" style="border: 1px solid #dee2e6; padding: 10px; text-align: left;">อัตราภาษีที่เสียที่แท้จริง (Effective Tax Rate)</td>
            <td style="border: 1px solid #dee2e6; padding: 10px; text-align: right; color:#155724;">{eff_A:.2f}%</td><td style="border: 1px solid #dee2e6; padding: 10px; text-align: right; color:#721c24;">{eff_B:.2f}%</td>
        </tr>
    </table>
    <div style="margin-top: 15px; padding: 15px; background-color: #fff3cd; border-left: 5px solid #ffc107; border-radius: 5px;">
        <h5 style="margin: 0 0 5px 0; color: #856404;">💡 สรุปความคุ้มค่าของการลงทุน:</h5>
        <span style="font-size: 15px; color: #212529;">การลงทุนใน RMF, ประกัน และ ThaiESG ช่วยให้คุณประหยัดภาษีไปได้ทั้งหมด <b><span style="color:#28a745;">฿{tax_B - tax_A:,.2f}</span></b></span>
    </div>
    """
    
    st.markdown(summary_html, unsafe_allow_html=True)

# ==========================================
# 5. โซน จัดการระบบ Save / Load ข้อมูล
# ==========================================
with st.sidebar:
    st.header("💾 จัดการข้อมูล (Draft)")
    st.markdown("สามารถบันทึกข้อมูลที่กรอกไว้เพื่อกลับมาทำต่อได้")
    
    st.markdown("---")
    st.subheader("📥 โหลดข้อมูล (Load)")
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ Draft (.json)", type="json")
    if uploaded_file is not None:
        if st.button("🔄 โหลดข้อมูลเข้าสู่ระบบ", use_container_width=True):
            data = json.load(uploaded_file)
            
            # โหลดข้อมูลตาราง
            for df_key in ['df_sal', 'df_agt', 'df_fa', 'df_rent', 'df_div']:
                if df_key in data:
                    st.session_state[df_key] = pd.DataFrame(data[df_key])
            
            # โหลดข้อมูลช่องกรอกตัวเลขและ Checkbox
            keys_to_load = [
                "inc_6", "wht_6", "inc_7", "wht_7", "inc_8", "wht_8",
                "inc_inv_1", "wht_inv_1", "inc_inv_2", "wht_inv_2", "inc_inv_3", "wht_inv_3",
                "inc_inv_4", "wht_inv_4", "inc_inv_5", "wht_inv_5", "inc_inv_6", "wht_inv_6",
                "inc_inherit", "wht_inherit", "inc_ex_1", "inc_ex_2", "inc_ex_3", "inc_ex_4",
                "w_is_65", "w_is_disabled_self", "w_spouse", "w_child_total", "w_child_after61", "w_child_adopt",
                "w_parent", "w_parent_hlth", "w_disable", "w_life", "w_hlth", "w_soc",
                "w_pvd", "w_rmf", "w_pension", "w_tesg", "w_home", "w_easy",
                "w_don_edu", "w_don_gen", "w_don_pol"
            ]
            for k in keys_to_load:
                if k in data:
                    st.session_state[k] = data[k]
                    
            st.success("✅ โหลดข้อมูลสำเร็จ!")
            st.rerun() # รีเฟรชหน้าจอเพื่อแสดงผลข้อมูลใหม่

    st.markdown("---")
    st.subheader("💾 บันทึกข้อมูล (Save)")
    
    # รวบรวมข้อมูลทั้งหมดที่กรอกล่าสุดเพื่อสร้างไฟล์ Save
    save_keys = [
        "inc_6", "wht_6", "inc_7", "wht_7", "inc_8", "wht_8",
        "inc_inv_1", "wht_inv_1", "inc_inv_2", "wht_inv_2", "inc_inv_3", "wht_inv_3",
        "inc_inv_4", "wht_inv_4", "inc_inv_5", "wht_inv_5", "inc_inv_6", "wht_inv_6",
        "inc_inherit", "wht_inherit", "inc_ex_1", "inc_ex_2", "inc_ex_3", "inc_ex_4",
        "w_is_65", "w_is_disabled_self", "w_spouse", "w_child_total", "w_child_after61", "w_child_adopt",
        "w_parent", "w_parent_hlth", "w_disable", "w_life", "w_hlth", "w_soc",
        "w_pvd", "w_rmf", "w_pension", "w_tesg", "w_home", "w_easy",
        "w_don_edu", "w_don_gen", "w_don_pol"
    ]
    
    save_data = {
        "df_sal": df_sal.to_dict(orient='records'),
        "df_agt": df_agt.to_dict(orient='records'),
        "df_fa": df_fa.to_dict(orient='records'),
        "df_rent": df_rent.to_dict(orient='records'),
        "df_div": df_div.to_dict(orient='records')
    }
    
    for k in save_keys:
        save_data[k] = st.session_state.get(k)
        
    json_str = json.dumps(save_data, indent=4)
    
    st.download_button(
        label="⬇️ ดาวน์โหลดไฟล์ Draft (JSON)", 
        data=json_str, 
        file_name="SmartTax_Draft.json", 
        mime="application/json", 
        use_container_width=True
    )
