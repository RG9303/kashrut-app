import re

with open('src/app/calendario/page.tsx', 'r') as f:
    content = f.read()

# Replace Spanish links
content = content.replace("pesajLink: 'Ver Mega-Guía de Pesaj',",
    "pesajLink: 'Ver Mega-Guía de Pesaj',\n    purimLink: 'Ver Mega-Guía de Purim',\n    shavuotLink: 'Ver Mega-Guía de Shavuot',\n    roshLink: 'Ver Mega-Guía de Rosh Hashaná',\n    kipurLink: 'Ver Mega-Guía de Yom Kipur',\n    sukotLink: 'Ver Mega-Guía de Sukot',\n    janucaLink: 'Ver Mega-Guía de Janucá',")

# Replace English links
content = content.replace("pesajLink: 'View Pesach Mega-Guide',",
    "pesajLink: 'View Pesach Mega-Guide',\n    purimLink: 'View Purim Mega-Guide',\n    shavuotLink: 'View Shavuot Mega-Guide',\n    roshLink: 'View Rosh Hashanah Mega-Guide',\n    kipurLink: 'View Yom Kippur Mega-Guide',\n    sukotLink: 'View Sukkot Mega-Guide',\n    janucaLink: 'View Hanukkah Mega-Guide',")

# Replace in timeline array
def replace_timeline(id_name, link_var):
    global content
    
    pattern = rf"(id:\s*'{id_name}'.*?linkText:\s*)null(,\s*linkHref:\s*)null"
    replacement = rf"\1t.{link_var}\2'/chaguim'"
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

replace_timeline('purim', 'purimLink')
replace_timeline('shavuot', 'shavuotLink')
replace_timeline('rosh-hashana', 'roshLink')
replace_timeline('yom-kipur', 'kipurLink')
replace_timeline('sukot', 'sukotLink')
replace_timeline('januca', 'janucaLink')

with open('src/app/calendario/page.tsx', 'w') as f:
    f.write(content)
print("Updated calendario links")
