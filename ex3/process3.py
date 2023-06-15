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


            # 规则 1: 修改transcription
            if '￥' in transcription:
                transcription = transcription.replace('￥ ', '')
            elif '不' in transcription:
                transcription = '不含税价'
            elif '所' in transcription:
                transcription = '税务所'
            elif '发票' in transcription:
                transcription = '机动车销售统一发票'
            elif '国家税务总局南宁' in transcription:
                transcription = '国家税务总局南宁高新技术产业开发区税务局心圩税务分局'
            elif '器码' in transcription:
                transcription = '发动机号码'
            elif '机码' in transcription:
                transcription = '发动机号码'
            elif '称' in transcription and transcription != '购买方名称':
                transcription = '销货单位名称'

            # 规则 2: 修改key_cls
            if transcription in ['购买方名称', '车辆类型', '厂牌型号', '产地', '发动机号码', '销货单位名称', '纳税人识别号', '开户银行', '增值税', '不含税价', '主管税务', '机关及代码']:
                key_cls = 'question'
            elif transcription == '机动车销售统一发票':
                key_cls = 'head'
            else:
                key_cls = 'answer'

            processed_annotations.append({
                'transcription': transcription,
                'points': annotation['points'],
                'key_cls': key_cls
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

input_file = "D:\DL_projects\somedatas\\vehicle_invoice\\processed_data\\test\\Labelraw.txt"
output_file = "D:\DL_projects\somedatas\\vehicle_invoice\\processed_data\\test\\Labelraw3.txt"

process_annotations(input_file, output_file)
