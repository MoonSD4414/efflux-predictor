import streamlit as st
import joblib
from utils import extract_features

# 預載模型
model = joblib.load("efflux_model.pkl")

st.title("Efflux Protein Family Predictor 🧬")
st.markdown("上傳蛋白質序列（FASTA 格式），預測其所屬 Efflux 家族")

# 使用者輸入
fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")

if st.button("開始預測"):
    if fasta_input.strip() == "":
        st.warning("請輸入序列資料")
    else:
        # 提取序列部分（只要一條序列）
        lines = fasta_input.strip().split('\n')
        seq = ''.join([line.strip() for line in lines if not line.startswith(">")])

        # 特徵萃取
        features = extract_features(seq)  # 自己寫 AAC/DPC/PSSM 萃取

        # 模型預測
        prediction = model.predict([features])[0]
        st.success(f"預測結果：該蛋白屬於 **{prediction}** 家族")
