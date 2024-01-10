import cv2
import os
import glob
import numpy as np

def resize_image_proportionally(image_path, output_path, target_width=600, target_height=800):
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Erreur : Impossible de charger l'image '{image_path}'.")
        return False

    # Calculer le ratio de redimensionnement
    h, w = image.shape[:2]
    scale = min(target_width / w, target_height / h)

    # Redimensionner l'image
    new_size = (int(w * scale), int(h * scale))
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

    # Créer une nouvelle image avec l'arrière-plan transparent
    new_image = np.zeros((target_height, target_width, 4), dtype=np.uint8)

    # Calculer la position centrée
    x_offset = (target_width - new_size[0]) // 2
    y_offset = (target_height - new_size[1]) // 2

    # Placer l'image redimensionnée sur le nouvel arrière-plan
    new_image[y_offset:y_offset + new_size[1], x_offset:x_offset + new_size[0]] = resized_image

    # Sauvegarder l'image redimensionnée
    if not cv2.imwrite(output_path, new_image):
        print(f"Erreur : Impossible de sauvegarder l'image '{output_path}'.")
        return False

    print(f"Image '{image_path}' redimensionnée et sauvegardée.")
    return True

def resize_images_in_folder(folder_path, target_width=600, target_height=800):
    png_files = glob.glob(os.path.join(folder_path, "*.png"))
    for file in png_files:
        if not resize_image_proportionally(file, file, target_width, target_height):
            print(f"Erreur lors du traitement de l'image '{file}'.")

if __name__ == "__main__":
    folder_path = input("Entrez le chemin du dossier contenant les images PNG : ")
    resize_images_in_folder(folder_path)
