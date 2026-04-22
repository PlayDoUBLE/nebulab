import streamlit as st
from lunar_python import Solar, Lunar
import datetime
import base64

# --- 1. 頁面設定 ---
st.set_page_config(page_title="Nebulab 水晶五行分析", page_icon="🌌", layout="centered")

# --- 2. 核心樣式 ---
st.markdown("""
<style>
    .stApp { background-color: #F0F2F6; }
    .block-container { background-color: #ffffff; padding: 3rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    #MainMenu, footer, header {visibility: hidden;}
    .stAppDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# --- 3. 數據定義 ---
STEM_5 = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
BRANCH_5 = {"寅":"木","卯":"木","巳":"火","午":"火","申":"金","酉":"金","亥":"水","子":"水","辰":"土","戌":"土","丑":"土","未":"土"}
ZODIAC = {"子":"鼠","丑":"牛","寅":"虎","卯":"兔","辰":"龍","巳":"蛇","午":"馬","未":"羊","申":"猴","酉":"雞","戌":"狗","亥":"豬"}

WUXING_CONFIG = {
    "金": {"color": "#FFD700", "advice": "【白水晶、鈦金】可提升果斷力與純淨能量。"},
    "木": {"color": "#138b6d", "advice": "【綠幽靈、綠髮晶】有助於事業成長與生機。"},
    "水": {"color": "#ADD8E6", "advice": "【黑曜石、海藍寶】能增強靈活性與情緒流動。"},
    "火": {"color": "#FF0000", "advice": "【紫水晶、紅石榴石】可帶動熱情與行動力。"},
    "土": {"color": "#FF8C00", "advice": "【黃水晶、虎眼石】有助於穩定情緒與聚財。"}
}

LIFE_NUM_DATA = {
    1: {"type": "開創領導類", "trait": "獨立、果斷、具領導力，但易流於自我中心。", "crystal": "鈦金、黃水晶"},
    2: {"type": "溝通合作類", "trait": "溫和、敏感、善於合作，但易猶豫不決。", "crystal": "海藍寶、月光石"},
    3: {"type": "創意表達類", "trait": "聰明、活潑、充滿創意，但易缺乏耐心。", "crystal": "紫水晶、粉晶"},
    4: {"type": "穩定執行類", "trait": "務實、穩重、守規矩，但易過於固執。", "crystal": "綠幽靈、黑曜石"},
    5: {"type": "自由冒險類", "trait": "嚮往自由、口才好，但易心浮氣躁。", "crystal": "白水晶、天河石"},
    6: {"type": "奉獻療癒類", "trait": "追求完美、熱情慷慨，但易承擔壓力。", "crystal": "拉長石、紅紋石"},
    7: {"type": "真理探索類", "trait": "愛思考、分析力強，但易生疑心病。", "crystal": "青金石、舒俱徠"},
    8: {"type": "權力回饋類", "trait": "具備商業頭腦、注重效率，但易過於現實。", "crystal": "金髮晶、虎眼石"},
    9: {"type": "夢想大愛類", "trait": "慈悲、想像力豐富，但易流於空想。", "crystal": "煙晶、黑髮晶"}
}

# --- 4. 封面 ---
ig_url = "https://www.instagram.com/nebulab.crystals/"
try:
    with open("cover.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f'<a href="{ig_url}" target="_blank"><img src="data:image/jpeg;base64,{data}" style="width:100%; border-radius:10px; margin-bottom:20px;"></a>', unsafe_allow_html=True)
except:
    st.markdown(f"### 🌌 [Nebulab Crystals]({ig_url})")

st.title("🌌 五行命盤與生命靈數分析")

# --- 5. 輸入 ---
with st.form("user_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        d = st.date_input("出生日期", value=datetime.date(1981, 1, 7))
    with col2:
        t = st.time_input("出生時間", value=datetime.time(12, 0))
    submitted = st.form_submit_button("開始分析")

# --- 6. 運算與呈現 ---
if submitted:
    try:
        # A. 靈數
        s_date = d.strftime("%Y%m%d")
        total = sum(int(n) for n in s_date)
        while total > 9: 
            total = sum(int(n) for n in str(total))
        info = LIFE_NUM_DATA[total]

        # B. 八字
        sol = Solar.fromYmdHms(d.year, d.month, d.day, t.hour, t.minute, 0)
        lun = sol.getLunar()
        ec = lun.getEightChar()
        
        # C. 五行統計
        bz = [ec.getYearGan(), ec.getYearZhi(), ec.getMonthGan(), ec.getMonthZhi(),
              ec.getDayGan(), ec.getDayZhi(), ec.getTimeGan(), ec.getTimeZhi()]
        stats = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        for c in bz:
            if c in STEM_5: stats[STEM_5[c]] += 1
            if c in BRANCH_5: stats[BRANCH_5[c]] += 1

        # D. 顯示結果
        st.divider()
        st.write(f"🎂 **陽曆：** {d.year}/{d.month}/{d.day} {t.hour}:{t.minute} ({ZODIAC.get(ec.getYearZhi())})")
        st.write(f"📜 **八字：** {ec.getYearGan()}{ec.getYearZhi()} {ec.getMonthGan()}{ec.getMonthZhi()} {ec.getDayGan()}{ec.getDayZhi()} {ec.getTimeGan()}{ec.getTimeZhi()}")
        st.write(f"🔢 **生命靈數：{total} 號人** ({info['type']})")
        st.info(f"💡 **性格：** {info['trait']}")
        
        # E. 圖表
        st.write("#### 📊 五行分佈：")
        for el in ["金", "木", "水", "火", "土"]:
            v = stats[el]
            p = (v / 8) * 100
            c = WUXING_CONFIG[el]["color"]
            st.markdown(f'<div style="display:flex;justify-content:space-between;"><b>{el}</b><b>{v}</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:#eee;width:100%;height:15px;border-radius:10px;"><div style="background:{c};width:{p}%;height:100%;border-radius:10px;"></div></div>', unsafe_allow_html=True)

        # F. 建議
        st.write("#### 🔮 能量平衡建議：")
        m = [k for k, v in stats.items() if v == 0]
        
        # --- 五行建議 ---
        if m:
            st.warning(f"⚠️ **五行缺失補足：** 缺少【{'、'.join(m)}】")
            for x in m: 
                st.info(f"✨ **{x}：** {WUXING_CONFIG[x]['advice']}")
        else:
            st.success("✅ **您的五行平衡，什麼都不缺！但建議配戴水晶可進一步提升氣場喔！")
        
        # --- 靈數建議 ---
        st.success(f"🌟 **靈數強化：** 建議配戴 **{info['crystal']}** 強化天賦。")
            
    except Exception as e:
        st.error("分析出錯，請檢查輸入。")

# --- 7. 頁尾 ---
st.divider()
st.caption("僅供參考，心有所願的人，自然就會強大！")
st.markdown("🔗 **挑選請洽 [Nebulab.Crystals](http://ig.me/m/nebulab.crystals)**")
