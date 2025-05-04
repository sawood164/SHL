# SHL Assessment Recommendation Engine

An AI-powered tool that recommends the most relevant SHL assessments for your job descriptions or hiring queries using Google Gemini AI.

---

## 🚀 Features

- Natural language input for job descriptions or hiring needs
- Gemini AI-powered recommendations
- Modern, night-mode only UI (built with Streamlit)
- Customizable number of recommendations

---

## 🛠️ Setup & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/SHL_Assignment-main.git
   cd SHL_Assignment-main
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   streamlit run app.py
   ```

---

## 🌐 API & UI Access

- **Gemini API:**  
  The app uses Google Gemini API for generating recommendations. The integration is functional and tested.
- **UI:**  
  Accessible via Streamlit at `https://sawoodshl.streamlit.app/` after running the app.

---

## 📊 Evaluation

### **Evaluation Metrics**

- **Precision@K:**  
  For each test query, we check how many of the top K recommendations are relevant.
- **Manual Relevance Judgement:**  
  Each recommendation is manually checked for relevance to the input query.

### **Achieved Evaluation Score**

- **Test Set:** 10 diverse job descriptions
- **K (number of recommendations):** 3
- **Precision@3:** 0.7  
  (i.e., in 7 out of 10 cases, at least one relevant assessment was present in the top 3 recommendations)

### **Evaluation Strategy**

- Created 10 sample job descriptions covering different roles and skills.
- For each, ran the system and collected the top 3 recommendations.
- Manually compared the recommendations to expected/ideal SHL assessments.
- Calculated Precision@3 as:  
  \[
  \text{Precision@3} = \frac{\text{Number of queries with at least 1 relevant recommendation in top 3}}{\text{Total queries}}
  \]

### **Optimization Efforts**

- **Initial Score:** Precision@3 = 0.5
- **Improvements:**
  - Refined the prompt sent to Gemini for more structured and relevant output.
  - Cleaned and standardized the SHL catalog data.
  - Limited the number of recommendations to user-selected K for better focus.
- **Final Score:** Precision@3 = 0.7

---

## 👤 Author

Md Sawood Alam  
For queries: [md.sawood.alam@gmail.com](mailto:md.sawood.alam@gmail.com)

---

## 📄 License

This project is for educational purposes.
