# Comparativa de imágenes en base a su nitidez, su luminosidad y su contraste y mejora del brillo de imágenes

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)
![MIT License](https://img.shields.io/github/license/maryycarrera/pid-2.1-2425)
![Último commit](https://img.shields.io/github/last-commit/maryycarrera/pid-2.1-2425)
![Issues abiertas](https://img.shields.io/github/issues/maryycarrera/pid-2.1-2425)
![Pull Requests abiertas](https://img.shields.io/github/issues-pr/maryycarrera/pid-2.1-2425)


1. [Contenido del repositorio](#contenido-del-repositorio)
2. [Cómo usar el repositorio](#cómo-usar-el-repositorio)
3. [Contribuciones](#contribuciones)

---

## Contenido del repositorio

Este repositorio contiene una serie de cuadernos de Jupyter que se han utilizado para experimentar con los métodos estudiados. Dichos experimentos se han implementado en cuadernos diferentes según el objeto de estudio (nitidez, luminosidad o contraste) y según el método aplicado en cada uno (obtención de la nitidez usando filtros o mediante la transformada de wavelet). También existen tres cuadernos cuya finalidad es evaluar los métodos implementados en base a los resultados obtenidos sobre un banco de imágenes.

Las imágenes utilizadas para la experimentación se encuentran en el directorio `/images`. Las imágenes cuyo nombre termina por `sharp.png`, `blur.png` y `blur_gamma.png` han sido obtenidas de un [banco de imágenes real](https://seungjunnah.github.io/Datasets/gopro.html) y se han utilizado para el cálculo de la nitidez. No se han utilizado todas las imágenes de este banco, sino que se han seleccionado 44 conjuntos de imágenes al azar. Para el cálculo de la luminosidad, se han utilizado todas las imágenes `sharp.png` y se ha aumentado y disminuido su luminosidad para generar imágenes que nosotros supiéramos seguro que iban a tener mayor o menor brillo, de cara a evaluar correctamente el método implementado. Las imágenes así generadas son aquellas cuyo nombre acaba en `bright.png` o `dark.png`. Para el contraste se ha seguido el mismo procedimiento, obteniendo las imágenes cuyo nombre termina en `contrast.png`. En la carpeta `/images_procesadas` se pueden ver los resultados de los experimentos, siguiendo una estructura similar a la de la carpeta `/images`. Por último, en la carpeta `/evaluacion_metodos` se pueden ver las estadísticas de aciertos de los diferentes métodos implementados.

Por otra parte, se ha desarrollado una aplicación web a pequeña escala, en la que se han implementado los métodos estudiados con el objetivo de ponerlos a prueba más fácilmente. Esta aplicación separa la comparación y selección de imágenes en base a sus parámetros (nitidez, luminosidad o contraste) de la mejora del contraste de una imagen. La interfaz de usuario es intuitiva y la lógica de la aplicación permite una rápida adaptación a su uso.

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

4. Opcionalmente, se puede utilizar el paquete `nbstripout`, que sirve para limpiar los metadatos de los notebooks antes de subirlos al repositorio remoto. Para utilizar esta herramienta, ejecutar los siguientes comandos:
    ```
    nbstripout --install
    nbstripout <nombre_del_archivo>.ipynb
    ```

    Para desactivar este paquete:
    ```
    nbstripout --uninstall
    ```

Una vez seguidos estos pasos, ya se pueden ejecutar los notebooks de Jupyter. Basta con seleccionar el kernel de Python correspondiente al entorno virtual. Se recomienda comenzar con el notebook `configuracion_inicial.ipynb`.

Si se desea ejecutar la aplicación web, habrá que ejecutar el siguiente comando, con el entorno virtual activado:

```
streamlit run app.py
```

Esto ejecutará la aplicación en la ruta por defecto `http://localhost:8501` y se abrirá en una ventana del navegador web.

Para desactivar el entorno virtual:
```
deactivate
```

---

## Contribuciones

Para comenzar a contribuir en este repositorio, se debe hacer un fork del mismo. Cualquier aportación debe hacerse por medio de Pull Requests.

Gracias a nuestros contribuidores:

<a href="https://github.com/maryycarrera/pid-2.1-2425/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=maryycarrera/pid-2.1-2425" />
</a>
