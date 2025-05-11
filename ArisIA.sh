#!/bin/bash
# INSTALADOR OFICIAL DE ARISIA - IA Local para Linux

# ===== CONSTANTES =====
VERSION="1.0"
REPO_URL="https://github.com/tu_usuario/arisia_repo"
MODELO_BASE="datificate/gpt2-small-spanish"
DIR_INSTALACION="$HOME/.arisia"
DIR_APLICACIONES="$HOME/.local/share/applications"

# ===== CONFIGURACIÓN DE COLORES =====
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m' # Sin color

# ===== FUNCIONES =====

mostrar_banner() {
    clear
    echo -e "${AZUL}
    █████╗ ██████╗ ██╗███████╗██╗ █████╗ 
   ██╔══██╗██╔══██╗██║██╔════╝██║██╔══██╗
   ███████║██████╔╝██║███████╗██║███████║
   ██╔══██║██╔══██╗██║╚════██║██║██╔══██║
   ██║  ██║██║  ██║██║███████║██║██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝
   ${NC}"
    echo -e "${AMARILLO}          Versión ${VERSION} - IA Local para Linux${NC}\n"
}

verificar_dependencias() {
    local faltantes=()
    
    echo -e "${AZUL}[+] Verificando dependencias...${NC}"
    
    # Python 3
    if ! command -v python3 &>/dev/null; then
        faltantes+=("python3")
    fi
    
    # pip
    if ! command -v pip3 &>/dev/null; then
        faltantes+=("python3-pip")
    fi
    
    # git
    if ! command -v git &>/dev/null; then
        faltantes+=("git")
    fi
    
    if [ ${#faltantes[@]} -ne 0 ]; then
        echo -e "${ROJO}[!] Faltan dependencias:${NC}"
        for pkg in "${faltantes[@]}"; do
            echo -e "  - ${pkg}"
        done
        
        if [[ -f /etc/debian_version ]]; then
            echo -e "\n${AMARILLO}Instalar con:${NC}"
            echo -e "sudo apt install ${faltantes[*]}"
        elif [[ -f /etc/redhat-release ]]; then
            echo -e "\n${AMARILLO}Instalar con:${NC}"
            echo -e "sudo dnf install ${faltantes[*]}"
        elif [[ -f /etc/arch-release ]]; then
            echo -e "\n${AMARILLO}Instalar con:${NC}"
            echo -e "sudo pacman -S ${faltantes[*]}"
        fi
        
        exit 1
    fi
}

instalar_python_deps() {
    echo -e "${AZUL}[+] Instalando dependencias de Python...${NC}"
    
    local requerimientos=(
        "torch"
        "transformers"
        "sentencepiece"
    )
    
    for pkg in "${requerimientos[@]}"; do
        if ! python3 -c "import ${pkg%%==*}" &>/dev/null; then
            echo -e "${AMARILLO}  - Instalando ${pkg}...${NC}"
            pip3 install --user --quiet "${pkg}"
        else
            echo -e "${VERDE}  - ${pkg} ya instalado${NC}"
        fi
    done
}

descargar_arisia() {
    echo -e "${AZUL}[+] Descargando ARISIA...${NC}"
    
    if [[ -d "${DIR_INSTALACION}" ]]; then
        echo -e "${AMARILLO}  - Actualizando instalación existente...${NC}"
        cd "${DIR_INSTALACION}" && git pull
    else
        echo -e "${AMARILLO}  - Clonando repositorio...${NC}"
        git clone --depth 1 "${REPO_URL}" "${DIR_INSTALACION}"
    fi
}

configurar_modelo() {
    echo -e "${AZUL}[+] Configurando modelo de lenguaje...${NC}"
    
    mkdir -p "${DIR_INSTALACION}/modelos"
    
    if [[ ! -d "${DIR_INSTALACION}/modelos/base" ]]; then
        echo -e "${AMARILLO}  - Descargando modelo base (esto puede tomar varios minutos)...${NC}"
        python3 -c "
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model = GPT2LMHeadModel.from_pretrained('${MODELO_BASE}')
tokenizer = GPT2Tokenizer.from_pretrained('${MODELO_BASE}')
model.save_pretrained('${DIR_INSTALACION}/modelos/base')
tokenizer.save_pretrained('${DIR_INSTALACION}/modelos/base')
print('Modelo configurado correctamente')
"
    else
        echo -e "${VERDE}  - Modelo base ya instalado${NC}"
    fi
}

crear_accesos() {
    echo -e "${AZUL}[+] Creando accesos directos...${NC}"
    
    # Directorio de aplicaciones si no existe
    mkdir -p "${DIR_APLICACIONES}"
    
    # Archivo .desktop para la GUI
    cat > "${DIR_APLICACIONES}/arisia.desktop" <<EOL
[Desktop Entry]
Version=1.0
Name=ARISIA
Comment=IA Local para Linux
Exec=python3 ${DIR_INSTALACION}/interfaces/gui.py
Icon=${DIR_INSTALACION}/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;Science;AI;
Keywords=IA;Inteligencia Artificial;Local;
EOL
    
    # Alias para CLI
    if ! grep -q "alias arisia=" "${HOME}/.bashrc"; then
        echo -e "\nalias arisia='python3 ${DIR_INSTALACION}/interfaces/cli.py'" >> "${HOME}/.bashrc"
    fi
    
    # Permisos
    chmod +x "${DIR_INSTALACION}/interfaces/"*.py
}

instalar_plugins() {
    echo -e "${AZUL}[+] Configurando plugins básicos...${NC}"
    
    mkdir -p "${DIR_INSTALACION}/plugins"
    
    # Plugin de traducción básico
    cat > "${DIR_INSTALACION}/plugins/traductor.py" <<EOL
def procesar_texto(texto):
    \"\"\"Plugin de traducción básico\"\"\"
    diccionario = {
        'hello': 'hola',
        'goodbye': 'adiós',
        'thanks': 'gracias'
    }
    for eng, esp in diccionario.items():
        texto = texto.replace(eng, esp)
    return texto
EOL
}

finalizar_instalacion() {
    echo -e "\n${VERDE}[✔] ARISIA se ha instalado correctamente${NC}"
    echo -e "\n${AZUL}Opciones de uso:${NC}"
    echo -e "  - Interfaz gráfica: Busca 'ARISIA' en tu menú de aplicaciones"
    echo -e "  - Terminal: Ejecuta 'arisia' en una nueva sesión"
    echo -e "  - API local: python3 ${DIR_INSTALACION}/interfaces/api.py"
    echo -e "\n${AMARILLO}Directorio de instalación: ${DIR_INSTALACION}${NC}"
}

# ===== EJECUCIÓN PRINCIPAL =====
mostrar_banner
verificar_dependencias
instalar_python_deps
descargar_arisia
configurar_modelo
instalar_plugins
crear_accesos
finalizar_instalacion