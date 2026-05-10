import re

with open('src/app/calendario/page.tsx', 'r') as f:
    content = f.read()

# Replace linkHref: '/chaguim' with linkHref: '/chaguim?jag=x'
def fix_link(id_str):
    global content
    content = re.sub(rf"(id:\s*'{id_str}'.*?linkHref:\s*)'/chaguim'", rf"\1'/chaguim?jag={id_str}'", content, flags=re.DOTALL)

for id_str in ['purim', 'pesaj', 'shavuot', 'rosh-hashana', 'yom-kipur', 'sukot', 'januca']:
    fix_link(id_str)

with open('src/app/calendario/page.tsx', 'w') as f:
    f.write(content)
print("Updated calendario links to include ?jag=...")
