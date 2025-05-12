#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# Configuración
INSTALL_PATH = Path.home() / ".arisia"
VENV_PIP = str(INSTALL_PATH / "venv" / "bin" / "pip")

# Lista de paquetes a instalar
PACKAGES = [
    "torch>=2.0.0 --index-url https://download.pytorch.org/whl/cpu",
    "transformers>=4.30.0",
    "sentencepiece>=0.1.95",
    "fastapi>=0.95.0",
    "uvicorn>=0.21.0",
    "requests>=2.28.0"
]

def install_packages():
    print("🔵 Instalando paquetes Python en el entorno virtual...\n")
    
    try:
        # Actualizar pip primero
        subprocess.run([VENV_PIP, "install", "--upgrade", "pip"], check=True)
        
        # Instalar paquetes uno por uno
        for pkg in PACKAGES:
            print(f"📦 Instalando {pkg.split()[0]}...")
            cmd = [VENV_PIP, "install"] + pkg.split()
            subprocess.run(cmd, check=True)
        
        print("\n🎉 ¡Paquetes Python instalados correctamente!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error instalando paquetes: {e}")
        print("\nPuedes intentar instalar los paquetes manualmente con:")
        print(f"  {VENV_PIP} install {' '.join(PACKAGES)}")
        sys.exit(1)

if __name__ == "__main__":
    if not (INSTALL_PATH / "venv").exists():
        print("❌ No se encontró el entorno virtual de ARISIA")
        print("   Ejecuta primero el instalador principal (setup.py)")
        sys.exit(1)
    
    install_packages()