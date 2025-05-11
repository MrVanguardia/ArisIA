#!/bin/bash
# INSTALADOR ARISIA PARA FEDORA/RHEL
# Versión 2.2 - Compatible con Fedora 36+ y RHEL 9+

# ===== CONFIGURACIÓN =====
VERSION="2.2"
DIR_INSTALACION="$HOME/.arisia"
REPO_URL="https://github.com/tu_usuario/arisia.git"
MODELO_URL="https://huggingface.co/datificate/gpt2-small-spanish"
PYTHON_VER="python3.11"

# Colores
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m'

# ===== FUNCIONES =====
instalar_dependencias() {
    echo -e "${AZUL}[+] Actualizando paquetes...${NC}"
    sudo dnf update -y > /dev/null 2>&1

    local dependencias=(
        git
        python3-pip
        python3-virtualenv
        python3-devel
        gcc-c++
        make
        cmake
        openblas-devel
    )

    echo -e "${AZUL}[+] Instalando dependencias del sistema...${NC}"
    sudo dnf install -y "${dependencias[@]}" > /dev/null 2>&1

    # Para RHEL/CentOS 8 necesitamos habilitar PowerTools
    if grep -q "CentOS Linux 8" /etc/redhat-release; then
        sudo dnf config-manager --set-enabled powertools > /dev/null 2>&1
    fi
}

crear_entorno_virtual() {
    echo -e "${AZUL}[+] Creando entorno virtual Python...${NC}"
    $PYTHON_VER -m venv "$DIR_INSTALACION/venv"
    source "$DIR_INSTALACION/venv/bin/activate"
}

instalar_paquetes_python() {
    local paquetes=(
        torch==2.1.0
        transformers==4.33.1
        sentencepiece==0.1.99
        fastapi==0.103.1
        uvicorn==0.23.2
    )

    echo -e "${AZUL}[+] Instalando paquetes Python...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    
    # Instalación optimizada para arquitectura
    local arch=$(uname -m)
    if [ "$arch" == "x86_64" ]; then
        pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu > /dev/null 2>&1
    else
        pip install "${paquetes[@]}" > /dev/null 2>&1
    fi
}

clonar_repositorio() {
    echo -e "${AZUL}[+] Clonando repositorio ARISIA...${NC}"
    if [ -d "$DIR_INSTALACION" ]; then
        echo -e "${AMARILLO}[!] Directorio existente detectado, actualizando...${NC}"
        cd "$DIR_INSTALACION" && git pull > /dev/null 2>&1
    else
        git clone --depth 1 "$REPO_URL" "$DIR_INSTALACION" > /dev/null 2>&1
    fi
}

descargar_modelo() {
    echo -e "${AZUL}[+] Configurando modelo de lenguaje...${NC}"
    mkdir -p "$DIR_INSTALACION/modelos"
    
    if [ ! -d "$DIR_INSTALACION/modelos/base" ]; then
        echo -e "${AMARILLO}[!] Descargando modelo (≈300MB)...${NC}"
        python -c "
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model = GPT2LMHeadModel.from_pretrained('$MODELO_URL')
tokenizer = GPT2Tokenizer.from_pretrained('$MODELO_URL')
model.save_pretrained('$DIR_INSTALACION/modelos/base')
tokenizer.save_pretrained('$DIR_INSTALACION/modelos/base')
print('Modelo configurado')
"
    else
        echo -e "${VERDE}[✓] Modelo ya existe${NC}"
    fi
}

configurar_accesos() {
    echo -e "${AZUL}[+] Configurando accesos directos...${NC}"
    
    # Archivo .desktop
    cat > ~/.local/share/applications/arisia.desktop <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=ARISIA
Comment=IA Local Privada
Exec=$DIR_INSTALACION/venv/bin/python $DIR_INSTALACION/interfaces/gui.py
Icon=$DIR_INSTALACION/assets/icon.png
Terminal=false
Categories=Utility;Science;AI;
Keywords=AI;IA;Local;
EOL

    # Alias para terminal
    if ! grep -q "alias arisia=" ~/.bashrc; then
        echo "alias arisia='$DIR_INSTALACION/venv/bin/python $DIR_INSTALACION/interfaces/cli.py'" >> ~/.bashrc
    fi

    # Permisos
    chmod +x "$DIR_INSTALACION"/interfaces/*.py
    chmod +x ~/.local/share/applications/arisia.desktop
    
    # Actualizar base de datos de aplicaciones
    update-desktop-database ~/.local/share/applications > /dev/null 2>&1
}

# ===== EJECUCIÓN PRINCIPAL =====
clear
echo -e "${AZUL}"
echo "   █████╗ ██████╗ ██╗███████╗██╗ █████╗ "
echo "  ██╔══██╗██╔══██╗██║██╔════╝██║██╔══██╗"
echo "  ███████║██████╔╝██║███████╗██║███████║"
echo "  ██╔══██║██╔══██╗██║╚════██║██║██╔══██║"
echo "  ██║  ██║██║  ██║██║███████║██║██║  ██║"
echo "  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝"
echo -e "${NC}${AMARILLO}          Instalador para Fedora/RHEL v$VERSION${NC}"
echo -e "${AZUL}===============================================${NC}"

# Verificar sistema
if ! grep -qEi "fedora|rhel|centos|almalinux|rocky" /etc/*release; then
    echo -e "${ROJO}[ERROR] Este script solo funciona en Fedora/RHEL y derivados${NC}"
    exit 1
fi

# Instalación
instalar_dependencias
crear_entorno_virtual
instalar_paquetes_python
clonar_repositorio
descargar_modelo
configurar_accesos

echo -e "\n${VERDE}[✔] Instalación completada!${NC}"
echo -e "\n${AZUL}Opciones de uso:${NC}"
echo -e "  - Menú aplicaciones: Busca 'ARISIA'"
echo -e "  - Terminal: Ejecuta 'arisia' (en nueva sesión)"
echo -e "  - API REST: ${DIR_INSTALACION}/venv/bin/python ${DIR_INSTALACION}/interfaces/api.py"
echo -e "\n${AMARILLO}Reinicia tu terminal para usar el comando 'arisia'${NC}"