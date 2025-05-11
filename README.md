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

# Para Instalar ArisIA necesitas ejecutar este comando en la terminal (Debes tener el setup descargado)
python3 setup.py

# Verifica que el modelo se descargó correctamente
ls ~/.arisia/models/base/

# Prueba que el comando funciona
arisia --version

# Crea un entorno virtual (evita problemas de permisos)
python3 -m venv ~/.arisia_venv
source ~/.arisia_venv/bin/activate

# Instala en modo usuario
python3 setup.py install --user

# Descarga este instalador simplificado:
wget https://raw.githubusercontent.com/tu_usuario/arisia/main/install_local.sh
chmod +x install_local.sh
./install_local.sh

# Verifica la instalación:
ls ~/.arisia/models/base/  # Deberías ver los archivos del modelo
python3 -c "from transformers import GPT2LMHeadModel; print('✔ IA lista!')"
