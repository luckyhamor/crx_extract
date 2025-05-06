# vulnerable.py

# Vulnerable: Command injection via eval()
def command_injection():
    user_input = "__import__('os').system('ls')"
    eval(user_input)  # This is dangerous!

# Vulnerable: Hardcoded credentials
def hardcoded_credentials():
    username = "admin"
    password = "password123"  # Hardcoded password (not secure)
    print(f"Logging in with {username}:{password}")

# Vulnerable: Insecure deserialization
import pickle
def insecure_deserialization():
    data = b"cos\nsystem\n(S'ls'\ntR."
    pickle.loads(data)  # This deserialization can execute arbitrary code

command_injection()
hardcoded_credentials()
insecure_deserialization()
