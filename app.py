import streamlit as st
from lunar_python import Solar, Lunar
import pandas as pd
import datetime

# --- 1. 頁面設定 ---
st.set_page_config(page_title="五行分析與水晶推薦", layout="centered")

# --- 2. 樣式 ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    .block-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 數據 ---
STEM_5 = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
BRANCH_5 = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
CRYSTAL = {
    "金": "【白水晶、鈦金】可提升果斷力與純淨能量。",
    "木": "【綠幽靈、綠髮晶】有助於事業成長與生機。",
    "水": "【黑曜石、海藍寶】能增強靈活性與情緒流動。",
    "火": "【紫水晶、紅石榴石】可帶動熱情與行動力。",
    "土": "【黃水晶、虎眼石】有助於穩定情緒與聚財。"
}

# --- 4. 封面 ---
try:
    st.image("cover.jpg", use_container_width=True)
except:
    pass

st.title("🌌 五行命盤查詢參考")

# --- 5. 輸入表單 ---
with st.form("my_form"):
    d = st.date_input("出生日期", value=datetime.date(1981, 1, 7), min_value=datetime.date(1900, 1, 1))
    t = st.time_input("出生時間", value=datetime.time(12, 0))
    submitted = st.form_submit_button("開始計算")

# --- 6. 運算與結果 ---
if submitted:
    try:
        solar = Solar.fromYmdHms(d.year, d.month, d.day, t.hour, t.minute, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        
        # 修正：將八字提取拆解開來，避免長括號導致報錯
        bz = []
        bz.append(ec.getYearGan())
        bz.append(ec.getYearZhi())
        bz.append(ec.getMonthGan())
        bz.append(ec.getMonthZhi())
        bz.append(ec.getDayGan())
        bz.append(ec.getDayZhi())
        bz.append(ec.getTimeGan())
        bz.append(ec.getTimeZhi())
        
        stats = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for char in bz:
            if char in STEM_5: stats[STEM_5[char]] += 1
            if char in BRANCH_5: stats[BRANCH_5[char]] += 1

        st.divider()
        st.write(f"### 您的八字：{' '.join(bz)}")
        
        df = pd.DataFrame(list(stats.items()), columns=['五行', '數量'])
        st.bar_chart(df.set_index('五行'))

        missing = [k for k, v in stats.items() if v == 0]
        if missing:
            st.warning(f"您的命盤中缺少：{', '.join(missing)}")
            for m in missing:
                st.info(f"🔮 **補【{m}】水晶推薦：**\n{CRYSTAL[m]}")
        else:
            st.success("太棒了!您的五行平衡，什麼都不缺！")

    except Exception as e:
        st.error(f"發生錯誤：{e}")

st.caption("僅供參考，請勿過度迷信。")
