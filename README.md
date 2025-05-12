# ArisIA
Tu asistente de IA 100% local y privado 
Características principales
Compatibilidad multiplataforma: Soporta Ubuntu/Debian, Fedora/RHEL y Arch/Manjaro

# Instalación completa:

Primero ejecuta el setup.py como lo harías normalmente

python3 setup.py install --user

Una vez que termine la instalación principal, ejecuta el script de instalación manual

python3 install_python_deps.py

# Instalar pip 
sudo apt-get update

sudo apt-get install -y python3-pip python3-venv

sudo apt-get install -y git python3-dev build-essential curl

python3 -m pip install --user --upgrade pip setuptools wheel

python3 -m pip install --user

# Para Debian/Ubuntu:
sudo apt-get install python3-tk

# Para Fedora:
sudo dnf install python3-tkinter

# Para Arch Linux:
sudo pacman -S tk

# Para CentOS/RHEL:
sudo yum install python3-tkinter

# Verificar la instalación:
python3 -m tkinter -c "tk._test()"

# Prueba que el comando funciona
arisia --version

# Instala en modo usuario
python3 setup.py install --user

# Verifica la instalación:
ls ~/.arisia/models/base/  # Deberías ver los archivos del modelo
python3 -c "from transformers import GPT2LMHeadModel; print('✔ IA lista!')"

# Dar permisos de ejecución (si no los tiene)
chmod +x setup.py

# Reaunudar Instalacion Manual
# Activa el entorno virtual
source ~/.arisia/venv/bin/activate

# Reanuda la instalación con más reintentos y tiempo de espera
pip install --upgrade --retries 10 --timeout 120 \
torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu \
transformers>=4.30.0 \
sentencepiece>=0.1.95 \
fastapi>=0.95.0 \
uvicorn>=0.21.0 \
requests>=2.28.0

# Ejecutar (como usuario normal, NO root)
./setup.py

