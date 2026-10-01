#!/usr/bin/env bash
set -euo pipefail

ENGINE_ROOT="/Users/kennethdallmier/cathedral_engine"
CORPUS_DIR="/Users/kennethdallmier/corpus"
echo "[CATHE-DRIVE] Initiating Local AI & Ingestion Pipeline..."

# 1. Expand and validate corpus substrate
python3 "$ENGINE_ROOT/expand_corpus.py" --input "$CORPUS_DIR/" --validate

# 2. Execute base model pretraining
python3 "$ENGINE_ROOT/pretrain_base_model.py" \
    --config "$ENGINE_ROOT/configs/pretrain_config.json" \
    --output "$ENGINE_ROOT/base_model/"

# 3. Compile and align via LoRA/SFT
python3 "$ENGINE_ROOT/compile_and_train.py" \
    --base "$ENGINE_ROOT/base_model/" \
    --output "$ENGINE_ROOT/merged_model/"

# 4. Reconcile configuration vocabulary
python3 "$ENGINE_ROOT/update_config_vocab.py" \
    --model_dir "$ENGINE_ROOT/merged_model/"

# 5. Fix model cache integrity
python3 "$ENGINE_ROOT/fix_model_cache.py" \
    --model_dir "$ENGINE_ROOT/merged_model/"

# 6. Convert HuggingFace artifacts to GGUF
python3 "$ENGINE_ROOT/convert_hf_to_gguf.py" \
    --input "$ENGINE_ROOT/merged_model/" \
    --output "$ENGINE_ROOT/models/mlaos-cathedral-f16.gguf"

echo "[CATHE-DRIVE] Pipeline complete. Quantized artifact registered at /models/mlaos-cathedral-f16.gguf."
