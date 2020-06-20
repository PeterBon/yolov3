import json

image_size = 2048
ids_train = open("images/ids_train.txt").read().splitlines()
ids_valid = open("images/ids_valid.txt").read().splitlines()
annotations = json.loads(open("annotations.json").read())
classes = annotations['types']

def write_labels(annos, id):
    img = annos['imgs'][id]
    objs = img['objects']
    with open('labels/' + id + '.txt', 'w') as f_label:
        for obj in objs:
            cls = obj['category']
            cls_id = classes.index(cls)
            bbox = obj['bbox']
            xmin = float(bbox['xmin'])
            ymin = float(bbox['ymin'])
            xmax = float(bbox['xmax'])
            ymax = float(bbox['ymax'])
            # 中心点和宽高要求在（0，1）之间
            x_center = (xmin + xmax) / 2 / image_size
            y_center = (ymin + ymax) / 2 / image_size
            width = (xmax - xmin) / image_size
            high = (ymax - ymin) / image_size
            f_label.write(
                str(cls_id) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(high) + '\n')

with open('classes.names','w') as f_classesnames:
    for cls in classes:
        f_classesnames.write(cls+'\n')

f_train = open('train.txt','w')
f_valid = open('valid.txt','w')
for id in ids_train:
    f_train.write('data/custom/images/' + id + '.jpg\n')
    write_labels(annotations, id)
for id in ids_valid:
    f_valid.write('data/custom/images/' + id + '.jpg\n')
    write_labels(annotations, id)
f_train.close()
f_valid.close()
