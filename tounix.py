from pathlib import Path
import sys

def convert_file_to_lf(file_path: Path):
    """Converte um arquivo para LF (\\n), sobrescrevendo o original."""
    try:
        # Lê o conteúdo como texto (UTF-8)
        content = file_path.read_text(encoding='utf-8', errors='replace')
        
        # Remove \\r e garante que termina com \\n
        lines = content.splitlines()
        new_content = '\n'.join(lines) + '\n' if content else ''
        
        # Escreve de volta com newline='\n' (LF)
        file_path.write_text(new_content, encoding='utf-8', newline='\n')
        
        print(f"Convertido: {file_path}")
    except Exception as e:
        print(f"Erro ao converter {file_path}: {e}", file=sys.stderr)

def main():
    root = Path("localized_data")
    
    if not root.is_dir():
        print("Erro: Pasta 'localized_data' não encontrada na raiz.")
        return
    
    print("Iniciando conversão para Unix LF (\\n)...")
    print("Isso vai sobrescrever os arquivos originais!\n")
    
    count = 0
    for file_path in root.rglob("*"):
        if file_path.is_file() and file_path.suffix in {'.json', '.txt', '.yaml', '.yml', '.js', '.css', '.html', '.md'}:
            # Pode adicionar mais extensões se quiser converter outros tipos de texto
            convert_file_to_lf(file_path)
            count += 1
    
    if count == 0:
        print("Nenhum arquivo de texto encontrado para converter.")
    else:
        print(f"\nConcluído! {count} arquivos convertidos para LF.")

if __name__ == "__main__":
    main()