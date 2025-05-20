# ArisIA
Tu asistente de IA 100% local y privado 
Características principales
Compatibilidad multiplataforma: Soporta Ubuntu/Debian, Fedora/RHEL y Arch/Manjaro

# 1 Dependencias Instalares

sudo dnf install python3 python3-pip python3-devel # Python y pip
sudo dnf install gcc g++ make # Compiladores para las dependencias de armas
sudo dnf install tk-devel # Para tkinter (interfaz gráfica)
sudo dnf install redhat-rpm-config # Ayuda con paquetes Python que necesita compilación
pip3 install --upgrade pip # Actualizar pip primero

# Instala todas las libres del script
pip3 install numpy nltk scikit-learn pandas matplotlib scipy pickle-mixin # Proceso de datos y NLP
pip3 install tkinter customtkinter # Interfaz gráfica
pip3 install solicitud almohada # Para mango de imágenes/HTTP (comunes en proyectos con GUI)
pip3 install regex # Mejora sobre el módulo 're' estar
pip3 install tqdm # Barras de progreso

# Ejecuta en Python

importar nltk
nltk.download('punkt') # Tokenizador básico
nltk.download('palabras de parada') # Palabras comunidades un ignorante en PNL
nltk.download('wordnet') # Diccionario léxico

importar numpy como np
importar nltk
importar sklearn
importar tkinter como tk
importar customtkinter como ctk

imprimir("¡Todas las libertades se importaron correctamente!")

# 2 Pasos correctos para ejecutar installer.sh:
Asegurate de que el script tiene permisos de ejecución:

chmod +x instalador.sh

# 3 Si requiere permisos de raíz (sudo):

sudo ./installer.sh
