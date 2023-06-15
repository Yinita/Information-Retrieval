import json

def process_annotations(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        img_name, raw_annotations = line.strip().split('\t')
        annotations = json.loads(raw_annotations)

        processed_annotations = []
        for annotation in annotations:
            transcription = annotation['transcription']
            if len(transcription) > 2 and not any(substring in transcription for substring in ['付款凭证','手开无效','机动车'
                ,'商检','社会','查询码','／','完税凭证号码','身份证号码', '机打', '票', '草', '整', '章', '率',
                '+', '-', '*', '/', '机器编号', '！', '印', '!', 'LL', 'RL', '（', '限乘',
                'lll', 'LLL'])and not transcription.startswith(('00','L','111', '145002', '133002', '53990', '66190','13%')):
                processed_annotations.append({
                    'transcription': transcription,
                    'points': annotation['points']
                })

        data.append({
            'image': img_name,
            'annotations': processed_annotations
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(item['image'] + '\t')
            f.write(json.dumps(item['annotations'], ensure_ascii=False, separators=(',', ':')))
            f.write('\n')

input_file = "D:\DL_projects\somedatas\\vehicle_invoice\\train\\Labelraw.txt"
output_file = "D:\DL_projects\somedatas\\vehicle_invoice\\train\\Labelraw3.txt"

process_annotations(input_file, output_file)
