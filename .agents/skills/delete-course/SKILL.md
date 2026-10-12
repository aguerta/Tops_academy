---
name: delete-course
description: Safely and quickly deletes courses from the Top's Academy platform (< 300 ms). Eliminates courses/<course_id>.json, competence_analysis_<course_id>.md, and intermediate working folders so they cannot be served or analyzed by the platform, while preserving historical QA audit reports with 'ELIMINADO' status and deletion timestamp, and strictly enforcing the inviolable immutability of content/.
triggers:
  - "delete course"
  - "eliminar curso"
  - "borrar curso"
  - "purge course"
  - "retirar curso"
  - "retirar curso de la plataforma"
  - "limpiar plataforma"
inputs:
  course_id:
    type: string
    description: Alphanumeric slug identifier for the course to delete
    required: false
  all:
    type: boolean
    description: Purge all active courses currently published in the platform
    default: false
  clean_orphans:
    type: boolean
    description: Clean orphan intermediate directories in courses/
    default: false
  dry_run:
    type: boolean
    description: Simulate deletion and report affected files without touching disk
    default: false
  archive:
    type: boolean
    description: Move course files to archive_rejected_courses/ instead of permanent deletion
    default: false
  clear_work:
    type: boolean
    description: Also clear intermediate working files in work/ if related
    default: false
outputs:
  deleted_files:
    type: array
    description: List of platform files permanently removed
  deleted_dirs:
    type: array
    description: List of course directories permanently removed
  stamped_reports:
    type: array
    description: List of QA audit reports preserved and stamped with deletion timestamp
  status:
    type: string
    description: Outcome status ('success' or 'dry_run')
---

# Delete-Course Skill (Plataforma Top's Academy)

Skill especializada y de alta velocidad para la baja y purga inmediata de cursos de la plataforma interactiva Top's Academy, garantizando el aislamiento absoluto de los materiales originales y la preservación histórica de las auditorías de calidad.

---

> [!CAUTION]
> ## 🚨 INVARIANTE INVIOLABLE: INMUTABILIDAD DE `content/`
> La carpeta `content/` (y cualquier variante como `contents/`) almacena los **materiales fuente originales** (PDFs Beamer, notas manuscritas OneNote, imágenes de pizarrón y datos primarios). 
> 
> **BAJO NINGUNA CIRCUNSTANCIA SE PUEDE TOCAR, MODIFICAR O ELIMINAR LA CARPETA `content/`**.
> El motor (`delete_course.py`) implementa la guarda `assert_path_safe()` que resuelve canónicamente las rutas y aborta de inmediato con una excepción `SecurityError` si cualquier archivo o argumento coincide o reside dentro de `content/` o `contents/`.

> [!IMPORTANT]
> ## 📊 POLÍTICA DE PRESERVACIÓN HISTÓRICA DE AUDITORÍAS (QA LEGACY)
> Los reportes de auditoría en `reports/qa_audits/` (`<id>_payload.json`, `<id>_qa_report.json`, `<id>_qa_report.md` y `SUITE_QA_AUDIT_REPORT.md`) **NO se eliminan**. 
> Se conservan permanentemente como registro analítico, pero el motor inyecta:
> 1. En el JSON individual: `"platform_status": "ELIMINADO"` y `"deleted_at": "<FECHA_HORA>"`.
> 2. En el Markdown individual: Banner de advertencia `[!WARNING]` y campo `**Fecha de Eliminación:** <FECHA_HORA>` (o `Nulo` si continúa vigente).
> 3. En la tabla consolidada `SUITE_QA_AUDIT_REPORT.md`: Columna **`Fecha Eliminación`** y estado actualizado a `Eliminado de la Plataforma`.

---

## Modos de Uso y Comandos CLI

El motor determinista puede ejecutarse desde la terminal o mediante llamadas de agentes con `run_command`:

### 1. Listar el Estado de Todos los Cursos
Inspecciona qué cursos están activos en la plataforma y cuáles están retirados con auditoría legacy:
```bash
python .agents/skills/delete-course/scripts/delete_course.py --list
```
*(O mediante el atajo `python scripts/delete_course.py --list`)*

### 2. Previsualizar la Eliminación (Dry-Run Seguro)
Permite verificar exactamente qué archivos se eliminarían y qué reportes se sellarían sin tocar el disco:
```bash
python .agents/skills/delete-course/scripts/delete_course.py --course-id <ID_DEL_CURSO> --dry-run
```

### 3. Eliminar un Curso Específico Rápido (< 300 ms)
Elimina todos los archivos del curso de `courses/`, deshabilitándolo inmediatamente en `run_platform.py` y sellando su auditoría:
```bash
python .agents/skills/delete-course/scripts/delete_course.py --course-id <ID_DEL_CURSO> --yes
```

### 4. Purgar Todos los Cursos Activos de la Plataforma
Retira todos los cursos publicados en `courses/*.json`:
```bash
python .agents/skills/delete-course/scripts/delete_course.py --all --yes
```

### 5. Limpiar Carpetas Intermedias Huérfanas en `courses/`
Elimina directorios residuales en `courses/` que no correspondan a cursos JSON activos (protegiendo siempre `courses/fixtures/`):
```bash
python .agents/skills/delete-course/scripts/delete_course.py --clean-orphans
```

### 6. Opción Alternativa de Archivado (`--archive`)
Si en lugar de purgar definitivamente se desea mover el curso a `archive_rejected_courses/`:
```bash
python .agents/skills/delete-course/scripts/delete_course.py --course-id <ID_DEL_CURSO> --archive --yes
```

---

## Flujo de Trabajo para el Agente Orquestador

Cuando el usuario solicite eliminar o retirar un curso de la plataforma:

1. **Paso 1: Identificación y Diagnóstico:**
   Ejecuta `python scripts/delete_course.py --list` para confirmar el identificador exacto del curso.
2. **Paso 2: Ejecución de Purga:**
   Ejecuta `python scripts/delete_course.py --course-id <id> --yes`.
3. **Paso 3: Verificación con la Plataforma:**
   Ejecuta `python run_platform.py --scan` y confirma que el curso ya no es descubierto por la plataforma.
4. **Paso 4: Verificación de Integridad de Fuentes:**
   Verifica que la carpeta `content/` permanezca 100% intacta.
5. **Paso 5: Reporte al Usuario:**
   Informa al usuario el tiempo de ejecución, los archivos eliminados y la confirmación de que su reporte de auditoría quedó archivado y sellado con la fecha de baja correspondiente.
