# RNLN 2026 — Laboratorio 2

Generación de programas en un lenguaje de dominio específico (DSL) para dibujar escenas geométricas en una grilla $6 \times 6$ a partir de instrucciones en lenguaje natural, evaluando estrategias de **zero-shot**, **prompting (few-shot)** y **fine-tuning con LoRA**.

## Estructura del proyecto

- [RNLN_2026_lab2.ipynb](RNLN_2026_lab2.ipynb): Notebook principal del laboratorio.
- `data/`: Particiones del dataset (`train.csv`, `dev.csv`, `test.csv`, `test_ood.csv`).
- `modelo_con_lora/`: Adaptadores LoRA entrenados sobre `Qwen/Qwen3.5-0.8B` (`r=16`, `lora_alpha=32`, `target_modules="all-linear"`).
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

## Notas de evaluación en el notebook

- **Aislamiento entre modelo base y LoRA (`test` y `test_ood`):**
  - Las celdas de evaluación de **Estrategia 4 (Few-Shot)** desactivan explícitamente los adaptadores (`with model.disable_adapter():`) cuando `model` es un `PeftModel`, asegurando que se evalúe únicamente el modelo base sin pesos LoRA.
  - Las celdas de evaluación de **LoRA** verifican que `model` sea una instancia `PeftModel` con los adaptadores de `./modelo_con_lora` cargados y activos (`enable_adapter_layers()`) antes de generar las predicciones.
