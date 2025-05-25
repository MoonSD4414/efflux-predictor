import streamlit as st
import joblib
import numpy as np
from utils import extract_aac_features
import smtplib
from email.message import EmailMessage

# ========== 載入模型與編碼器 ==========
model = joblib.load("svm_model_AAC.pkl")
label_encoder = joblib.load("label_encoder_AAC.pkl")

# ========== 預測頁面 UI ==========
st.title("Efflux Protein Family Predictor 🧬")
st.markdown("請輸入或上傳單條蛋白質序列（FASTA 格式），進行家族分類預測。")

input_method = st.radio("請選擇輸入方式：", ["貼上序列", "上傳 FASTA 檔案"])
sequence = ""

# ========== 貼上序列 ==========
if input_method == "貼上序列":
    fasta_input = st.text_area("請貼上蛋白質序列（FASTA 格式）")
    if fasta_input.strip():
        lines = fasta_input.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

# ========== 上傳檔案 ==========
elif input_method == "上傳 FASTA 檔案":
    uploaded_file = st.file_uploader("請上傳 FASTA 檔案", type=["fasta", "fa", "txt"])
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        lines = content.strip().split('\n')
        sequence = ''.join([line.strip() for line in lines if not line.startswith(">")])

# ========== 預測按鈕 ==========
if st.button("開始預測"):
    if not sequence:
        st.warning("請提供蛋白質序列")
    elif not sequence.isalpha():
        st.error("❌ 序列中包含非字母字符，請確認格式正確（僅限 A-Z）")
    else:
        features = extract_aac_features(sequence).reshape(1, -1)
        pred = model.predict(features)[0]
        decoded = label_encoder.inverse_transform([pred])[0]
        st.success(f"✅ 預測家族：**{decoded}**")

        # ========== Email 輸入與寄送 ==========
        st.markdown("### 📧 將預測結果寄送至您的信箱")
        email_input = st.text_input("請輸入 Email")
        send_btn = st.button("寄送結果到信箱")

        if send_btn:
            if not email_input or "@" not in email_input:
                st.error("請輸入有效的 Email 地址")
            else:
                subject = "Efflux Protein Family Prediction Result"
                body = f"您好，您所輸入的蛋白質序列預測家族為：{decoded}"

                #  Gmail 發信帳號與應用程式密碼
                smtp_user = "s10240410@gmail.com"        
                smtp_pass = "p10240410"           

                try:
                    msg = EmailMessage()
                    msg.set_content(body)
                    msg["Subject"] = subject
                    msg["From"] = smtp_user
                    msg["To"] = email_input

                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(smtp_user, smtp_pass)
                        smtp.send_message(msg)

                    st.success("📧 已成功寄出結果信件！")
                except Exception as e:
                    st.error(f"❌ 發送失敗：{e}")
