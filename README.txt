# 🔐 Cipher Program

This project is a simple Python-based cryptography toolkit that implements two classic ciphers:

- **Caesar Cipher (shift-based substitution)
- **Rail Fence Cipher (zig-zag transposition)

It supports encryption, decryption, manual decryption attempts, and a "Heavy Mode" that tries all logical combinations automatically.

---

## 📂 Files Used
- `input.txt` → Contains the plaintext (for encryption) or ciphertext (for decryption).
- `output.txt` → Stores the result of encryption.
- `compare.txt` → Contains the expected plaintext (used in Heavy Mode to check matches).
- `processing.txt` → Logs all brute-force attempts in Heavy Mode.

---

## ▶️ How to Run
1. Save your plaintext in `input.txt`.
2. Run the program:
   ```bash
   python cipher_program.py
