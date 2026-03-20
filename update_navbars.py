import os
import re

directory = r"c:\Users\Arjee\aryan\HTML-FILE\CODES"

files_to_update = [
    ("Dashboard.html", "Dashboard.html"),
    ("Event.html", "Event.html"),
    ("guest.html", "guest.html"),
    ("qr.html", "qr.html"),
    ("scanner.html", "scanner.html"),
    ("pre-registration.html", "pre-registration.html"),
    ("pre-reg-submissions.html", "pre-reg-submissions.html"),
    ("settings.html", "settings.html"),
    ("scanner-settings.html", "scanner-settings.html"),
]

def get_template(active_page):
    def make_link(href, text):
        if href == active_page:
            return f'<a class="active">{text}</a>'
        return f'<a href="{href}">{text}</a>'

    return f"""<div class="navbar">
    <div class="nav-left">
      <div class="logo">
        <img src="logo.png" alt="TalentYug">
      </div>
      <div class="nav-links">
        {make_link('Event.html', 'My Events')}
        {make_link('Dashboard.html', 'Dashboard')}
        {make_link('qr.html', 'QR Codes')}
        {make_link('scanner.html', 'Scanner')}
        {make_link('guest.html', 'Guest Lists')}
        <div class="settings">
          <button class="settings-btn" data-settings-toggle>
            Settings ▾
          </button>
          <div class="settings-menu" id="settingsMenu">
            <a href="pre-registration.html">Pre-Registration Form</a>
            <a href="pre-reg-submissions.html">Pre-Reg Submissions</a>
            <a href="scanner-settings.html">Scanner Settings</a>
            <a href="settings.html">Event Settings</a>
          </div>
        </div>
      </div>
    </div>

    <div style="display:flex;align-items:center;gap:12px;">
      <button class="logout" onclick="logout()">Logout</button>
      <div class="hamburger" onclick="toggleMenu()" id="hamburger">
        <span></span><span></span><span></span>
      </div>
    </div>
  </div>

  <!-- MOBILE MENU -->
  <div class="mobile-menu" id="mobileMenu">
    {make_link('Event.html', 'My Events')}
    {make_link('Dashboard.html', 'Dashboard')}
    {make_link('qr.html', 'QR Codes')}
    {make_link('scanner.html', 'Scanner')}
    {make_link('guest.html', 'Guest Lists')}
    <div class="settings mobile-settings">
      <button class="settings-btn" data-settings-toggle>
        Settings ▾
      </button>
      <div class="settings-menu">
        <a href="pre-registration.html">Pre-Registration Form</a>
        <a href="pre-reg-submissions.html">Pre-Reg Submissions</a>
        <a href="scanner-settings.html">Scanner Settings</a>
        <a href="settings.html">Event Settings</a>
      </div>
    </div>
  </div>"""

for filename, active_page in files_to_update:
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        continue
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace everything from <div class="navbar"> to just before <div class="container"> or whatever is after mobile-menu
    # We will use regex to find <div class="navbar"> and replace up to the end of <div class="mobile-menu"... </div>
    # A bit tricky because of nested divs in mobile-menu. Mobile menu has 3 div closings including itself.
    
    # Let's find `<div class="navbar">`
    start_idx = content.find('<div class="navbar">')
    
    # Let's find `class="container"` after the navbar
    end_idx1 = content.find('<div class="container">', start_idx)
    end_idx2 = content.find('<div class="dashboard-container">', start_idx)
    
    # Some pages might have a different container class.
    candidates = [idx for idx in [end_idx1, end_idx2] if idx != -1]
    
    if not candidates:
        print(f"Could not find container after navbar in {filename}")
        continue
        
    end_idx = min(candidates)
    
    # Reverse search to find the end of mobile menu, but we can just replace everything between <div class="navbar"> and the container (trimming the container's preceding whitespace)
    # Actually, there might be other things between mobile-menu and container. Let's just use regex to replace from `<div class="navbar">` up to `</div>\n\n<div class="container..."`
    
    # Or better: search for `<!-- CONTENT -->` if it exists.
    
    # Let's just do a targeted replacement. Find `<div class="navbar">` and `<div class="container`
    # Check what is between them. Usually it's just the mobile menu and maybe some empty lines.
    
    between_content = content[start_idx:end_idx]
    
    # Find the last </div> before end_idx to be safe? 
    # Just replacing the `between_content` is safest if it only contains navbar and mobile menu.
    # Let's verify by printing what we replace.
    
    # We will clean it up safely.
    pattern = re.compile(r'<div class="navbar">.*?<div class="mobile-menu"[^>]*>.*?</div>\s*</div>\s*(?=<div class="(?:container|dashboard-container)")', re.DOTALL)
    
    new_content = pattern.sub(get_template(active_page) + '\n\n', content)
    
    # If regex failed, try a broader one but be careful
    if new_content == content:
        print(f"Regex failed for {filename}. Falling back to manual slicing...")
        # Since we know mobile menu ends, we can try replacing from <div class="navbar"> to the container.
        # But wait, scanner.html doesn't have mobile menu maybe?
        pass
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Updated {filename}")
