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
            if not any(substring in transcription for substring in ['进口证明',
                                      '证号'])and not transcription.startswith(('WAN','YX')):
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

input_file = "D:\DL_projects\somedatas\\vehicle_invoice\\test\\Labelraw2.txt"
output_file = "D:\DL_projects\somedatas\\vehicle_invoice\\test\\Labelraw3.txt"

process_annotations(input_file, output_file)
