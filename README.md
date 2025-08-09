# 🏦 Bank Agent Mini Project

A simple **Bank Agent** chatbot built in Python that supports multiple accounts, input/output guardrails, and secure PIN-based access.  
This project follows the structure demonstrated in class and is suitable for AI + Python learning.

---

## ✨ Features
- 🔒 **PIN-protected access** for users
- 🧾 **Multiple account support** (different balances for each)
- 🛡 **Input guardrails** to validate requests
- 📤 **Output guardrails** to ensure controlled responses
- 🤝 **Multiple agents** (handoff support)
- 📚 **Context-aware responses** (remembers logged-in user)

---
🧑‍💻 **How It Works**
User enters name & PIN (stored in context)
Input guardrail checks if query is bank-related
Agent verifies account from multiple saved accounts
If match found → Balance displayed
Otherwise → "Account not found"

📝 Example Accounts
**Name	PIN	 Balance

Anum	1234	$100,000

Ali	 5678	  $50,000

Sara	1111	$75,000**

