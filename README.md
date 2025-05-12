# ArisIA
Tu asistente de IA 100% local y privado 
Características principales
Compatibilidad multiplataforma: Soporta Ubuntu/Debian, Fedora/RHEL y Arch/Manjaro

Instalación completa:

Crea entorno virtual Python

Instala dependencias del sistema y Python

Descarga modelos de lenguaje (~300MB)

Configura accesos directos

Componentes técnicos interesantes
Detección automática de distribución: Usa /etc/os-release para identificar el sistema

Manejo de dependencias: Instala paquetes específicos para cada distro

Modelo de lenguaje: Descarga un modelo GPT-2 en español desde Hugging Face

Configuración de accesos:

Crea un archivo .desktop para el lanzador gráfico

Añade alias en .bashrc y .zshrc

¿Para qué podría servirte?
Como base para desarrollar tu propia aplicación de IA local

Para aprender cómo implementar un instalador multiplataforma en Python

Como ejemplo de integración con modelos de Hugging Face

Para ver cómo gestionar dependencias en diferentes distros Linux

# Instalar pip 
sudo apt-get update

sudo apt-get install -y python3-pip python3-venv

sudo apt-get install -y git python3-dev build-essential curl

python3 -m pip install --user --upgrade pip setuptools wheel

python3 -m pip install --user

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

