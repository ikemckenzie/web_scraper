from bs4 import BeautifulSoup
import requests
import re
import argparse
import sys


def the_getter(url, regex, result_text):
    results = '\n'.join(set([str(url.get('href')).replace('mailto:', '')
                             for url in url.find_all('a') if re.search(regex, str(url))]))
    if not results:
        print('No {} found'.format(result_text))
    else:
        print '\n\n{}:\n'.format(result_text), results
    return results


def get_phones(url):
    phone_results = '\n'.join(set(['({}) {}-{}'.format(phone[0], phone[1], phone[2]) for phone in re.compile(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?').findall(str(url))]))
    if not phone_results:
        print('No phone numbers found')
    print '\n\nPhone Numbers:\n', phone_results
    return phone_results


def get_images(url):
    image_results = '\n'.join(set([image.get('src').replace('/s/', '')
                                   for image in url.find_all('img', src=True)]))
    if not image_results:
        print('No images found')
    print '\n\nImages:\n', image_results
    return image_results


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Enter url for the webscraper')
    return parser


def main(args):
    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    namespace = parser.parse_args(args)
    url = BeautifulSoup(requests.get(namespace.url).text, 'html.parser')
    if url:
        get_images(url)
        get_phones(url)
        the_getter(
            url, r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URLs')
        the_getter(
            url, r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', 'Emails')


if __name__ == '__main__':
    main(sys.argv[1:])
