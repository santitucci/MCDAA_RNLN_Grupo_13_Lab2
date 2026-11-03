# RNLN 2026 — Laboratorio 2

Generación de programas en un lenguaje de dominio específico (DSL) para dibujar escenas geométricas en una grilla $6 \times 6$ a partir de instrucciones en lenguaje natural, evaluando estrategias de **zero-shot**, **prompting (few-shot)** y **fine-tuning con LoRA**.

## Estructura del proyecto

- [RNLN_2026_lab2.ipynb](RNLN_2026_lab2.ipynb): Notebook principal del laboratorio.
- `data/`: Particiones del dataset (`train.csv`, `dev.csv`, `test.csv`, `test_ood.csv`).
- [requirements.txt](requirements.txt): Dependencias base del laboratorio.
- [patch_transformers_macintel.py](patch_transformers_macintel.py) y [torch_compat_macintel.py](torch_compat_macintel.py): Parches de compatibilidad para macOS Intel (`torch==2.2.2` + `transformers==5.2.0`).

## Entornos virtuales (Dropbox multi-OS)

Dado que el proyecto se sincroniza mediante Dropbox entre **macOS** y **Windows**, se mantienen entornos virtuales separados por sistema operativo para evitar conflictos de binarios:

- **Windows**: `.venv-win/` (Python 3.12, `torch>=2.4` CPU, `transformers==5.2.0`, `peft`, `accelerate`).
  - Activación en PowerShell: `.venv-win\Scripts\Activate.ps1`
  - Ejecución / instalación con `uv` en red con proxy/certificados del sistema: añadir `--system-certs`.
  - Carga del modelo sin red (caché local): `HF_HUB_OFFLINE=1` y `huggingface_hub.constants.HF_HUB_OFFLINE = True` se definen antes de instanciar `AutoTokenizer` para evitar que `transformers` consulte `model_info()` en línea.
- **macOS**: `.venv/` (Python 3.12 para macOS).
  - Activación en bash/zsh: `source .venv/bin/activate`
