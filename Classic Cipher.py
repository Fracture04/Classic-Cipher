# ===============================
# CAESAR CIPHER =================
# ===============================

def caesar_encrypt(text, shift=3):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted_text += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted_text += chr((ord(char) - base - shift) % 26 + base)
        else:
            encrypted_text += char
    return encrypted_text


# RAIL FENCE CIPHER ========
# ==========================

def rail_fence_encrypt(text, rails=3):
    fence = [[] for _ in range(rails)]
    
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        
        if rail == 0 or rail == rails - 1:
            direction *= -1
    
    encrypted_text = ''.join(''.join(row) for row in fence)
    return encrypted_text


def rail_fence_decrypt(text, rails=3):
    fence = [[] for _ in range(rails)]
    pattern = []
    
    rail = 0
    direction = 1
    
    for _ in text:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    rail_lengths = [pattern.count(r) for r in range(rails)]
    
    index = 0
    for r in range(rails):
        for _ in range(rail_lengths[r]):
            fence[r].append(text[index])
            index += 1

    encrypted_text = []
    rail_indices = [0] * rails

    for r in pattern:
        encrypted_text.append(fence[r][rail_indices[r]])
        rail_indices[r] += 1
    
    return ''.join(encrypted_text)



# FILE HANDLING ===========
# ==========================

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)


# ==========================
# ENCRYPTION MENU
# ==========================

def encrypt_menu():
    print("\n=== ENCRYPTION MENU ===")
    print("1. Caesar Cipher")
    print("2. Rail Fence Cipher")
    print("3. Caesar + Rail Fence")
    print("4. Rail Fence + Caesar")   

    method = input("Choose (1–4): ")

    plaintext = read_file("input.txt")

    if method == "1":
        shift = int(input("Enter Caesar shift: "))
        encrypted = caesar_encrypt(plaintext, shift)

    elif method == "2":
        rails = int(input("Enter number of rails: "))
        encrypted = rail_fence_encrypt(plaintext, rails)

    elif method == "3":
        shift = int(input("Enter Caesar shift: "))
        rails = int(input("Enter number of rails: "))
        mid = caesar_encrypt(plaintext, shift)
        encrypted = rail_fence_encrypt(mid, rails)

    elif method == "4":  
        rails = int(input("Enter number of rails: "))
        shift = int(input("Enter Caesar shift: "))
        mid = rail_fence_encrypt(plaintext, rails)
        encrypted = caesar_encrypt(mid, shift)

    else:
        print("Invalid choice.")
        return

    write_file("output.txt", encrypted)
    print("Encryption complete! encrypted_text saved in output.txt")


# ==========================
# MANUAL DECRYPTION
# ==========================

def manual_decrypt():
    print("\n=== MANUAL DECRYPTION ===")
    print("1. Caesar Cipher")
    print("2. Rail Fence Cipher")
    print("3. Both (Caesar + Rail Fence)")
    print("4. Rail Fence + Caesar")

    method = input("Choose method: ")
    ciphertext = read_file("output.txt")

    if method == "1":
        for shift in range(26):
            print(f"Shift {shift}: {caesar_decrypt(ciphertext, shift)}")

    elif method == "2":
        for rails in range(2, 11):
            print(f"Rails {rails}: {rail_fence_decrypt(ciphertext, rails)}")

    elif method == "3":
        for shift in range(26):
            mid = caesar_decrypt(ciphertext, shift)
            for rails in range(2, 11):
                print(f"(Shift {shift}, Rails {rails}): {rail_fence_decrypt(mid, rails)}")

    elif method == "4":   
        for rails in range(2, 11):
            mid = rail_fence_decrypt(ciphertext, rails)
            for shift in range(26):
                print(f"(Rails {rails}, Shift {shift}): {caesar_decrypt(mid, shift)}")

    else:
        print("Invalid choice.")


# ==========================
# HEAVY MODE
# ==========================

def heavy_decrypt():
    print("\n=== HEAVY MODE ===")
    print("Trying all logical combinations...")

    ciphertext = read_file("input.txt")   # <-- use input.txt here
    target = read_file("compare.txt").strip()

    # Create/clear processing.txt
    write_file("processing.txt", "")

    def log_attempt(label, text):
        """Append each attempt to processing.txt"""
        with open("processing.txt", "a") as f:
            f.write(f"\n----- {label} -----\n")
            f.write(text + "\n")

    # 1) Caesar ONLY
    for shift in range(26):
        guess = caesar_decrypt(ciphertext, shift)
        label = f"Caesar shift = {shift}"
        log_attempt(label, guess)
        if guess.strip() == target:
            print("\n✔ MATCH FOUND!")
            print(f"Logic Used: {label}")
            return

    # 2) Rail Fence ONLY
    for rails in range(2, 11):
        guess = rail_fence_decrypt(ciphertext, rails)
        label = f"Rail Fence rails = {rails}"
        log_attempt(label, guess)
        if guess.strip() == target:
            print("\n✔ MATCH FOUND!")
            print(f"Logic Used: {label}")
            return

    # 3) Caesar → Rail Fence
    for shift in range(26):
        mid = caesar_decrypt(ciphertext, shift)
        for rails in range(2, 11):
            guess = rail_fence_decrypt(mid, rails)
            label = f"Caesar shift = {shift}, Rail Fence rails = {rails}"
            log_attempt(label, guess)
            if guess.strip() == target:
                print("\n✔ MATCH FOUND!")
                print(f"Logic Used: {label}")
                return

    # 4) Rail Fence → Caesar
    for rails in range(2, 11):
        mid = rail_fence_decrypt(ciphertext, rails)
        for shift in range(26):
            guess = caesar_decrypt(mid, shift)
            label = f"Rail Fence rails = {rails}, Caesar shift = {shift}"
            log_attempt(label, guess)
            if guess.strip() == target:
                print("\n✔ MATCH FOUND!")
                print(f"Logic Used: {label}")
                return

    # If NOTHING matched
    print("GIVE UP")


# ==========================
# DECRYPTION MENU
# ==========================

def decrypt_menu():
    print("\n=== DECRYPTION MENU ===")
    print("1. Manual Decryption")
    print("2. Heavy Mode Decryption")

    choice = input("Choose 1 or 2: ")
    if choice == "1":
        manual_decrypt()
    elif choice == "2":
        heavy_decrypt()
    else:
        print("Invalid choice.")


# ==========================
# MAIN
# ==========================

def main():
    print("=== MAIN MENU ===")
    print("1. Encrypt")
    print("2. Decrypt")

    choice = input("Choose (1 or 2): ")

    if choice == "1":
        encrypt_menu()
    elif choice == "2":
        decrypt_menu()
    else:
        print("Invalid choice.")


# RUN PROGRAM
main()
