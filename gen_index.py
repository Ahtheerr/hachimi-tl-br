import pygit2
from pathlib import Path
import json
from blake3 import blake3

def ls_tree(tree: pygit2.Tree, parent=Path(""), skip_trees=False):
    for e in tree:
        path = parent / e.name
        if isinstance(e, pygit2.Tree):
            if not skip_trees:
                yield path
            yield from ls_tree(e, path, skip_trees)
        else:
            yield path

def normalize_to_lf_bytes(file_path: Path) -> bytes:
    """Lê o arquivo, converte para LF (\\n) e retorna bytes normalizados."""
    try:
        # Lê como texto, ignorando erros de encoding pra não crashar
        text = file_path.read_text(encoding='utf-8', errors='replace')
        # Divide em linhas (remove qualquer \\r) e junta com \\n
        lines = text.splitlines()
        normalized_text = '\n'.join(lines) + '\n'  # adiciona final \\n como a maioria dos JSONs tem
        return normalized_text.encode('utf-8')
    except Exception as e:
        print(f"[Aviso] Falha ao normalizar {file_path}: {e}")
        # Fallback: lê bytes crus se der ruim (mas hash pode variar)
        return file_path.read_bytes()

def main():
    with open("index_base.json", encoding='utf-8') as f:
        index = json.load(f)
    index["files"] = []

    repo = pygit2.Repository('.')
    tree = repo.revparse_single('HEAD').tree

    ld_tree = None
    for e in tree:
        if e.name == "localized_data" and isinstance(e, pygit2.Tree):
            ld_tree = e
            break

    if not ld_tree:
        print("[Error] localized_data tree not found")
        return

    hasher = blake3(max_threads=blake3.AUTO)
    for path in ls_tree(ld_tree, skip_trees=True):
        if path.name == ".gitignore":
            continue

        print(path)
        fs_path = Path("localized_data") / path

        # Usa conteúdo normalizado para LF
        normalized_content = normalize_to_lf_bytes(fs_path)
        hasher.update(normalized_content)
        file_hash = hasher.digest()
        hasher.reset()

        index["files"].append({
            'path': path.as_posix(),
            'hash': file_hash.hex(),
            'size': fs_path.stat().st_size   # tamanho original (não normalizado)
        })

    # Salva o index.json sempre com LF
    with open("index.json", "w", encoding="utf-8", newline='\n') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print("\nindex.json gerado com hashes normalizados para LF.")

if __name__ == "__main__":
    main()