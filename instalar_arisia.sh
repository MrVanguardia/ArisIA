#!/bin/bash
# INSTALADOR ARISIA PARA UBUNTU/DEBIAN
# Versión 2.1 - Compatible con Ubuntu 20.04+ y Debian 11+

# ===== CONFIGURACIÓN =====
VERSION="2.1"
DIR_INSTALACION="$HOME/.arisia"
REPO_URL="https://github.com/tu_usuario/arisia.git"
MODELO_URL="https://huggingface.co/datificate/gpt2-small-spanish"
PYTHON_VER="python3.10"

# Colores
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m'

# ===== FUNCIONES =====
instalar_dependencias() {
    echo -e "${AZUL}[+] Actualizando paquetes...${NC}"
    sudo apt-get update > /dev/null 2>&1

    local dependencias=(
        git
        python3-pip
        python3-venv
        python3-dev
        build-essential
        libopenblas-dev
    )

    echo -e "${AZUL}[+] Instalando dependencias del sistema...${NC}"
    sudo apt-get install -y "${dependencias[@]}" > /dev/null 2>&1

    if ! command -v $PYTHON_VER &> /dev/null; then
        echo -e "${AMARILLO}[!] Python 3.10 no detectado, instalando...${NC}"
        sudo apt-get install -y $PYTHON_VER > /dev/null 2>&1
    fi
}

crear_entorno_virtual() {
    echo -e "${AZUL}[+] Creando entorno virtual Python...${NC}"
    $PYTHON_VER -m venv "$DIR_INSTALACION/venv"
    source "$DIR_INSTALACION/venv/bin/activate"
}

instalar_paquetes_python() {
    local paquetes=(
        torch==2.0.1
        transformers==4.30.2
        sentencepiece==0.1.99
        fastapi==0.95.2
        uvicorn==0.22.0
    )

    echo -e "${AZUL}[+] Instalando paquetes Python...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    pip install "${paquetes[@]}" > /dev/null 2>&1
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
echo -e "${NC}${AMARILLO}          Instalador para Ubuntu/Debian v$VERSION${NC}"
echo -e "${AZUL}===============================================${NC}"

# Verificar sistema
if ! grep -qEi "(ubuntu|debian)" /etc/*release; then
    echo -e "${ROJO}[ERROR] Este script solo funciona en Ubuntu/Debian${NC}"
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
echo -e "  - Terminal: Ejecuta 'arisia'"
echo -e "  - API REST: ${DIR_INSTALACION}/venv/bin/python ${DIR_INSTALACION}/interfaces/api.py"
echo -e "\n${AMARILLO}Reinicia tu terminal para usar el comando 'arisia'${NC}"