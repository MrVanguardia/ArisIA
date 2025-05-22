![V](https://github.com/user-attachments/assets/822dc5b5-01b3-4298-9f60-0eaa1d88b4d6)
# ArisIA
Tu asistente de IA 100% local y privado 
Características principales
Compatibilidad multiplataforma: Soporta Ubuntu/Debian, Fedora y Arch

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

pip instala transformadores de antorcha pieza de sentencia

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

# Requisitos Adicionales

Para esta versión necesitamos instalar:

pip insta transformadores de antorcha

# Activar el entorno virtual de ArisIA:

ls -ld/opt/arisia/venv

sudo chown -R $USUARIO:$USUARIO/opt/arisia/venv

sudo chmod -R u+rwX/opt/arisia/venv

fuente/opt/arisia/venv/bin/activate

pip install --forzar-reinstalar transformadores de antorcha

pip insta transformadores de antorcha

# 2 Pasos correctos para ejecutar installer.sh:


Asegurate de que el script tiene permisos de ejecución:


chmod +x instalador.sh


# 3 requiere permisos de raíz (sudo):


sudo ./installer.sh

# Para DESINSTALAR ARISIA

sudo arisia --uninstall

# Desistalar modelos

# Opción A: Borrar manualmente el modelo

rm -rf ~/.cache/huggingface/hub/models--PlanTL-GOB-ES--bertin-gpt-j-6B

(O usa sudo si los permisos lo requieren).

# Opción B: Borrar toda la caché de Hugging Face (si no necesitas otros modelos)

rm -rf ~/.cache/huggingface/
