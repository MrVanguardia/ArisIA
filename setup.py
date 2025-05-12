#!/usr/bin/env python3
# ARISIA INSTALLER - UNIVERSAL LINUX VERSION
import os
import sys
import platform
import subprocess
from pathlib import Path
from setuptools import setup, find_packages

# Configuración global
APP_NAME = "arisia"
VERSION = "3.0.3"
PYTHON_REQUIRES = ">=3.8"
MODEL_URL = "https://huggingface.co/datificate/gpt2-small-spanish"
INSTALL_PATH = Path.home() / f".{APP_NAME}"

class UniversalInstaller:
    @staticmethod
    def run():
        print(f"\n🔵 Instalando {APP_NAME} v{VERSION}...\n")
        
        # 1. Verificar e instalar requisitos básicos
        UniversalInstaller.install_essential_tools()
        
        # 2. Detectar distribución
        distro = UniversalInstaller.detect_distro()
        print(f"✔ Sistema detectado: {distro['name']} {distro['version']}")
        
        # 3. Instalar dependencias específicas
        UniversalInstaller.install_system_deps(distro)
        
        # 4. Configurar entorno Python
        UniversalInstaller.ensure_python_environment()
        
        # 5. Instalar componentes principales
        UniversalInstaller.create_dirs()
        UniversalInstaller.setup_python_env()
        UniversalInstaller.download_model()
        UniversalInstaller.configure_launchers()
        
        print(f"\n🎉 ¡Instalación completada en {INSTALL_PATH}!")
        print("   Ejecuta 'arisia' en tu terminal o búscala en el menú de aplicaciones")
        print("\n⚠️  IMPORTANTE: Ahora debes ejecutar el script de instalación manual de paquetes Python")
        print("   que se te proporcionó junto con este instalador.")

    @staticmethod
    def install_essential_tools():
        """Instala herramientas esenciales como git, curl y pip"""
        print("🛠️  Instalando herramientas esenciales...")
        try:
            # Verificar si pip está instalado
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            print("⚠️  Pip no encontrado, instalando...")
            try:
                subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            except Exception as e:
                print(f"❌ Error instalando pip: {e}")
                sys.exit(1)

    @staticmethod
    def detect_distro():
        """Detección mejorada de distribución"""
        distro_info = {"name": "Linux", "version": ""}
        try:
            with open("/etc/os-release") as f:
                content = f.read()
                
            if "debian" in content.lower():
                distro_info["name"] = "Debian"
            elif "ubuntu" in content.lower():
                distro_info["name"] = "Ubuntu"
            elif "fedora" in content.lower():
                distro_info["name"] = "Fedora"
            elif "arch" in content.lower():
                distro_info["name"] = "Arch"
            elif "centos" in content.lower() or "rhel" in content.lower():
                distro_info["name"] = "CentOS/RHEL"
            elif "opensuse" in content.lower():
                distro_info["name"] = "openSUSE"
                
            # Extraer versión
            for line in content.splitlines():
                if "VERSION_ID=" in line:
                    distro_info["version"] = line.split("=")[1].strip('"')
                    break
                    
        except FileNotFoundError:
            pass
            
        return distro_info

    @staticmethod
    def install_system_deps(distro):
        """Instala dependencias del sistema para todas las distros principales"""
        deps = {
            "debian": ["git", "python3-venv", "python3-dev", "build-essential", "curl"],
            "ubuntu": ["git", "python3-venv", "python3-dev", "build-essential", "curl"],
            "fedora": ["git", "python3-devel", "gcc-c++", "make", "curl"],
            "arch": ["git", "python", "base-devel", "curl"],
            "centos/rhel": ["git", "python3-devel", "gcc-c++", "make", "curl"],
            "opensuse": ["git", "python3-devel", "gcc-c++", "make", "curl"]
        }
        
        cmds = {
            "debian": ["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "-y"],
            "ubuntu": ["sudo", "apt-get", "update", "&&", "sudo", "apt-get", "install", "-y"],
            "fedora": ["sudo", "dnf", "install", "-y"],
            "arch": ["sudo", "pacman", "-Sy", "--noconfirm", "--needed"],
            "centos/rhel": ["sudo", "yum", "install", "-y"],
            "opensuse": ["sudo", "zypper", "install", "-y"]
        }
        
        distro_name = distro["name"].lower()
        for distro_key in deps:
            if distro_key in distro_name:
                print(f"⚙️  Instalando dependencias para {distro['name']}...")
                try:
                    subprocess.run(" ".join(cmds[distro_key] + deps[distro_key]), 
                                 shell=True, check=True)
                    break
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Error instalando dependencias: {e}")
                    print("ℹ️  Intenta instalarlas manualmente con:")
                    print("    " + " ".join(cmds[distro_key] + deps[distro_key]))
                break

    @staticmethod
    def ensure_python_environment():
        """Verifica e instala Python 3.8+ si es necesario"""
        print("🐍 Verificando entorno Python...")
        try:
            # Verificar versión de Python
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            version_str = result.stdout.strip()
            version = tuple(map(int, version_str.split()[1].split('.')[:2]))
            
            if version < (3, 8):
                print(f"❌ Se requiere Python ≥3.8 (tienes {version_str})")
                UniversalInstaller.install_python_modern()
                
        except Exception as e:
            print(f"⚠️  Error verificando Python: {e}")
            UniversalInstaller.install_python_modern()

    @staticmethod
    def install_python_modern():
        """Intenta instalar Python 3.8+ en diferentes distribuciones"""
        print("🔄 Intentando instalar Python moderno...")
        distro = UniversalInstaller.detect_distro()
        
        try:
            if distro["name"].lower() in ["debian", "ubuntu"]:
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3.8"], check=True)
            elif distro["name"].lower() == "fedora":
                subprocess.run(["sudo", "dnf", "install", "-y", "python3.8"], check=True)
            elif distro["name"].lower() == "arch":
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "python"], check=True)
            elif distro["name"].lower() in ["centos", "rhel"]:
                subprocess.run(["sudo", "yum", "install", "-y", "python3.8"], check=True)
            else:
                print("⚠️  No se pudo instalar Python automáticamente en esta distribución")
                print("ℹ️  Por favor instala Python ≥3.8 manualmente")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando Python: {e}")
            sys.exit(1)

    @staticmethod
    def create_dirs():
        """Crea la estructura de directorios necesaria"""
        dirs = [
            INSTALL_PATH,
            INSTALL_PATH / "models",
            INSTALL_PATH / "plugins",
            INSTALL_PATH / "logs",
            INSTALL_PATH / "assets"
        ]
        for d in dirs:
            d.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def setup_python_env():
        """Configura el entorno virtual"""
        venv_path = INSTALL_PATH / "venv"
        
        # Crear entorno virtual si no existe
        if not venv_path.exists():
            print("🐍 Creando entorno virtual Python...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        print("⚠️  La instalación de paquetes Python se realizará manualmente después")

    @staticmethod
    def download_model():
        """Descarga el modelo de lenguaje"""
        model_dir = INSTALL_PATH / "models/base"
        if not (model_dir / "config.json").exists():
            print("🧠 Descargando modelo de lenguaje...")
            try:
                download_script = f"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
os.makedirs('{model_dir}', exist_ok=True)
model = GPT2LMHeadModel.from_pretrained('{MODEL_URL}')
tokenizer = GPT2Tokenizer.from_pretrained('{MODEL_URL}')
model.save_pretrained('{model_dir}')
tokenizer.save_pretrained('{model_dir}')
print('✅ Modelo descargado correctamente')
                """
                subprocess.run(
                    [str(INSTALL_PATH / "venv" / "bin" / "python"), "-c", download_script],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"❌ Error descargando el modelo: {e}")
                print("ℹ️  Puedes intentar descargarlo manualmente después con:")
                print(f"    arisia download-model")

    @staticmethod
    def configure_launchers():
        """Configura los lanzadores de aplicación"""
        # Crear acceso directo para escritorio
        desktop_file = Path.home() / ".local/share/applications/arisia.desktop"
        desktop_content = f"""
[Desktop Entry]
Version=1.0
Type=Application
Name=ARISIA
Comment=IA Local con Privacidad Total
Exec={INSTALL_PATH}/venv/bin/python {INSTALL_PATH}/interfaces/gui.py
Icon={INSTALL_PATH}/assets/icon.png
Terminal=false
Categories=Utility;Science;AI;
Keywords=AI;IA;Local;
        """
        
        try:
            desktop_file.parent.mkdir(exist_ok=True, parents=True)
            desktop_file.write_text(desktop_content)
            desktop_file.chmod(0o755)
            print(f"🚀 Acceso directo creado en {desktop_file}")
        except Exception as e:
            print(f"⚠️  No se pudo crear el acceso directo: {e}")

        # Configurar alias en shells
        alias_line = f"alias arisia='{INSTALL_PATH}/venv/bin/python {INSTALL_PATH}/interfaces/cli.py'"
        
        # Bash
        bashrc = Path.home() / ".bashrc"
        try:
            if not any("arisia" in line for line in bashrc.read_text().splitlines()):
                with bashrc.open("a") as f:
                    f.write(f"\n# ARISIA Alias\n{alias_line}\n")
        except Exception as e:
            print(f"⚠️  No se pudo configurar alias en .bashrc: {e}")
        
        # Zsh
        zshrc = Path.home() / ".zshrc"
        try:
            if zshrc.exists():
                if not any("arisia" in line for line in zshrc.read_text().splitlines()):
                    with zshrc.open("a") as f:
                        f.write(f"\n# ARISIA Alias\n{alias_line}\n")
        except Exception as e:
            print(f"⚠️  No se pudo configurar alias en .zshrc: {e}")

def main():
    if platform.system() != "Linux":
        print("❌ Este instalador solo funciona en Linux", file=sys.stderr)
        sys.exit(1)
        
    if os.geteuid() == 0:
        print("⚠️  No ejecutes este instalador como root/sudo", file=sys.stderr)
        sys.exit(1)
        
    # Configuración del paquete Python
    setup(
        name=APP_NAME,
        version=VERSION,
        python_requires=PYTHON_REQUIRES,
        packages=find_packages(),
        include_package_data=True,
        install_requires=[],  # Las dependencias se manejan manualmente
        entry_points={
            "console_scripts": [
                f"{APP_NAME}={APP_NAME}.cli:main",
                f"{APP_NAME}-download-model={APP_NAME}.model:download"
            ],
        },
    )
    
    # Ejecutar instalador personalizado
    UniversalInstaller.run()

if __name__ == "__main__":
    main()
