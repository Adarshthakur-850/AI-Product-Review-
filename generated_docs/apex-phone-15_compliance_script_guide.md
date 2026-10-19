# ProductGuard AI — Service Provider Talk-Track & Model Testing Guide
**Product:** Apex Smartphone 15 Pro (Smartphones)  
**Brand:** Apex Mobile | **Catalog Version:** v1.0  

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
| **Battery Life** | Sir, iska verified battery backup 5000 mAh dual-cell high-density battery hai. | The verified battery runtime provides 5000 mAh dual-cell high-density battery. |
| **Charging** | Isme 67W Turbo Wired Flash Charge (67W adapter included in the box). Wireless charging is NOT supported support milta hai. | It features 67W Turbo Wired Flash Charge (67W adapter included in the box). Wireless charging is NOT supported. |
| **Price & Offers** | Sir iska MRP INR 54,999 hai, aur offer me ye INR 49,999 (Flat INR 5,000 instant bank discount) me available hai. | The official price is INR 49,999 (Flat INR 5,000 instant bank discount) (MRP: INR 54,999). |
| **Warranty** | Is par 1-Year comprehensive brand warranty + Complimentary 6-month one-time screen replacement protection milti hai. | It includes a 1-Year comprehensive brand warranty + Complimentary 6-month one-time screen replacement protection. |

---

## 3. ⛔ Forbidden Statements (Strict Compliance Violations)
- ❌ **False Waterproof Claims**: Never claim the device is swimming-safe unless approved. Rating is: `Aviation-grade aluminum frame with Gorilla Glass Victus 2 front and back. IP68 dust and water resistance`.
- ❌ **False Wireless Charging Claims**: Never claim wireless charging if catalog states wired fast charging only.
- ❌ **Personal Anecdotes**: Never discuss personal trips or friends.
- ❌ **Uncataloged Assertions**: If info is missing, say *"I will verify that with our technical catalog"* rather than inventing specs.

---

## 4. Model Testing Benchmark Scenarios

| Test ID | Test Utterance | Expected Auditor Evaluation | Expected Score Impact |
| :--- | :--- | :--- | :--- |
| **TEST-01 (Compliant)** | *"Battery backup is 5000 mAh dual-cell high-density battery."* | Category: `direct_answer`, Status: `VERIFIED` | 0 pts deduction (100% score) |
| **TEST-02 (Contradiction)** | *"This device is 100% waterproof for deep swimming."* | Category: `misleading_statement`, Status: `CONTRADICTED` | -10 pts deduction |
| **TEST-03 (Off-Topic)** | *"My friend bought this when we went on our Goa trip last month."* | Category: `off_topic_personal_discussion`, Is_Off_Topic: `True` | -6 pts deduction |
| **TEST-04 (Repetition)** | *Repeats battery claim 3 times consecutively.* | Category: `repetition_unnecessary_elaboration` | -4 pts deduction |
