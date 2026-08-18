import os
import json
import urllib.request

def generate():
    os.makedirs("profile-summary-card-output/tokyonight", exist_ok=True)
    
    # 1. Stats Card
    stats_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="450" height="220" viewBox="0 0 450 220" fill="none">
  <rect width="450" height="220" rx="15" fill="#0D1117" stroke="#6C63FF" stroke-width="1.5"/>
  <text x="35" y="45" fill="#6C63FF" font-family="'Segoe UI', Ubuntu, sans-serif" font-weight="700" font-size="20">Jivtesh's GitHub Stats</text>
  
  <g transform="translate(35, 75)">
    <!-- Repos -->
    <text x="0" y="20" fill="#4ECDC4" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="600">📦 Public Repositories:</text>
    <text x="380" y="20" fill="#FFFFFF" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="700" text-anchor="end">26</text>
    
    <!-- Followers -->
    <text x="0" y="55" fill="#45B7D1" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="600">👥 Followers:</text>
    <text x="380" y="55" fill="#FFFFFF" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="700" text-anchor="end">5</text>
    
    <!-- Following -->
    <text x="0" y="90" fill="#96CEB4" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="600">🌐 Following:</text>
    <text x="380" y="90" fill="#FFFFFF" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="700" text-anchor="end">4</text>
    
    <!-- Contributions -->
    <text x="0" y="125" fill="#FFEAA7" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="600">⚡ Primary Tech:</text>
    <text x="380" y="125" fill="#FFFFFF" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="700" text-anchor="end">Python / Rust / TS</text>
  </g>
</svg>"""

    # 2. Language Breakdown Card
    langs_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="450" height="220" viewBox="0 0 450 220" fill="none">
  <rect width="450" height="220" rx="15" fill="#0D1117" stroke="#6C63FF" stroke-width="1.5"/>
  <text x="35" y="45" fill="#6C63FF" font-family="'Segoe UI', Ubuntu, sans-serif" font-weight="700" font-size="20">Top Languages by Repos</text>
  
  <g transform="translate(35, 75)">
    <!-- Python (38%) -->
    <text x="0" y="18" fill="#A9A9A9" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="13">Python (38%)</text>
    <rect x="150" y="7" width="220" height="12" rx="6" fill="#161B22"/>
    <rect x="150" y="7" width="83.6" height="12" rx="6" fill="#3572A5"/>
    
    <!-- TypeScript (14%) -->
    <text x="0" y="48" fill="#A9A9A9" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="13">TypeScript (14%)</text>
    <rect x="150" y="37" width="220" height="12" rx="6" fill="#161B22"/>
    <rect x="150" y="37" width="30.8" height="12" rx="6" fill="#3178C6"/>
    
    <!-- JavaScript (14%) -->
    <text x="0" y="78" fill="#A9A9A9" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="13">JavaScript (14%)</text>
    <rect x="150" y="67" width="220" height="12" rx="6" fill="#161B22"/>
    <rect x="150" y="67" width="30.8" height="12" rx="6" fill="#F7DF1E"/>
    
    <!-- Rust (10%) -->
    <text x="0" y="108" fill="#A9A9A9" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="13">Rust (10%)</text>
    <rect x="150" y="97" width="220" height="12" rx="6" fill="#161B22"/>
    <rect x="150" y="97" width="22" height="12" rx="6" fill="#DEA584"/>
  </g>
</svg>"""

    with open("profile-summary-card-output/tokyonight/3-stats.svg", "w") as f:
        f.write(stats_svg)
        
    with open("profile-summary-card-output/tokyonight/1-repos-per-language.svg", "w") as f:
        f.write(langs_svg)
        
    print("✅ Static SVG cards generated successfully!")

if __name__ == "__main__":
    generate()
