import zxcvbn
import hashlib
import requests
import matplotlib.pyplot as plt

# Test dataset bridging different structural complexities
test_passwords = [
    "password123", "Tr0ub4dor&3", "correcthorsebatterystaple", "123456", 
    "Admin@123", "Qwerty!2026", "SuperSecretKey99!", "monkey12", "iloveyou", "P@ssw0rd!"
]

scores = []
breach_counts = []

print("[*] Running comparative research benchmark...")
for pwd in test_passwords:
    # 1. Entropy Score
    res = zxcvbn.zxcvbn(pwd)
    scores.append(res['score'])
    
    # 2. Breach Check
    sha1 = hashlib.shasub = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=3)
        count = 0
        if r.status_code == 200:
            for line in r.text.splitlines():
                if line.split(':')[0] == suffix:
                    count = int(line.split(':')[1])
                    break
        breach_counts.append(count)
    except:
        breach_counts.append(0)

# Generate Research Visualization
plt.figure(figsize=(9, 5))
plt.scatter(scores, breach_counts, color='#dc3545', s=120, zorder=3)
plt.title("Comparative Analysis: Entropy Score vs. Real-World Breach Frequency")
plt.xlabel("zxcvbn Mathematical Entropy Score (0 = Weak, 4 = Strong)")
plt.ylabel("Times Leaked in Public Databases (Log Scale)")
plt.yscale('symlog')
plt.grid(True, linestyle='--', alpha=0.6)

for i, txt in enumerate(test_passwords):
    plt.annotate(txt, (scores[i], breach_counts[i]), fontsize=9, xytext=(6, 6), textcoords='offset points')

plt.tight_layout()
plt.savefig("research_benchmark_plot.png", dpi=300)
print("[+] Benchmark complete! Saved graph as 'research_benchmark_plot.png' for your report.")