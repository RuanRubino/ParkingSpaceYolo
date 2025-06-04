import os
from glob import glob
import shutil

def sends(jpg_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    try:
            current_processing_file = jpg_file # Atualiza para cada arquivo
            output_path = os.path.join(output_dir, os.path.basename(jpg_file))
            shutil.copy(jpg_file, output_path)
    except Exception as e:
        if current_processing_file:
            print(f"Erro ao processar {current_processing_file}: {str(e)}")
        else:
            print(f"Erro antes de iniciar o processamento dos arquivos: {str(e)}")
# Processar todos os XMLs


