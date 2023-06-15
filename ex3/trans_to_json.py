import os
from PIL import Image
import json
import re
def get_image_size(image_dir, file_name):
    """
    Get the size (width and height) of an image file in the specified directory.

    :param image_dir: str, the directory containing the image file
    :param file_name: str, the name of the image file
    :return: tuple, the size of the image as (width, height)
    """
    image_path = os.path.join(image_dir, file_name)
    with Image.open(image_path) as img:
        width, height = img.size

    return width, height



def txt_to_json(txt_content,image_dir):
    """
    Convert txt content to the desired JSON format.

    :param txt_content: str, text content to be converted
    :param img_height: int, image height
    :param img_width: int, image width
    :return: str, converted JSON string
    """
    lines = txt_content.split('\n')
    ocr_info = []

    linking_dict = {}

    for line in lines:
        if not line:
            continue
        id_counter = 0
        parts = line.split('	')
        #print(parts[0])
        img_width, img_height = get_image_size(image_dir, parts[0])
        # 使用正则表达式匹配提取所需的信息
        pattern = r'"transcription": "([^"]+)", "points": \[((?:\[\d+, \d+\],? ?)+)\], "key_cls": "([^"]+)"'

        for match in re.finditer(pattern, parts[1]):
            text = match.group(1)
            points_str = match.group(2)
            key_cls = match.group(3)

            # 提取坐标点
            points = [[int(x), int(y)] for x, y in re.findall(r'\[(\d+), (\d+)\]', points_str)]

            xmin = min(p[0] for p in points)
            ymin = min(p[1] for p in points)
            xmax = max(p[0] for p in points)
            ymax = max(p[1] for p in points)
            bbox = [xmin, ymin, xmax, ymax]
            print(f"text: {text}, key_cls: {key_cls}, points: {points}, bbox: {bbox}")

            if "head" in key_cls:
                label = "header"
            elif "question" in key_cls:
                label = "question"
            elif "answer" in key_cls:
                label = "answer"
            else:
                continue

            if label in ["question", "answer"]:
                cls_num = key_cls.split("_")[-1]
                if cls_num not in linking_dict:
                    linking_dict[cls_num] = {"question": [], "answer": []}
                linking_dict[cls_num][label].append(id_counter)

            ocr_info.append({
                "text": text,
                "label": label,
                "bbox": bbox,
                "id": id_counter,
                "words": []
            })

            id_counter += 1

        # Generate linking pairs
        for cls_num, link_info in linking_dict.items():
            question_ids = link_info["question"]
            answer_ids = link_info["answer"]

            for q_id in question_ids:
                for a_id in answer_ids:
                    q_cls_num = int(re.findall(r'\d+', ocr_info[q_id]["label"])[0])
                    a_cls_num = int(re.findall(r'\d+', ocr_info[a_id]["label"])[0])
                    if q_cls_num == a_cls_num:
                        ocr_info[q_id]["linking"].append([q_id, a_id])
                        ocr_info[a_id]["linking"].append([q_id, a_id])

    result = {
        "height": img_height,
        "width": img_width,
        "ocr_info": ocr_info
    }

    return json.dumps(result, ensure_ascii=False, indent=4)

# Read the txt content and pass it to the function



if __name__ == "__main__":
    # Example usage
    image_dir = 'D:\\DL_projects\\somedatas\\vehicle_invoice\\Vehicle_invoice_dataset\\processed_data\\'
    file_name = 'train/0.jpg'
    width, height = get_image_size(image_dir, file_name)
    print(f"Image size: width={width}, height={height}")

    train_input='D:\\DL_projects\\somedatas\\vehicle_invoice\\Vehicle_invoice_dataset\\processed_data\\train\\Label.txt'
    test_input = 'D:\\DL_projects\\somedatas\\vehicle_invoice\\test\\Label.txt'
    output='D:\DL_projects\somedatas\\vehicle_invoice\Vehicle_invoice_dataset\processed_data\\train\\normalize_train.json'
    with open(train_input, 'r', encoding='utf-8') as txt_file:
        txt_content = txt_file.read()

    json_string = txt_to_json(txt_content,image_dir)
    print(json_string)