from google import genai
import streamlit as st

# Gemini API Key को Streamlit Secrets से लोड करना
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

PROJECT_KNOWLEDGE = """
प्रोजेक्ट शीर्षक: पारंपरिक और डिजिटल शिक्षा का संगम (Traditional vs Digital Learning)

आधार 1: Digital + Traditional Learning (मिश्रित शिक्षण)
- पारंपरिक चॉक-टॉक और किताबों के साथ डिजिटल टूल्स (स्क्रीन, एनिमेशन) का संतुलन।

आधार 2: T.L.M (Teaching Learning Material - शिक्षण अधिगम सामग्री)
- हस्तनिर्मित चार्ट, मॉडल, फ्लैशकार्ड और 3D आकृतियाँ।

आधार 3: Low Cost Smart Class (किफायती स्मार्ट क्लासरूम)
- महंगे स्मार्ट बोर्ड की जगह कम लागत वाला प्रोजेक्टर, टीवी या फोन का उपयोग।

आधार 4: Inclusive Education (समावेशी शिक्षा)
- सामान्य और विशेष आवश्यकता वाले (दिव्यांग) बच्चों को एक साथ पढ़ाना।

आधार 5: Activity Based Learning (गतिविधि आधारित शिक्षा)
- रोल-प्ले, पहेलियाँ, विज्ञान के आसान प्रयोग और गणितीय खेल (Learning by Doing)।

आधार 6: Eco-Friendly School (पर्यावरण अनुकूल विद्यालय)
- प्लास्टिक-मुक्त परिसर, वेस्ट मटेरियल से टी.एल.एम. बनाना।
"""

system_prompt = f"""
तुम 'शिक्षा सेतु AI' हो।
तुम्हारा काम स्कूल प्रोजेक्ट "पारंपरिक और डिजिटल शिक्षा" के 6 आधारों को समझाना है:
{PROJECT_KNOWLEDGE}
हमेशा सरल, आदरपूर्ण और स्पष्ट हिंदी में उत्तर दो।
"""

st.set_page_config(page_title="शिक्षा सेतु AI Assistant", page_icon="📚")

st.title("🎓 पारंपरिक एवं डिजिटल शिक्षा AI गाइड")
st.caption("हमारे स्कूल मॉडल के 6 स्तंभों के बारे में सवाल पूछें।")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "नमस्ते! मैं आपके प्रोजेक्ट का AI सहायक हूँ। 6 आधारों में से किसी पर भी सवाल पूछें।"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("अपना सवाल यहाँ लिखें...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input,
        config={"system_instruction": system_prompt},
    )

    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)