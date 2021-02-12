import sys
import codecs

URL = 1

def load_channel_urls(fname):
    urls = []
    with codecs.open(fname, 'r', 'utf-8', 'ignore') as fp:
        for line in fp:
            line = line.split(',')
            url = line[URL]
            url = url[1:-1]
            urls.append(url)
    return urls


def write_urls(fname, urls):
    with open(fname, 'w') as fp:
        for url in urls:
            fp.write(url+'\n')

def main():
    urls = load_channel_urls(sys.argv[1])
    write_urls(sys.argv[2], urls)


if __name__ == '__main__':
    main()
