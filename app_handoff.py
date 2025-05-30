
import streamlit as st
from datetime import datetime
from html2image import Html2Image
import yagmail

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "bashammakh97.2.5@gmail.com"

hti = Html2Image(output_path='.')

st.set_page_config(page_title="Surgical Handoff App", layout="centered")
st.title("🔄 Surgical Handoff Submission")

with st.form("handoff_form"):
    st.subheader("🩺 Patient Medical Record")
    name = st.text_input("Name")
    room = st.text_input("Room")
    specialist = st.text_input("Specialist")
    age = st.text_input("Age")
    allergy = st.text_input("Allergy")
    pmhx = st.text_area("Past Medical History")
    pshx = st.text_area("Past Surgical History")
    diagnosis = st.text_area("Diagnosis")
    operation = st.text_area("Operation")
    diet = st.text_input("Diet")
    ivf = st.text_input("IV Fluids")
    bp = st.text_input("BP")
    hr = st.text_input("HR")
    rr = st.text_input("RR")
    temp = st.text_input("Temp")
    amb = st.checkbox("Ambulation")
    uri = st.checkbox("Urination")
    eat = st.checkbox("Diet Tolerance")
    dress = st.checkbox("Dressing Change")
    foley = st.text_input("Foley")
    ngt = st.text_input("NGT")
    drain = st.text_input("Drain")
    chest_tube = st.text_input("Chest Tube")
    stoma = st.text_input("Stoma")
    meds = [st.text_input(f"Medication {i+1}") for i in range(5)]
    dvt = st.text_input("DVT Prophylaxis")
    analgesia = st.text_input("Analgesia")
    notes = st.text_area("Important Notes")
    consult = st.text_input("Consultation")

    submitted = st.form_submit_button("📤 Submit and Send to Email")

if submitted:
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html = f"""
    <html><body style='font-family:Arial; width:800px;'>
    <h2>Patient Medical Record - {now}</h2>
    <p><b>Name:</b> {name} &nbsp;&nbsp; <b>Room:</b> {room}</p>
    <p><b>Specialist:</b> {specialist}</p>
    <p><b>Age:</b> {age} &nbsp;&nbsp; <b>Allergy:</b> {allergy}</p>
    <p><b>PM Hx:</b><br>{pmhx.replace('\n', '<br>')}</p>
    <p><b>PS Hx:</b><br>{pshx.replace('\n', '<br>')}</p>
    <p><b>Diagnosis:</b><br>{diagnosis.replace('\n', '<br>')}</p>
    <p><b>Operation:</b><br>{operation.replace('\n', '<br>')}</p>
    <p><b>Diet:</b> {diet}</p>
    <p><b>IVF:</b> {ivf}</p>
    <p><b>Vitals:</b> BP: {bp}, HR: {hr}, RR: {rr}, Temp: {temp}</p>
    <p><b>Checklist:</b><br>
    Amb: {'✔️' if amb else '❌'} &nbsp; Uri: {'✔️' if uri else '❌'} &nbsp;
    Diet: {'✔️' if eat else '❌'} &nbsp; Dress: {'✔️' if dress else '❌'}</p>
    <p><b>Devices:</b><br>
    - Foley: {foley}<br>- NGT: {ngt}<br>- Drain: {drain}<br>
    - Chest Tube: {chest_tube}<br>- Stoma: {stoma}</p>
    <p><b>Medications:</b><br>"""
    for med in meds:
        if med:
            html += f"- {med}<br>"
    html += f"""
    <p><b>DVT Prophylaxis:</b> {dvt}</p>
    <p><b>Analgesia:</b> {analgesia}</p>
    <p><b>Notes:</b><br>{notes.replace('\n', '<br>')}</p>
    <p><b>Consultation:</b> {consult}</p>
    </body></html>
    """

    image_name = f"handoff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    hti.screenshot(html_str=html, save_as=image_name)

    try:
        yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
        yag.send(
            to=EMAIL_RECEIVER,
            subject="📝 Surgical Handoff",
            contents="Attached is your patient handoff record.",
            attachments=image_name
        )
        st.success(f"Handoff image sent to {EMAIL_RECEIVER}")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
