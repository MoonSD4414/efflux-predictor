import streamlit as st
import joblib
import numpy as np
from utils import extract_aac_features

# 載入模型與 LabelEncoder
model = joblib.load("svm_model_AAC.pkl")
label_encoder = joblib.load("label_encoder_AAC.pkl")

st.title("Efflux Protein Family Predictor 🧬")
st.markdown("輸入蛋白質序列（單條，FASTA 格式）進行家族分類預測。")

fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")

if st.button("開始預測"):
    if not fasta_input.strip():
        st.warning("請輸入蛋白質序列")
    else:
        # 擷取序列（忽略 > 標頭）
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

        if not sequence.isalpha():
            st.error("序列中包含非字母字符，請確認格式正確")
        else:
            # 特徵萃取
            features = extract_aac_features(sequence)

            # 預測
            prediction = model.predict([features])[0]
            decoded = label_encoder.inverse_transform([prediction])[0]

            st.success(f"✅ 預測家族：**{decoded}**")
