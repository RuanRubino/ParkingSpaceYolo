import os 
from glob import glob
import shutil

def split_validation(labels_dir, image_dir, output_dir, val_ratio=0.8):
    # Cria os diretórios de saída se não existirem
    os.makedirs(os.path.join(output_dir, './yolu_dataset/images/val/'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, './yolu_dataset/labels/val/'), exist_ok=True)

    # Obtém todos os arquivos de imagem no diretório
    image_files = glob(os.path.join(image_dir, '*.jpg'))
    labels_files = glob(os.path.join(labels_dir, '*.txt'))

    # Calcula o número de imagens para validação
    num_val = int(len(image_files) * val_ratio)

    # Embaralha as imagens e divide em treino e validação
    
    img_val_files = image_files[num_val:]
    labels_val_files = labels_files[num_val:]

    # Move as imagens para os diretórios correspondentes
    for file in img_val_files:
        shutil.move(file, os.path.join(output_dir, 'val', os.path.basename(file)))
    
    for file in labels_val_files:
        shutil.move(file, os.path.join(output_dir, 'val', os.path.basename(file)))

if __name__ == "__main__":
    # Configurações
    labels_dir = '../yolu/yolu_dataset/labels/train/'
    image_dir = '../yolu/yolu_dataset/images/train/'
    output_dir = '../yolu/yolu_dataset/'

    # Chama a função para dividir os dados
    split_validation(labels_dir, image_dir, output_dir, val_ratio=0.8)

    print("Divisão de validação concluída.")