import streamlit as st
import numpy as np
from utils import extract_aac_features

# ==== 假模型與假 LabelEncoder ====
class DummyModel:
    def predict(self, X):
        return [0]  # 固定預測類別索引為 0

class DummyLabelEncoder:
    def inverse_transform(self, labels):
        return ["ABC Transporter"]  # 類別索引 0 對應的標籤

# ==== 使用假模型 ====
model = DummyModel()
label_encoder = DummyLabelEncoder()

# ==== UI ====
st.title("Efflux Protein Family Predictor 🧬")
st.markdown("輸入蛋白質序列（FASTA 格式），測試網站能否正常運行（使用假模型）。")

fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")

if st.button("開始預測"):
    if not fasta_input.strip():
        st.warning("請輸入蛋白質序列")
    else:
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

        if not sequence.isalpha():
            st.error("序列中包含非字母字符，請確認格式正確")
        else:
            features = extract_aac_features(sequence).reshape(1, -1)
            pred = model.predict(features)[0]
            result = label_encoder.inverse_transform([pred])[0]
            st.success(f"✅ 模擬預測家族：**{result}**")
