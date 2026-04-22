import streamlit as st
from lunar_python import Solar, Lunar
import datetime
import base64

# --- 1. 頁面設定 ---
st.set_page_config(page_title="五行分析與水晶推薦", layout="centered")

# --- 2. 核心樣式設定 ---
st.markdown("""
<style>
    .stApp { background-color: #F0F2F6; }
    .block-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 五行與水晶數據定義 ---
STEM_5 = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
BRANCH_5 = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
WUXING_CONFIG = {
    "金": {"color": "#FFD700", "advice": "【白水晶、鈦金】可提升果斷力與純淨能量。"},
    "木": {"color": "#138b6d", "advice": "【綠幽靈、綠髮晶】有助於事業成長與生機。"},
    "水": {"color": "#ADD8E6", "advice": "【黑曜石、海藍寶】能增強靈活性與情緒流動。"},
    "火": {"color": "#FF0000", "advice": "【紫水晶、紅石榴石】可帶動熱情與行動力。"},
    "土": {"color": "#FF8C00", "advice": "【黃水晶、虎眼石】有助於穩定情緒與聚財。"}
}

# --- 4. 封面區塊 (支援點擊圖片跳轉 IG) ---
ig_url = "https://www.instagram.com/nebulab.crystals/"
try:
    with open("cover.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    img_html = f'<a href="{ig_url}" target="_blank"><img src="data:image/jpeg;base64,{data}" style="width:100%; border-radius:10px; cursor:pointer; margin-bottom:20px;"></a>'
    st.markdown(img_html, unsafe_allow_html=True)
except Exception:
    st.markdown(f"### 🌌 [Nebulab Crystals]({ig_url})")

st.title("🌌 五行命盤查詢參考")

# --- 5. 輸入表單 ---
with st.form("user_input_form"):
    d = st.date_input("出生日期", value=datetime.date(1981, 1, 7),min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2026, 1, 7))
    t = st.time_input("出生時間", value=datetime.time(12, 0))
    submitted = st.form_submit_button("查詢")

# --- 6. 計算與結果呈現 ---
if submitted:
    try:
        # A. 八字運算 (修正點就在這裡：getEightChar())
        solar = Solar.fromYmdHms(d.year, d.month, d.day, t.hour, t.minute, 0)
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        bz = [ec.getYearGan(), ec.getYearZhi(), ec.getMonthGan(), ec.getMonthZhi(),
              ec.getDayGan(), ec.getDayZhi(), ec.getTimeGan(), ec.getTimeZhi()]
        
        # B. 五行統計
        stats = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        for char in bz:
            if char in STEM_5: stats[STEM_5[char]] += 1
            if char in BRANCH_5: stats[BRANCH_5[char]] += 1

        st.divider()
        st.subheader(f"您的八字：{' '.join(bz)}")
        
        # C. 繪製五行能量圖表
        st.write("#### 五行衰旺指數對比：")
        for el in ["金", "木", "水", "火", "土"]:
            val = stats[el]
            pct = (val / 8) * 100
            clr = WUXING_CONFIG[el]["color"]
            label = f'<div style="display:flex;justify-content:space-between;font-weight:bold;margin-top:10px;"><span>{el}</span><span>{val}</span></div>'
            bar = f'<div style="background-color:#eee;border-radius:10px;width:100%;height:20px;"><div style="background-color:{clr};width:{pct}%;height:100%;border-radius:10px;"></div></div>'
            st.markdown(label, unsafe_allow_html=True)
            st.markdown(bar, unsafe_allow_html=True)

        # D. 水晶建議
        st.write("")
        missing = [k for k, v in stats.items() if v == 0]
        if missing:
            st.warning(f"您的命盤中缺少：{'、'.join(missing)}")
            for m in missing:
                st.info(f"🔮 **補【{m}】水晶推薦：**\n{WUXING_CONFIG[m]['advice']}")
        else:
            st.success("您的五行平衡，什麼都不缺！但建議配戴水晶可進一步提升氣場喔！")
            
    except Exception as e:
        st.error(f"計算過程出錯：{e}")

# --- 7. 頁尾 ---
st.divider()
st.caption("僅供參考，請勿過度迷信。")
st.markdown(f"🔗 **挑選適合的水晶請洽 [Nebulab.Crystals]({"http://ig.me/m/nebulab.crystals"})**")
