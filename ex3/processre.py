import json


def process_question_pairing(ocr_infos):
    question_counter = 1
    questions = []
    answers = []

    # 寻找主管税务问题及其相关答案
    main_tax_question = None
    main_tax_question_index = None
    main_tax_answer_indices = []

    for index, ocr_info in enumerate(ocr_infos):
        if ocr_info["key_cls"] == "question" and "主管税务" in ocr_info["transcription"]:
            main_tax_question = ocr_info
            main_tax_question_index = index
            break

    if main_tax_question is not None:
        for index, ocr_info in enumerate(ocr_infos):
            if ocr_info["key_cls"] == "answer" and (
                "国家税务总局" in ocr_info["transcription"] or "税务所" in ocr_info["transcription"]
            ):
                main_tax_answer_indices.append(index)
                ocr_info["key_cls"] = f"answer_{question_counter}"
                ocr_infos[index] = ocr_info

        main_tax_question["key_cls"] = f"question_{question_counter}"
        ocr_infos[main_tax_question_index] = main_tax_question

        question_counter += 1

    for index, ocr_info in enumerate(ocr_infos):
        if ocr_info["key_cls"] == "question" and index != main_tax_question_index:
            questions.append((index, ocr_info))
        elif ocr_info["key_cls"] == "answer" and index not in main_tax_answer_indices:
            answers.append((index, ocr_info))

    for question_index, question in questions:
        question["key_cls"] = f"question_{question_counter}"
        ocr_infos[question_index] = question  # 将更新的问题信息写回 ocr_infos

        closest_answer_index = None
        closest_answer = None
        closest_distance = float("inf")

        threshold = 0

        for answer_index, answer in answers:
            if is_pair(question, answer):
                distance = get_distance(question["points"], answer["points"])
                if distance < closest_distance and distance > threshold:
                    closest_distance = distance
                    closest_answer = answer
                    closest_answer_index = answer_index

        if closest_answer:
            closest_answer["key_cls"] = f"answer_{question_counter}"
            ocr_infos[closest_answer_index] = closest_answer  # 将更新的答案信息写回 ocr_infos
            answers.remove((closest_answer_index, closest_answer))
        question_counter += 1

    return ocr_infos


def is_pair(question, answer):
    question_bbox = question["points"]
    answer_bbox = answer["points"]

    question_right = question_bbox[1][0]
    question_bottom = question_bbox[3][1]

    answer_left = answer_bbox[0][0]
    answer_top = answer_bbox[0][1]


    return True

def get_distance(question_points, answer_points):
    question_right = question_points[1][0]
    question_bottom = question_points[2][1]

    answer_left = answer_points[0][0]
    answer_top = answer_points[0][1]

    distance = ((answer_left - question_right) ** 2 + (answer_top - question_bottom) ** 2) ** 0.5
    return distance

'''output_file = 'D:\DL_projects\somedatas\\vehicle_invoice\processed_data\\train\\Label2.txt'



# 解析输入数据并继续后续处理
data_list = parse_input_data(input_data)

with open(output_file, 'w', encoding='utf-8') as f:
    for data in data_list:
        ocr_infos = data['ocr_infos']
        paired_questions = process_question_pairing(ocr_infos)

        for pair in paired_questions:
            f.write(f"{pair['question']}: {pair['answer']}\n")

        f.write('\n')'''
def parse_input_txt(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    for line in lines:
        file_path, ocr_infos_str = line.strip().split("\t")
        ocr_infos = json.loads(ocr_infos_str)
        ocr_infos = process_question_pairing(ocr_infos)
        data.append({"file_path": file_path, "ocr_infos": ocr_infos})

    return data
def write_output_txt(output_file, data):
    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            file_path = item["file_path"]
            ocr_infos = item["ocr_infos"]
            ocr_infos_str = json.dumps(ocr_infos, ensure_ascii=False)
            #print(ocr_infos_str)
            f.write(f"{file_path}\t{ocr_infos_str}\n")

input_file_path = "D:\DL_projects\somedatas\\vehicle_invoice\processed_data\\test\\Labelraw3.txt"
output_file_path = 'D:\DL_projects\somedatas\\vehicle_invoice\processed_data\\test\\Label.txt'

data_list = parse_input_txt(input_file_path)

write_output_txt(output_file_path, data_list)
