# RNLN 2026 — Laboratorio 2

Generación de programas en un lenguaje de dominio específico (DSL) para dibujar escenas geométricas en una grilla $6 \times 6$ a partir de instrucciones en lenguaje natural, evaluando estrategias de **zero-shot**, **prompting (few-shot)** y **fine-tuning con LoRA**.

## Estructura del proyecto

- [RNLN_2026_lab2.ipynb](RNLN_2026_lab2.ipynb): Notebook principal del laboratorio.
- `data/`: Particiones del dataset (`train.csv`, `dev.csv`, `test.csv`, `test_ood.csv`).
- `modelo_con_lora/`: Adaptadores LoRA entrenados sobre `Qwen/Qwen3.5-0.8B` (`r=16`, `lora_alpha=32`, `target_modules="all-linear"`).
- [pyproject.toml](pyproject.toml) y `uv.lock`: Gestión de dependencias multiplataforma con `uv` (usando *hard links* desde la caché global).
- [requirements.txt](requirements.txt): Dependencias base del laboratorio (referencia).
- [patch_transformers_macintel.py](patch_transformers_macintel.py) y [torch_compat_macintel.py](torch_compat_macintel.py): Parches de compatibilidad para macOS Intel (`torch==2.2.2` + `transformers==5.2.0`).

## Gestión de entornos virtuales con `uv` (Hard Links + Multi-OS)

El proyecto utiliza `uv` con `link-mode = "hardlink"` en [pyproject.toml](pyproject.toml). Los paquetes se descargan una sola vez en la caché global del sistema (`%LOCALAPPDATA%\uv\cache` en Windows / `~/.cache/uv` en macOS) y se enlazan mediante **hard links** en cada entorno virtual sin ocupar espacio adicional en el disco local.

Para evitar colisiones de binarios entre sistemas operativos dentro de Dropbox, se usan carpetas separadas por OS (preconfiguradas automáticamente en [.vscode/settings.json](.vscode/settings.json) mediante `UV_PROJECT_ENVIRONMENT`):

- **Windows (`.venv-win`)**:
  ```powershell
  # En terminales integradas de VS Code, UV_PROJECT_ENVIRONMENT y el proxy corporativo ya están configurados:
  uv sync
  ```
  - Si se ejecuta desde una terminal externa en red corporativa (Zscaler PAC):
    ```powershell
    $env:HTTPS_PROXY = "http://185.46.212.88:443"
    $env:UV_PROJECT_ENVIRONMENT = ".venv-win"
    uv sync --system-certs
    ```
  - Excluir `.venv-win` de la sincronización en la nube de Dropbox (para que Dropbox no suba los archivos enlazados):
    ```powershell
    Set-Content -Path .\.venv-win -Stream com.dropbox.ignored -Value 1
    ```

- **macOS (`.venv-mac`)**:
  ```bash
  UV_PROJECT_ENVIRONMENT=.venv-mac uv sync
  # Excluir de Dropbox en macOS:
  xattr -w com.dropbox.ignored 1 .venv-mac
  ```

## Notas de evaluación en el notebook

- **Aislamiento entre modelo base y LoRA (`test` y `test_ood`):**
  - Las celdas de evaluación de **Estrategia 4 (Few-Shot)** desactivan explícitamente los adaptadores (`with model.disable_adapter():`) cuando `model` es un `PeftModel`, asegurando que se evalúe únicamente el modelo base sin pesos LoRA.
  - Las celdas de evaluación de **LoRA** verifican que `model` sea una instancia `PeftModel` con los adaptadores de `./modelo_con_lora` cargados y activos (`enable_adapter_layers()`) antes de generar las predicciones.
