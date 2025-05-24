import streamlit as st
import joblib
import numpy as np
from utils import extract_aac_features
from tensorflow.keras.models import load_model

# 載入模型與標籤編碼器
svm_model = joblib.load("svm_model_AAC.pkl")
svm_label_encoder = joblib.load("label_encoder_AAC.pkl")

cnn_model = load_model("family_predictor_cnn.h5")
cnn_label_encoder = joblib.load("family_label_encoder.pkl")

st.title("Efflux Protein Family Predictor 🧬")
st.markdown("輸入蛋白質序列（FASTA 格式），選擇模型進行家族預測。")

# 模型選擇器
model_option = st.selectbox("請選擇預測模型", ["SVM (AAC)", "CNN (AAC)"])

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

            if model_option == "SVM (AAC)":
                pred = svm_model.predict(features)[0]
                result = svm_label_encoder.inverse_transform([pred])[0]
            else:
                features_cnn = features.reshape(1, 20, 1)  # CNN input shape (batch, length, channel)
                pred = np.argmax(cnn_model.predict(features_cnn), axis=1)[0]
                result = cnn_label_encoder.inverse_transform([pred])[0]

            st.success(f"✅ 預測家族：**{result}**")
