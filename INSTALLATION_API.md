# Dependances Python de l'orchestrateur (Option B - serveur local)
# Installation : pip install -r requirements.txt
anthropic>=0.109
weasyprint>=60
cairosvg>=2.7

# Dependances systeme NON pip (a installer separement) :
#   - LibreOffice (conversion DOCX -> PDF)        : apt-get install libreoffice
#   - Polices du kit (kit/polices/*.ttf)          : copier dans ~/.fonts puis fc-cache -f
#   - Bibliotheques systeme de weasyprint (selon l'OS) :
#       Debian/Ubuntu : apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
