import os
import re

directory = r"c:\Users\Arjee\aryan\HTML-FILE\CODES"

files_to_update = [
    "Dashboard.html",
    "Event.html",
    "guest.html",
    "qr.html",
    "scanner.html",
    "pre-registration.html",
    "pre-reg-submissions.html",
    "settings.html",
    "scanner-settings.html"
]

new_css = """/* MOBILE MENU */
.mobile-menu{
  display:none;
  flex-direction:column;
  background:var(--card);
  border-bottom:1px solid var(--border);
  padding:14px 20px;
}
.mobile-menu a{
  padding:10px 0;
  text-decoration:none;
  color:var(--text);
  font-weight:500;
}
.mobile-settings {
  padding: 10px 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.mobile-settings .settings-btn {
  padding: 0;
  font-size: 16px;
  font-weight: 500;
  color: var(--text);
  background: transparent;
}
.mobile-settings .settings-menu {
  position: static;
  box-shadow: none;
  border: none;
  padding-left: 12px;
  width: 100%;
  margin-top: 10px;
  border-left: 2px solid var(--border);
  border-radius: 0;
}
.mobile-settings .settings-menu a {
  padding: 8px 12px;
  font-size: 14px;
}"""

for filename in files_to_update:
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace the old MOBILE MENU section up to /* PAGE */ or the end of style if no /* PAGE */
    # Some files use /* PAGE */, some use /* CONTENT */, some just end the style block.
    # Let's find /* MOBILE MENU */
    
    start_idx = content.find("/* MOBILE MENU */")
    if start_idx == -1:
        print(f"Could not find /* MOBILE MENU */ CSS in {filename}")
        continue
        
    # Find next CSS comment or </style>
    end_idx1 = content.find("/* PAGE */", start_idx)
    end_idx2 = content.find("/* LOGOUT */", start_idx)
    end_idx3 = content.find("</style>", start_idx)
    end_idx4 = content.find("/* CONTENT */", start_idx)
    end_idx5 = content.find("/* ================= PAGE ================= */", start_idx)
    
    # We want the first one that appears after Mobile Menu except for LOGOUT maybe?
    # Some have LOGOUT inside or after. 
    # Just look for the first match amongst these.
    candidates = [idx for idx in [end_idx1, end_idx2, end_idx3, end_idx4, end_idx5] if idx != -1]
    
    if not candidates:
        print(f"Could not find end of mobile menu CSS in {filename}")
        continue
        
    end_idx = min(candidates)
    
    new_content = content[:start_idx] + new_css + "\n\n" + content[end_idx:]
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Updated CSS for {filename}")
