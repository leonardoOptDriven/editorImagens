import os

# Defina os caminhos das pastas
plot_folder = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/guilherme_fabrica_t4s_LABEL/v_fabrica_6/plots"
image_folder = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/guilherme_fabrica_t4s_LABEL/v_fabrica_6/images"
label_folder = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/guilherme_fabrica_t4s_LABEL/v_fabrica_6/labels"

# Obtenha os nomes dos arquivos na pasta plots, sem as extensões
plot_files = {os.path.splitext(file)[0] for file in os.listdir(plot_folder) if file.endswith(".png")}

# Verifique e delete arquivos na pasta images
for file in os.listdir(image_folder):
    file_name, file_extension = os.path.splitext(file)
    if file_name not in plot_files:
        os.remove(os.path.join(image_folder, file))
        print(f"Deletado: {os.path.join(image_folder, file)}")

# Verifique e delete arquivos na pasta labels
for file in os.listdir(label_folder):
    file_name, file_extension = os.path.splitext(file)
    if file_name not in plot_files:
        os.remove(os.path.join(label_folder, file))
        print(f"Deletado: {os.path.join(label_folder, file)}")