import json
import csv
import os
import sys

def tsv_to_json_recursive(input_tsv, output_root):
    files_data = {}

    try:
        with open(input_tsv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                rel_path = row.pop('relative_path', None)
                if not rel_path: continue

                clean_row = {}
                for key, value in row.items():
                    if value:
                        # Reverte o literal \n para quebra de linha real para o json.dump
                        clean_row[key] = value.replace('\\n', '\n')
                
                if rel_path not in files_data:
                    files_data[rel_path] = []
                files_data[rel_path].append(clean_row)

        for rel_path, blocks in files_data.items():
            # Define o caminho final e cria as pastas necessárias
            final_path = os.path.join(output_root, rel_path)
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            
            with open(final_path, 'w', encoding='utf-8') as jf:
                json.dump({"text_block_list": blocks}, jf, indent=4, ensure_ascii=False)
        
        print(f"Sucesso! Estrutura de arquivos recriada em '{output_root}'.")

    except Exception as e:
        print(f"Erro no processamento: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python importar.py arquivo.tsv pasta_destino")
    else:
        tsv_to_json_recursive(sys.argv[1], sys.argv[2])