import yaml 

if __name__ == '__main__':
    with open('test.yaml', 'r') as f:
        doc = yaml.load(f)
    print doc