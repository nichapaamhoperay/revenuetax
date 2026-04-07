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
tabs = st.tabs(['💰 เงินเดือน (40(1))', '🛡️ ค่าคอมมิชชัน (40(2))', '📈 ค่าตอบแทน FA (40(2))', '🏠 ค่าเช่าบ้าน (40(5))', '📊 เงินปันผล'])
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# เตรียมตารางข้อมูลเริ่มต้น
if 'df_sal' not in st.session_state:
    st.session_state.df_sal = pd.DataFrame({"เดือน": months, "รายได้": [150000]*12, "หัก ณ ที่จ่าย": [5000]*12})
    st.session_state.df_agt = pd.DataFrame({"เดือน": months, "รายได้": [0]*12, "หัก ณ ที่จ่าย": [0]*12})
    st.session_state.df_fa = pd.DataFrame({"เดือน": months, "รายได้": [0]*12, "หัก ณ ที่จ่าย": [0]*12})
    st.session_state.df_rent = pd.DataFrame({"เดือน": months, "รายได้": [25000]*12, "หัก ณ ที่จ่าย": [0]*12})
    
    div_data = [["KBANK", 20, 5000.0, 0.0, 0.0, 500.0]] + [["", 0, 0.0, 0.0, 0.0, 0.0] for _ in range(9)]
    st.session_state.df_div = pd.DataFrame(div_data, columns=["ชื่อหลักทรัพย์", "อัตราภาษี(%)", "เงินปันผล", "ไม่ได้รับเครดิต", "ยกเว้นภาษี", "หัก ณ ที่จ่าย"])

# ฟังก์ชันตารางแบบแก้ไขได้
config = {"เดือน": st.column_config.TextColumn(disabled=True)}

with tabs[0]: 
    df_sal = st.data_editor(st.session_state.df_sal, use_container_width=True, hide_index=True, column_config=config, key="editor_sal")
    st.info(f"**รวมเงินเดือน:** {df_sal['รายได้'].sum():,.2f} บาท | **รวมภาษีหัก ณ ที่จ่าย:** {df_sal['หัก ณ ที่จ่าย'].sum():,.2f} บาท")

with tabs[1]: 
    df_agt = st.data_editor(st.session_state.df_agt, use_container_width=True, hide_index=True, column_config=config, key="editor_agt")
    st.info(f"**รวมค่าคอมมิชชัน:** {df_agt['รายได้'].sum():,.2f} บาท | **รวมภาษีหัก ณ ที่จ่าย:** {df_agt['หัก ณ ที่จ่าย'].sum():,.2f} บาท")

with tabs[2]: 
    df_fa  = st.data_editor(st.session_state.df_fa, use_container_width=True, hide_index=True, column_config=config, key="editor_fa")
    st.info(f"**รวมค่าตอบแทน FA:** {df_fa['รายได้'].sum():,.2f} บาท | **รวมภาษีหัก ณ ที่จ่าย:** {df_fa['หัก ณ ที่จ่าย'].sum():,.2f} บาท")

with tabs[3]: 
    df_rent = st.data_editor(st.session_state.df_rent, use_container_width=True, hide_index=True, column_config=config, key="editor_rent")
    st.info(f"**รวมค่าเช่าบ้าน:** {df_rent['รายได้'].sum():,.2f} บาท | **รวมภาษีหัก ณ ที่จ่าย:** {df_rent['หัก ณ ที่จ่าย'].sum():,.2f} บาท")

with tabs[4]: 
    st.markdown("💡 *กรอกอัตราภาษีและเงินปันผล ระบบจะคำนวณเครดิตให้ตอนกดประมวลผลค่ะ*")
    df_div = st.data_editor(st.session_state.df_div, use_container_width=True, hide_index=True, key="editor_div")
    tot_div_amt = pd.to_numeric(df_div["เงินปันผล"], errors='coerce').sum()
    tot_div_wht = pd.to_numeric(df_div["หัก ณ ที่จ่าย"], errors='coerce').sum()
    st.info(f"**รวมเงินปันผล:** {tot_div_amt:,.2f} บาท | **รวมภาษีหัก ณ ที่จ่าย:** {tot_div_wht:,.2f} บาท")

# ==========================================
# 2. โซนกราฟ (Live Chart)
# ==========================================
st.header("2. กราฟสรุปรายได้รายเดือน")
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
ded_tabs = st.tabs(['1. ครอบครัว', '2. ประกัน/ลงทุน', '3. ดอกเบี้ยบ้าน', '4. E-Receipt', '5. บริจาค'])

with ded_tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        w_self = st.number_input("ลดหย่อนผู้มีเงินได้ (60,000 บาท)", value=60000, disabled=True)
        w_spouse = st.checkbox("คู่สมรสไม่มีรายได้ (60,000 บาท)")
        w_child_total = st.number_input("จำนวนบุตรทั้งหมด", min_value=0, value=2)
        w_child_after61 = st.number_input("บุตรที่เกิดปี 2561 เป็นต้นไป", min_value=0, value=2)
        w_child_adopt = st.number_input("จำนวนบุตรบุญธรรม", min_value=0, value=0)
    with c2:
        w_parent = st.number_input("เลี้ยงดูบิดามารดา (คนละ 30k)", min_value=0, max_value=4, value=0)
        w_parent_hlth = st.number_input("เบี้ยประกันสุขภาพบิดามารดา (Max 15k)", min_value=0, value=0, step=1000)
        w_disable = st.number_input("เลี้ยงดูคนพิการ (คนละ 60k)", min_value=0, value=0)
    
    alw_child = 0
    if w_child_total > 0:
        if w_child_total == w_child_after61: alw_child = 30000 + max(0, (w_child_after61 - 1) * 60000)
        else: alw_child = (max(0, w_child_total - w_child_after61) * 30000) + (w_child_after61 * 60000)
    t1 = 60000 + (60000 if w_spouse else 0) + alw_child + (min(w_parent, 4) * 30000) + min(w_parent_hlth, 15000) + (w_disable * 60000)
    st.success(f"**รวมมูลค่าลดหย่อนหมวดครอบครัว:** {t1:,.0f} บาท")

with ded_tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        w_life = st.number_input("ประกันชีวิตทั่วไป (Max 100k)", min_value=0, value=100000, step=5000)
        w_hlth = st.number_input("ประกันสุขภาพ (Max 25k)", min_value=0, value=25000, step=1000)
        w_soc = st.number_input("ประกันสังคม (Max 9k)", min_value=0, value=9000, step=500)
    with c2:
        st.markdown("**กลุ่มเกษียณ (รวมกันไม่เกิน 500,000)**")
        w_pvd = st.number_input("Provident Fund (PVD)", min_value=0, value=120000, step=5000)
        w_rmf = st.number_input("กองทุน RMF", min_value=0, value=50000, step=5000)
        w_pension = st.number_input("ประกันชีวิตแบบบำนาญ", min_value=0, value=0, step=5000)
        st.markdown("**แยกวงเงิน**")
        w_tesg = st.number_input("กองทุน ThaiESG (Max 300k)", min_value=0, value=30000, step=5000)
    
    t2_sum = w_life + w_hlth + w_pension + w_pvd + w_rmf + w_tesg + w_soc
    st.info(f"**ยอดลงทุนรวม (รอคำนวณเพดาน):** {t2_sum:,.0f} บาท")

with ded_tabs[2]: 
    w_home = st.number_input("ดอกเบี้ยบ้าน (Max 100k)", min_value=0, value=100000, step=5000)
    st.info(f"**ดอกเบี้ยบ้าน:** {w_home:,.0f} บาท")

with ded_tabs[3]: 
    w_easy = st.number_input("Easy E-Receipt (Max 50k)", min_value=0, value=0, step=1000)
    st.info(f"**ยอด E-Receipt:** {w_easy:,.0f} บาท")

with ded_tabs[4]:
    c1, c2 = st.columns(2)
    with c1:
        w_don_edu = st.number_input("บริจาคการศึกษา/รพ. (ได้ x2)", min_value=0, value=0, step=1000)
        w_don_gen = st.number_input("บริจาคทั่วไป", min_value=0, value=10000, step=1000)
    with c2:
        w_don_pol = st.number_input("บริจาคพรรคการเมือง (Max 10k)", min_value=0, value=0, step=500)
    
    t5_sum = w_don_edu + w_don_gen + w_don_pol
    st.info(f"**ยอดบริจาค (รอคำนวณเพดาน):** {t5_sum:,.0f} บาท")

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
    wht_base = wht_1 + wht_2 + wht_5
    
    tot_div_a = tot_div_c = tot_div_w = 0
    for _, row in df_div.iterrows():
        rate = pd.to_numeric(row["อัตราภาษี(%)"], errors='coerce')
        amt = pd.to_numeric(row["เงินปันผล"], errors='coerce')
        wht = pd.to_numeric(row["หัก ณ ที่จ่าย"], errors='coerce')
        if pd.notna(rate) and pd.notna(amt) and 0 < rate < 100 and amt > 0:
            tot_div_c += amt * (rate / (100.0 - rate))
        tot_div_a += (amt if pd.notna(amt) else 0)
        tot_div_w += (wht if pd.notna(wht) else 0)
    
    total_income = inc_1 + inc_2 + inc_5 + tot_div_a + tot_div_c
    
    # คำนวณค่าใช้จ่าย
    exp_1_2 = min((inc_1 + inc_2) * 0.5, 100000)
    exp_5 = inc_5 * 0.3
    exp_total = exp_1_2 + exp_5
    inc_after_exp = total_income - exp_total

    # Scenario A (ลงทุน)
    cap_life_hlth_A = min(w_life + min(w_hlth, 25000), 100000)
    alw_pension_A = min(w_pension, total_income * 0.15, 200000)
    alw_pvd_A = min(w_pvd, total_income * 0.15, 500000)
    alw_rmf_A = min(w_rmf, total_income * 0.30, 500000)
    cap_retire_A = min(alw_pension_A + alw_pvd_A + alw_rmf_A, 500000)
    alw_tesg_A = min(w_tesg, total_income * 0.30, 300000)
    alw_soc_capped = min(w_soc, 9000)
    alw_home_capped = min(w_home, 100000)
    alw_easy_capped = min(w_easy, 50000)
    alw_pol_capped = min(w_don_pol, 10000)
    
    tot_allowance_A = t1 + alw_soc_capped + alw_home_capped + alw_easy_capped + cap_life_hlth_A + cap_retire_A + alw_tesg_A
    net_pre_don_A = max(0, inc_after_exp - tot_allowance_A - alw_pol_capped)
    
    don_edu_calc = min(w_don_edu * 2, net_pre_don_A * 0.1)
    don_gen_calc = min(w_don_gen, (net_pre_don_A - don_edu_calc) * 0.1)
    don_A = don_edu_calc + don_gen_calc
    net_inc_A = net_pre_don_A - don_A

    # Scenario B (ไม่ลงทุน)
    tot_allowance_B = t1 + alw_soc_capped + alw_home_capped + alw_easy_capped + min(w_pvd, total_income * 0.15, 500000)
    net_pre_don_B = max(0, inc_after_exp - tot_allowance_B - alw_pol_capped)
    don_B = min(w_don_edu * 2, net_pre_don_B * 0.1) + min(w_don_gen, (net_pre_don_B - min(w_don_edu * 2, net_pre_don_B * 0.1)) * 0.1)
    net_inc_B = net_pre_don_B - don_B

    # คิดภาษี
    tax_A = tax_B = prev = 0
    rem_A, rem_B = net_inc_A, net_inc_B
    bracket_html = ""
    for lim, rate in [(150000, 0), (300000, 0.05), (500000, 0.1), (750000, 0.15), (1000000, 0.2), (2000000, 0.25), (5000000, 0.3), (float('inf'), 0.35)]:
        t_A, t_B = max(0, min(rem_A, lim - prev)), max(0, min(rem_B, lim - prev))
        tax_in_A, tax_in_B = t_A * rate, t_B * rate
        tax_A += tax_in_A; tax_B += tax_in_B
        if t_B > 0 or t_A > 0 or lim == 150000:
            lim_text = f"{lim:,.0f}" if lim != float('inf') else ""
            bracket_html += f'<tr style="text-align: right;"><td style="border: 1px solid #dee2e6; padding: 5px;">{lim_text}</td><td style="border: 1px solid #dee2e6; padding: 5px;">{rate*100:.2f}%</td><td style="border: 1px solid #dee2e6; padding: 5px;">{t_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px;">{t_B:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px;">{tax_in_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 5px;">{tax_in_B:,.2f}</td></tr>'
        rem_A -= t_A; rem_B -= t_B; prev = lim
        if rem_A <= 0 and rem_B <= 0 and lim > net_inc_B: break

    wht_total = wht_base + tot_div_w
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
        if inc_1 > 0: st.write(f"- **เงินเดือน 40(1):** {inc_1:,.2f} บาท")
        if inc_2 > 0: st.write(f"- **ค่าตอบแทน 40(2):** {inc_2:,.2f} บาท")
        if inc_1 > 0 or inc_2 > 0: st.caption(f"  *หักค่าใช้จ่าย 40(1)+(2) ได้:* {exp_1_2:,.2f} บาท")
        
        if inc_5 > 0: 
            st.write(f"- **ค่าเช่า 40(5):** {inc_5:,.2f} บาท")
            st.caption(f"  *หักค่าใช้จ่าย 40(5) (30%):* {exp_5:,.2f} บาท")
            
        if tot_div_a > 0:
            st.write(f"- **เงินปันผล 40(4):** {tot_div_a:,.2f} บาท")
            st.write(f"- **เครดิตภาษีปันผล:** {tot_div_c:,.2f} บาท")
            
        st.info(f"**รวมเงินได้พึงประเมิน:** {total_income:,.2f} บาท\n\n**รวมค่าใช้จ่ายที่หักได้:** {exp_total:,.2f} บาท")
        
        st.markdown("#### 4️⃣ ภาษีหัก ณ ที่จ่าย และ เครดิตปันผล")
        if wht_1 > 0: st.write(f"- หัก ณ ที่จ่าย 40(1): {wht_1:,.2f} บาท")
        if wht_2 > 0: st.write(f"- หัก ณ ที่จ่าย 40(2): {wht_2:,.2f} บาท")
        if wht_5 > 0: st.write(f"- หัก ณ ที่จ่าย 40(5): {wht_5:,.2f} บาท")
        if tot_div_w > 0: st.write(f"- หัก ณ ที่จ่าย ปันผล: {tot_div_w:,.2f} บาท")
        if tot_div_c > 0: st.write(f"- เครดิตภาษีปันผล: {tot_div_c:,.2f} บาท")
        st.success(f"**รวมภาษีที่จ่ายล่วงหน้าแล้ว:** {wht_total + tot_div_c:,.2f} บาท")

    with b_col2:
        st.markdown("#### 2️⃣ สรุปค่าลดหย่อน")
        if t1 > 0: st.write(f"- หมวดครอบครัว: {t1:,.2f} บาท")
        if cap_life_hlth_A > 0: st.write(f"- ประกันชีวิต/สุขภาพ: {cap_life_hlth_A:,.2f} บาท")
        if cap_retire_A > 0: st.write(f"- กลุ่มเกษียณ (PVD+RMF+บำนาญ): {cap_retire_A:,.2f} บาท")
        if alw_tesg_A > 0: st.write(f"- ThaiESG: {alw_tesg_A:,.2f} บาท")
        if alw_soc_capped > 0: st.write(f"- ประกันสังคม: {alw_soc_capped:,.2f} บาท")
        if alw_home_capped > 0: st.write(f"- ดอกเบี้ยบ้าน: {alw_home_capped:,.2f} บาท")
        if alw_easy_capped > 0: st.write(f"- Easy E-Receipt: {alw_easy_capped:,.2f} บาท")
        st.info(f"**รวมค่าลดหย่อนทั้งหมด:** {tot_allowance_A:,.2f} บาท")
        
        st.markdown("#### 3️⃣ สรุปเงินบริจาค")
        if w_don_edu > 0: 
            st.write(f"- บริจาคการศึกษา/รพ. (x2): {don_edu_calc:,.2f} บาท")
            st.caption(f"*(จ่ายจริง {w_don_edu:,.0f} บาท)*")
        if w_don_gen > 0: st.write(f"- บริจาคทั่วไป: {don_gen_calc:,.2f} บาท")
        if w_don_pol > 0: st.write(f"- บริจาคพรรคการเมือง: {alw_pol_capped:,.2f} บาท")
        st.info(f"**รวมเงินบริจาคที่หักได้:** {don_A + alw_pol_capped:,.2f} บาท")

    # ==========================================
    # แสดงผลตารางสรุปสุดท้าย
    # ==========================================
    st.markdown("---")
    st.markdown(f"""
    <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 15px; margin-top: 10px; border: 1px solid #dee2e6;">
        <tr style="background-color: #f8f9fa; font-weight: bold;"><td colspan="3" style="padding: 10px;">ตารางสรุปภาษี</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">+ เงินได้พึงประเมิน</td><td style="text-align: right; width: 150px; font-weight: bold;">{total_income:,.2f}</td><td style="width: 50px; padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ค่าใช้จ่าย</td><td style="text-align: right; font-weight: bold;">{exp_total:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px; font-weight: bold;">= เงินได้หลังหักค่าใช้จ่าย</td><td style="text-align: right; font-weight: bold;">{inc_after_exp:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ค่าลดหย่อน</td><td style="text-align: right; font-weight: bold;">{tot_allowance_A:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- เงินบริจาค</td><td style="text-align: right; font-weight: bold;">{don_A + alw_pol_capped:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr style="background-color: #cce5ff;"><td style="padding: 5px 10px 5px 60px; font-weight: bold;">= เงินได้สุทธิ</td><td style="text-align: right; font-weight: bold;">{net_inc_A:,.2f}</td><td style="padding-left: 10px; font-weight: bold;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">ภาษีที่ประเมิน</td><td style="text-align: right; font-weight: bold;">{tax_A:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr><td style="padding: 5px 10px 5px 60px;">- ภาษีหัก ณ ที่จ่าย และ เครดิตปันผล</td><td style="text-align: right; font-weight: bold;">{wht_total + tot_div_c:,.2f}</td><td style="padding-left: 10px;">บาท</td></tr>
        <tr style="{final_class}"><td style="padding: 10px 10px 10px 60px; font-weight: bold;">{final_label}</td><td style="text-align: right; font-weight: bold; font-size: 18px;">{abs(final_tax_A):,.2f}</td><td style="padding-left: 10px; font-weight: bold;">บาท</td></tr>
    </table>
    <br>
    <h3 style='color:#343a40;'>📊 เปรียบเทียบผลการประหยัดภาษี (Scenario Analysis)</h3>
    <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; border: 1px solid #dee2e6;">
        <tr style="background-color: #e9ecef; text-align: center; font-weight: bold;">
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px;">ตารางอัตราภาษี</td>
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px;">เงินได้ในแต่ละขั้นภาษี</td>
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px;">ภาษีเงินได้</td>
        </tr>
        <tr style="background-color: #f8f9fa; text-align: center; font-weight: bold;">
            <td style="border: 1px solid #dee2e6; padding: 5px;">ขั้นเงินได้ (บาท)</td><td style="border: 1px solid #dee2e6; padding: 5px;">อัตรา</td>
            <td style="border: 1px solid #dee2e6; padding: 5px; color:#28a745;">มีการลงทุน</td><td style="border: 1px solid #dee2e6; padding: 5px; color:#dc3545;">ไม่มีการลงทุน</td>
            <td style="border: 1px solid #dee2e6; padding: 5px; color:#28a745;">มีการลงทุน</td><td style="border: 1px solid #dee2e6; padding: 5px; color:#dc3545;">ไม่มีการลงทุน</td>
        </tr>
        {bracket_html}
        <tr style="background-color: #cce5ff; font-weight: bold; text-align: right;">
            <td colspan="2" style="border: 1px solid #dee2e6; padding: 10px; text-align: center;">รวม</td>
            <td style="border: 1px solid #dee2e6; padding: 10px;">{net_inc_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 10px;">{net_inc_B:,.2f}</td>
            <td style="border: 1px solid #dee2e6; padding: 10px; color:#28a745;">{tax_A:,.2f}</td><td style="border: 1px solid #dee2e6; padding: 10px; color:#dc3545;">{tax_B:,.2f}</td>
        </tr>
        <tr style="background-color: #d4edda; font-weight: bold; text-align: right;">
            <td colspan="4" style="border: 1px solid #dee2e6; padding: 10px; text-align: left;">อัตราภาษีที่เสียที่แท้จริง (Effective Tax Rate)</td>
            <td style="border: 1px solid #dee2e6; padding: 10px; color:#155724;">{eff_A:.2f}%</td><td style="border: 1px solid #dee2e6; padding: 10px; color:#721c24;">{eff_B:.2f}%</td>
        </tr>
    </table>
    <div style="margin-top: 15px; padding: 15px; background-color: #fff3cd; border-left: 5px solid #ffc107; border-radius: 5px;">
        <h5 style="margin: 0 0 5px 0; color: #856404;">💡 สรุปความคุ้มค่าของการลงทุน:</h5>
        <span style="font-size: 15px; color: #212529;">การลงทุนใน RMF, ประกัน และ ThaiESG ช่วยให้คุณประหยัดภาษีไปได้ทั้งหมด <b><span style="color:#28a745;">฿{tax_B - tax_A:,.2f}</span></b></span>
    </div>
    """, unsafe_allow_html=True)
