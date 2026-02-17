import json
import csv
import os
import sys

def json_to_tsv_recursive(root_folder):
    if not os.path.isdir(root_folder):
        print(f"Erro: Pasta '{root_folder}' não encontrada.")
        return

    data_to_write = []
    dynamic_columns = set()

    # os.walk percorre a árvore de diretórios inteira
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith('.json'):
                full_path = os.path.join(root, filename)
                # Salva o caminho relativo (ex: subpasta/arquivo.json)
                rel_path = os.path.relpath(full_path, root_folder)
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        blocks = content.get("text_block_list", [])
                        
                        for block in blocks:
                            row = {"relative_path": rel_path}
                            for key, value in block.items():
                                if isinstance(value, str):
                                    # Mantém o TSV limpo, convertendo quebras reais em literal \n
                                    value = value.replace('\n', '\\n')
                                row[key] = value
                                dynamic_columns.add(key)
                            data_to_write.append(row)
                except Exception as e:
                    print(f"Erro ao ler {rel_path}: {e}")

    columns = ["relative_path"] + sorted(list(dynamic_columns))
    
    output_file = "resultado_recursivo.tsv"
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(data_to_write)
    
    print(f"Sucesso! {len(data_to_write)} linhas exportadas para '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python exportar.py pasta_raiz")
    else:
        json_to_tsv_recursive(sys.argv[1])