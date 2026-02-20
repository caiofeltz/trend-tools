#!/usr/bin/env python3
"""
Verificador de Instalação - Streamlit Dashboard
"""

import sys
import subprocess
import os

def check_module(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

print("╔════════════════════════════════════════════════════════════╗")
print("║  🔍 VERIFICADOR DE INSTALAÇÃO - STREAMLIT DASHBOARD      ║")
print("╚════════════════════════════════════════════════════════════╝\n")

modules_to_check = [
    ('streamlit', 'Streamlit'),
    ('plotly', 'Plotly'),
    ('pandas', 'Pandas'),
    ('pytrends', 'PyTrends'),
]

all_ok = True

for module, name in modules_to_check:
    if check_module(module):
        print(f"✅ {name} - Instalado")
    else:
        print(f"❌ {name} - NÃO Instalado")
        all_ok = False

print("\n" + "="*60 + "\n")

if all_ok:
    print("✅ TODAS AS DEPENDÊNCIAS ESTÃO INSTALADAS!\n")
    print("Para iniciar o dashboard, execute:\n")
    print("  ./run_dashboard.sh")
    print("\nOU\n")
    print("  streamlit run streamlit_dashboard.py")
    print("\n" + "="*60 + "\n")
    sys.exit(0)
else:
    print("❌ FALTAM DEPENDÊNCIAS\n")
    print("Para instalar, execute:\n")
    print("  pip install -r requirements.txt")
    print("\n" + "="*60 + "\n")
    sys.exit(1)
