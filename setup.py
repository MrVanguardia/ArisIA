#!/usr/bin/env python3
# ARISIA INSTALLER - setup.py
# Versión 3.0 (Compatibilidad: Ubuntu/Debian, Fedora/RHEL, Arch/Manjaro)

import os
import sys
import platform
import subprocess
from pathlib import Path
from setuptools import setup, find_packages

# Configuración global
APP_NAME = "arisia"
VERSION = "3.0.1"
PYTHON_REQUIRES = ">=3.8"
MODEL_URL = "https://huggingface.co/datificate/gpt2-small-spanish"
INSTALL_PATH = Path.home() / f".{APP_NAME}"

class LinuxInstaller:
    @staticmethod
    def run():
        print(f"\n🔵 Instalando {APP_NAME} v{VERSION}...\n")
        
        # 1. Verificar sistema
        distro = LinuxInstaller.detect_distro()
        print(f"✔ Detectado: {distro['name']} {distro['version']}")
        
        # 2. Crear estructura de directorios
        LinuxInstaller.create_dirs()
        
        # 3. Instalar dependencias del sistema
        LinuxInstaller.install_system_deps(distro)
        
        # 4. Configurar entorno Python
        LinuxInstaller.setup_python_env()
        
        # 5. Instalar modelo de lenguaje
        LinuxInstaller.download_model()
        
        # 6. Configurar accesos
        LinuxInstaller.configure_launchers()
        
        print(f"\n🎉 {APP_NAME} instalado correctamente en {INSTALL_PATH}")
        print("   Ejecuta 'arisia' en tu terminal o búscala en el menú de aplicaciones")

    @staticmethod
    def detect_distro():
        distro_info = {
            "name": platform.system(),
            "version": platform.version()
        }
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if "PRETTY_NAME" in line:
                        distro_info["name"] = line.split("=")[1].strip().strip('"')
                    elif "VERSION_ID" in line:
                        distro_info["version"] = line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            pass
        return distro_info

    @staticmethod
    def create_dirs():
        dirs = [
            INSTALL_PATH,
            INSTALL_PATH / "models",
            INSTALL_PATH / "plugins",
            INSTALL_PATH / "logs"
        ]
        for d in dirs:
            d.mkdir(exist_ok=True)

    @staticmethod
    def install_system_deps(distro):
        deps = {
            "ubuntu": ["git", "python3-venv", "python3-dev", "build-essential"],
            "debian": ["git", "python3-venv", "python3-dev", "build-essential"],
            "fedora": ["git", "python3-devel", "gcc-c++", "make"],
            "arch": ["git", "python", "base-devel"]
        }
        
        pkg_manager = {
            "ubuntu": "apt-get install -y",
            "debian": "apt-get install -y",
            "fedora": "dnf install -y",
            "arch": "pacman -S --noconfirm --needed"
        }
        
        distro_name = distro["name"].lower()
        for key in deps:
            if key in distro_name:
                cmd = f"sudo {pkg_manager[key]} {' '.join(deps[key])}"
                print(f"⚙️ Instalando dependencias: {cmd}")
                subprocess.run(cmd, shell=True, check=True)
                break

    @staticmethod
    def setup_python_env():
        venv_path = INSTALL_PATH / "venv"
        if not (venv_path / "bin/python").exists():
            print("🐍 Creando entorno virtual Python...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        pip_cmd = [str(venv_path / "bin/pip"), "install", "--upgrade", "pip"]
        subprocess.run(pip_cmd, check=True)
        
        requirements = [
            "torch>=2.0.0",
            "transformers>=4.30.0",
            "sentencepiece>=0.1.95",
            "fastapi>=0.95.0",
            "uvicorn>=0.21.0"
        ]
        
        print("📦 Instalando dependencias Python...")
        subprocess.run([str(venv_path / "bin/pip"), "install"] + requirements, check=True)

    @staticmethod
    def download_model():
        model_dir = INSTALL_PATH / "models/base"
        if not (model_dir / "config.json").exists():
            print("🧠 Descargando modelo de lenguaje (≈300MB)...")
            download_script = f"""
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model = GPT2LMHeadModel.from_pretrained('{MODEL_URL}')
tokenizer = GPT2Tokenizer.from_pretrained('{MODEL_URL}')
model.save_pretrained('{model_dir}')
tokenizer.save_pretrained('{model_dir}')
            """
            subprocess.run(
                [str(INSTALL_PATH / "venv/bin/python"), "-c", download_script],
                check=True
            )

    @staticmethod
    def configure_launchers():
        # Desktop file
        desktop_file = Path.home() / ".local/share/applications/arisia.desktop"
        desktop_file.write_text(f"""
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
        """)
        
        # Bash alias
        bashrc = Path.home() / ".bashrc"
        alias_line = f"alias arisia='{INSTALL_PATH}/venv/bin/python {INSTALL_PATH}/interfaces/cli.py'"
        if not any("arisia" in line for line in bashrc.read_text().splitlines()):
            with bashrc.open("a") as f:
                f.write(f"\n{alias_line}\n")
        
        # Zsh alias (si existe)
        zshrc = Path.home() / ".zshrc"
        if zshrc.exists():
            if not any("arisia" in line for line in zshrc.read_text().splitlines()):
                with zshrc.open("a") as f:
                    f.write(f"\n{alias_line}\n")

        # Permisos
        desktop_file.chmod(0o755)
        print(f"🚀 Accesos directos configurados en {desktop_file}")

def main():
    if platform.system() != "Linux":
        print("❌ Este instalador solo funciona en Linux", file=sys.stderr)
        sys.exit(1)
        
    if os.geteuid() == 0:
        print("⚠️  No ejecutes este instalador como root/sudo", file=sys.stderr)
        sys.exit(1)
        
    setup(
        name=APP_NAME,
        version=VERSION,
        python_requires=PYTHON_REQUIRES,
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            "torch>=2.0.0",
            "transformers>=4.30.0",
            "sentencepiece>=0.1.95"
        ],
        entry_points={
            "console_scripts": [
                "arisia = arisia.cli:main",
            ],
        },
    )
    
    # Ejecutar instalador personalizado
    LinuxInstaller.run()

if __name__ == "__main__":
    main()