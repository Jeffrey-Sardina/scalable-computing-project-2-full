import sys

def main():
    file_name = sys.argv[1]
    correct = 0
    total = 0
    with open(file_name, 'r') as inp:
        for line in inp:
            total += 1
            y, pred = line.strip().split(',')
            if y.split('.')[0].strip() == y.strip():
                correct += 1
    print('correct', correct)
    print('total', total)
    print('ratio', correct / total)

if __name__ == '__main_':
    main()
