# Materiales de Estudio / Academic Course Content

Esta carpeta está destinada a alojar los insumos fuente originales de los cursos (PDFs, diapositivas Beamer, notas manuscritas, capturas de pizarra).

## 🔒 Política de Control de Versiones (Zero-Bloat)
Por diseño arquitectónico, **todos los archivos binarios (PDFs, PNGs, JPGs) dentro de esta carpeta están excluidos de Git** mediante `.gitignore`.
Esto evita el engrosamiento del repositorio (`bloat`), prevé violaciones de límites de cuota de GitHub y permite manejar libros enteros de cientos de megabytes de forma desacoplada.

## Estructura Recomendada
```
content/
├── <materia_o_tema_slug>/
│   ├── lecture_01.pdf
│   ├── notas_manuscritas.pdf
│   └── diagramas.png
```

## Ejecución del Pipeline
El generador de cursos (`.agents/skills/content-to-course/run.py`) toma los archivos mediante el parámetro `--pdf`:

```bash
python .agents/skills/content-to-course/run.py \
  --course-id <id_del_curso> \
  --title "<Título del Curso>" \
  --pdf content/<materia_slug>/archivo1.pdf content/<materia_slug>/archivo2.pdf
```
También es posible pasar rutas directas a archivos alojados externamente en Google Drive u otra unidad sin copiarlos aquí.
