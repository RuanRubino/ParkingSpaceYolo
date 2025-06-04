import os
import xml.etree.ElementTree as ET
from glob import glob
import shutil

def xml_to_yolo(xml_path, output_dir, img_width, img_height):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Criar nome do arquivo de saída
        base_name = os.path.splitext(os.path.basename(xml_path))[0]
        output_path = os.path.join(output_dir, base_name + '.txt')
        
        with open(output_path, 'w') as f:
            for space in root.findall('space'):
                # Determinar a classe baseado no status de ocupação
                try:
                    is_occupied = int(space.get('occupied'))
                    class_id = 1 if is_occupied else 0  # 0=vaga livre, 1=vaga ocupada
                except (ValueError, TypeError):
                    print(f"Status de ocupação inválido em {xml_path}")
                    continue
                
                # Obter pontos do contorno
                contour = space.find('contour')
                if contour is None:
                    continue
                
                points = []
                for point in contour.findall('point'):
                    try:
                        x = float(point.get('x')) / img_width  # Normaliza x
                        y = float(point.get('y')) / img_height  # Normaliza y
                        points.append((x, y))
                    except (ValueError, TypeError):
                        continue
                
                # Verificar se temos exatamente 4 pontos
                if len(points) != 4:
                    print(f"Contorno não tem 4 pontos em {xml_path}")
                    continue
                
                # Escrever no formato YOLO (classe seguida dos 8 valores normalizados)
                line = f"{class_id} " + " ".join([f"{p[0]:.6f} {p[1]:.6f}" for p in points]) + "\n"
                f.write(line)
        
        return output_path
        
    except Exception as e:
        print(f"Erro ao processar {xml_path}: {str(e)}")
        return None

def process_all_xmls(xml_files, img_width, img_height):
    # Criar diretórios se não existirem
    os.makedirs('../yolu/yolu_dataset/labels/train/', exist_ok=True)
    os.makedirs('../yolu/yolu_dataset/images/train/', exist_ok=True)
    
    for xml_file in xml_files:
        # Converter XML para YOLO
        label_path = xml_to_yolo(
            xml_file,
            '../yolu/yolu_dataset/labels/train/',
            img_width,
            img_height
        )
        
        if label_path:
            # Copiar imagem correspondente
            img_file = os.path.splitext(xml_file)[0] + '.jpg'
            if os.path.exists(img_file):
                dest_img = os.path.join(
                    '../yolu/yolu_dataset/images/train/',
                    os.path.basename(img_file)
                )
                shutil.copy2(img_file, dest_img)
                print(f"Processado: {xml_file} -> {label_path}, imagem copiada")
            else:
                print(f"Imagem correspondente não encontrada para {xml_file}")
        else:
            print(f"Falha ao processar {xml_file}")

# Configurações
IMAGE_WIDTH = 1280   
IMAGE_HEIGHT = 720  

# Processar todos os XMLs
xml_files = glob('../../PKLot/PKLot/PKLot/PUCPR/**/**/*.xml', recursive=True)
process_all_xmls(xml_files, IMAGE_WIDTH, IMAGE_HEIGHT)

# Criar arquivo data.yaml
yaml_content = """train: ../yolu/yolu_dataset/images/train/
val: ../yolu/yolu_dataset/images/val/

# Número de classes
nc: 2

# Nomes das classes
names: ['free_parking', 'occupied_parking']
"""

with open('../yolu/yolu_dataset/data.yaml', 'w') as f:
    f.write(yaml_content)

print("Conversão concluída e data.yaml criado")