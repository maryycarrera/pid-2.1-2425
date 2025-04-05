# Comparativa de imágenes en base a su nitidez, su luminosidad y su contraste y mejora del brillo de imágenes

1. [Contenido del repositorio](#contenido-del-repositorio)
2. [Cómo usar el repositorio](#cómo-usar-el-repositorio)
3. [Contribuciones](#contribuciones)

---

## Contenido del repositorio

Este repositorio contiene una serie de cuadernos de Jupyter que se han utilizado para experimentar con los métodos estudiados. Dichos experimentos se han implementado en cuadernos diferentes según el objeto de estudio (nitidez, luminosidad o contraste) y según el método aplicado en cada uno (obtención de la nitidez usando filtros o mediante la transformada de wavelet).

Las imágenes utilizadas para la experimentación se encuentran en el directorio `/imagenes`. En la carpeta `/imagenes_procesadas` se pueden ver los resultados de los experimentos, siguiendo una estructura similar a la de la carpeta `/imagenes`.

Por otra parte, se ha desarrollado una aplicación web a pequeña escala, en la que se han implementado los métodos estudiados con el objetivo de ponerlos a prueba más fácilmente. Esta aplicación separa la comparación y selección de imágenes en base a sus parámetros (nitidez, luminosidad o contraste) de la mejora del brillo de una imagen. La interfaz de usuario es intuitiva y la lógica de la aplicación permite una rápida adaptación a su uso.

---

## Cómo usar el repositorio

Las instrucciones de instalación y uso de este repositorio están explicadas para sistemas operativos Windows, dado que es el SO en el que se ha desarrollado el proyecto. Para comenzar a utilizar los recursos desarrollados en este repositorio, se debe crear primero un entorno virtual. Todos los comandos deben ejecutarse en una terminal de Windows.

1. Crear un entorno virtual en Windows.
    ```
    python -m venv venv
    ```

2. Activar el entorno virtual.
    ```
    venv\Scripts\activate
    ```

3. Instalar los paquetes necesarios.
    ```
    pip install -r requirements.txt
    ```

4. Opcionalmente, se puede utilizar el paquete `nbstripout`, que sirve para limpiar los metadatos de los notebooks antes de subirlos al repositorio local. Para utilizar esta herramienta, ejecutar el seguiente comando:
    ```
    nbstripout --install
    ```

5. Para desactivar este paquete:
    ```
    nbstripout --uninstall
    ```

6. Desactivar el entorno virtual.
    ```
    deactivate
    ```

Una vez seguidos estos pasos, ya se pueden ejecutar los notebooks de Jupyter. Basta con seleccionar el kernel de Python correspondiente al entorno virtual. Se recomienda comenzar con el notebook `configuración_inicial.ipynb`.

Si se desea ejecutar la aplicación web, habrá que ejecutar el siguiente comando, con el entorno virtual activado:

```
streamlit run app.py
```

Esto ejecutará la aplicación en la ruta por defecto `http://localhost:8501` y se abrirá en una ventana del navegador web.

---

## Contribuciones

Para comenzar a contribuir en este repositorio, se debe hacer un fork del mismo. Cualquier aportación debe hacerse por medio de Pull Requests.

Gracias a nuestros contribuidores:

<a href="https://github.com/maryycarrera/pid-2.1-2425/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=maryycarrera/pid-2.1-2425" />
</a>