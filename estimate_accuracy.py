import sys

def get_label(y):
    label = ''
    for uni_int in y.split('-'):
        label += chr(int(uni_int))
    return label

def main():
    file_name = sys.argv[1]
    correct = 0
    total = 0
    with open(file_name, 'r') as inp:
        for line in inp:
            total += 1
            y, pred = line.strip().split(',')
            y = get_label(y.split('.')[0].strip())
            if y == pred.strip():
                correct += 1
    print('correct', correct)
    print('total', total)
    print('ratio', correct / total)

if __name__ == '__main__':
    main()
