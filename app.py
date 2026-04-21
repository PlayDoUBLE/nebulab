import streamlit as st
from lunar_python import Solar, Lunar
import pandas as pd
import datetime

st.set_page_config(page_title="五行分析", layout="centered")

STEM_5 = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
BRANCH_5 = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}


st.markdown("""
    <style>
    /* 修改整體背景顏色為淡灰色 */
    .stApp {
        background-color: #F0F2F6;
    }
    
    /* 修改中間內容區塊的背景（選擇性，讓內容稍微浮現） */
    .block-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)



# 1. 頁面設定
st.set_page_config(page_title="五行分析", layout="centered")

# 2. 加上封面橫幅 (新增這行)
# use_container_width=True 會讓圖片自動填滿網頁寬度
st.image("cover.jpg", use_container_width=True)

st.title("🌌 五行命盤查詢參考")

with st.form("my_form"):
    d = st.date_input(
        "出生日期", 
        value=datetime.date(1981, 1, 7), 
        min_value=datetime.date(1900, 1, 1), 
        max_value=datetime.date(2100, 12, 31)
    )
    t = st.time_input("出生時間", value=datetime.time(12, 0))
    submitted = st.form_submit_button("開始計算")

if submitted:
    try:
        solar = Solar.fromYmdHms(d.year, d.month, d.day, t.hour, t.minute, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        
        bz = [
            eight_char.getYearGan(), eight_char.getYearZhi(),
            eight_char.getMonthGan(), eight_char.getMonthZhi(),
            eight_char.getDayGan(), eight_char.getDayZhi(),
            eight_char.getTimeGan(), eight_char.getTimeZhi()
        ]
        
        stats = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for char in bz:
            if char in STEM_5: stats[STEM_5[char]] += 1
            if char in BRANCH_5: stats[BRANCH_5[char]] += 1

        st.write(f"### 您的八字：{' '.join(bz)}")
        
        df = pd.DataFrame(list(stats.items()), columns=['五行', '數量'])
        st.bar_chart(df.set_index('五行'))

        missing = [k for k, v in stats.items() if v == 0]
        if missing:
            st.warning(f"您的命盤中缺少：{', '.join(missing)}")
        else:
            st.success("您的五行平衡，什麼都不缺！")

    except Exception as e:
        st.error(f"發生錯誤：{e}")

st.caption("僅供參考，請勿過度迷信。")