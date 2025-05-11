# ArisIA
Tu asistente de IA 100% local y privado

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
