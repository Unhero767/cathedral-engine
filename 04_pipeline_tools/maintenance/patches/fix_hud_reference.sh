#!/usr/bin/env zsh
echo "[Mlaos-Prime]: Fixing terminal prompt formatting and ensuring clean zsh execution..."
sed -i '' 's/%F{cyan}//g' ~/.zshrc 2>/dev/null || true
echo "[Mlaos-Prime]: Ready for next architectural directives."
