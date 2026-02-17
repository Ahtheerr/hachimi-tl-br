import os
import shutil
import sys
import re

def organizar_por_cab(pasta_alvo):
    if not os.path.exists(pasta_alvo):
        print(f"Erro: A pasta '{pasta_alvo}' não existe.")
        return

    # Regex para capturar o padrão CAB seguido de 32 caracteres hexadecimais
    # Exemplo: CAB-ca173a268eb895d638ab5629e47f62f4
    padrao_cab = re.compile(r"(CAB-[a-f0-9]{32})")

    arquivos = [f for f in os.listdir(pasta_alvo) if os.path.isfile(os.path.join(pasta_alvo, f))]
    contador = 0

    for nome_arquivo in arquivos:
        match = padrao_cab.search(nome_arquivo)
        
        if match:
            id_cab = match.group(1)
            # Define o caminho da nova subpasta
            nova_pasta = os.path.join(pasta_alvo, id_cab)

            # Cria a pasta se ela não existir
            if not os.path.exists(nova_pasta):
                os.makedirs(nova_pasta)

            # Move o arquivo
            origem = os.path.join(pasta_alvo, nome_arquivo)
            destino = os.path.join(nova_pasta, nome_arquivo)
            
            try:
                shutil.move(origem, destino)
                contador += 1
            except Exception as e:
                print(f"Erro ao mover {nome_arquivo}: {e}")

    print(f"Organização concluída! {contador} arquivos movidos para suas respectivas pastas CAB.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python organizar_cab.py <caminho_da_pasta>")
    else:
        organizar_por_cab(sys.argv[1])