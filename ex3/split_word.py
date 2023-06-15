import json
import regex


def get_word_list(s1):
    regEx = regex.compile('\W]+')
    res = regex.compile(r"([\u4e00-\u9fa5\pZ\（\）\：\。\，\？\《\》\“\”])")

    p1 = regEx.split(s1)
    str1_list = []
    for str in p1:
        if res.split(str) == None:
            str1_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str1_list.append(ch)
    list_word1 = [w for w in str1_list if len(w) > 0]
    return list_word1


def process_label_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            file_path, ocr_data = line.strip().split("\t")
            ocr_infos = json.loads(ocr_data)

            new_ocr_infos = []
            for ocr_info in ocr_infos:
                if ocr_info["key_cls"] in ["question", "answer"]:
                    transcription = ocr_info["transcription"]
                    words = get_word_list(transcription)
                    points = ocr_info["points"]

                    x1, y1 = points[0]
                    x2, y2 = points[1]
                    width = x2 - x1
                    word_width = width / len(words)

                    for i, word in enumerate(words):
                        word_x1 = x1 + i * word_width
                        word_x2 = word_x1 + word_width
                        new_points = [[word_x1, y1], [word_x2, y1], [word_x2, y2], [word_x1, y2]]
                        new_ocr_info = {
                            "transcription": word,
                            "points": new_points,
                            "key_cls": ocr_info["key_cls"]
                        }
                        new_ocr_infos.append(new_ocr_info)
                else:
                    new_ocr_infos.append(ocr_info)

            new_line = file_path + "\t" + json.dumps(new_ocr_infos, ensure_ascii=False)
            f.write(new_line + "\n")



if __name__ == "__main__":
    input='D:\\DL_projects\\somedatas\\vehicle_invoice\\test\\Labelraw4.txt'
    output='D:\\DL_projects\\somedatas\\vehicle_invoice\\test\\Label.txt'
    process_label_file(input, output)
