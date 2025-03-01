import os
import subprocess

def setup_virtual_env():
    # Nombre del entorno virtual
    venv_name = "venv"
    
    # Crear entorno virtual
    subprocess.run(["python", "-m", "venv", venv_name])
    
    # Activar el entorno virtual
    activate_script = os.path.join(venv_name, "Scripts", "activate")
    
    print(f"Para activar el entorno virtual, ejecuta: {activate_script}")
    
    # Instalar paquetes necesarios
    subprocess.run([os.path.join(venv_name, "Scripts", "pip"), "install", "opencv-python", "matplotlib", "numpy", "pandas", "jupyter"])
    
    print("Entorno virtual configurado con éxito y paquetes instalados.")

if __name__ == "__main__":
    setup_virtual_env()
