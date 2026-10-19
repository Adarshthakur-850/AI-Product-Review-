# ProductGuard AI — Service Provider Talk-Track & Model Testing Guide
**Product:** Quantum Sound Pro ANC Wireless Headphones (Audio & Headphones)  
**Brand:** QuantumTech | **Catalog Version:** v1.0  

---

## 1. Mandatory Service Provider Rules of Engagement
1. **Strict Factual Grounding**: Quote ONLY verified specifications from approved catalog sheets. Never guess.
2. **Conversational Relevance**: Answer the customer's question directly. Strictly avoid personal anecdotes (vacations, friends, family).
3. **Paced Conciseness**: Keep each turn under 40 words. Allow customer follow-ups.
4. **Multilingual Fluidity**: Accurately converse in English, Hindi, or Hinglish while preserving technical terms.

---

## 2. Approved Multilingual Talk-Track Scripts

| Customer Question / Topic | Approved Talk-Track (Hinglish / Hindi) | Approved Talk-Track (English) |
| :--- | :--- | :--- |
| **Greeting** | Namaste sir, welcome! Main is product ke specifications me aapki kya sahayata kar sakta hu? | Hello, welcome! How can I assist you with this product's specifications today? |
| **Battery Life** | Sir, iska verified battery backup Up to 30 hours of playtime with ANC OFF, 24 hours with ANC ON hai. | The verified battery runtime provides Up to 30 hours of playtime with ANC OFF, 24 hours with ANC ON. |
| **Charging** | Isme USB-C fast charging: 10 minutes gives 4 hours of playback. Full charge takes 90 minutes support milta hai. | It features USB-C fast charging: 10 minutes gives 4 hours of playback. Full charge takes 90 minutes. |
| **Price & Offers** | Sir iska MRP INR 7,999 hai, aur offer me ye INR 5,999 me available hai. | The official price is INR 5,999 (MRP: INR 7,999). |
| **Warranty** | Is par 1-Year comprehensive manufacturer replacement warranty against functional defects milti hai. | It includes a 1-Year comprehensive manufacturer replacement warranty against functional defects. |

---

## 3. ⛔ Forbidden Statements (Strict Compliance Violations)
- ❌ **False Waterproof Claims**: Never claim the device is swimming-safe unless approved. Rating is: `IPX4 splash and sweat resistant (not suitable for swimming or heavy rain)`.
- ❌ **False Wireless Charging Claims**: Never claim wireless charging if catalog states wired fast charging only.
- ❌ **Personal Anecdotes**: Never discuss personal trips or friends.
- ❌ **Uncataloged Assertions**: If info is missing, say *"I will verify that with our technical catalog"* rather than inventing specs.

---

## 4. Model Testing Benchmark Scenarios

| Test ID | Test Utterance | Expected Auditor Evaluation | Expected Score Impact |
| :--- | :--- | :--- | :--- |
| **TEST-01 (Compliant)** | *"Battery backup is Up to 30 hours of playtime with ANC OFF, 24 hours with ANC ON."* | Category: `direct_answer`, Status: `VERIFIED` | 0 pts deduction (100% score) |
| **TEST-02 (Contradiction)** | *"This device is 100% waterproof for deep swimming."* | Category: `misleading_statement`, Status: `CONTRADICTED` | -10 pts deduction |
| **TEST-03 (Off-Topic)** | *"My friend bought this when we went on our Goa trip last month."* | Category: `off_topic_personal_discussion`, Is_Off_Topic: `True` | -6 pts deduction |
| **TEST-04 (Repetition)** | *Repeats battery claim 3 times consecutively.* | Category: `repetition_unnecessary_elaboration` | -4 pts deduction |
