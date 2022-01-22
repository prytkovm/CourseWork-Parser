from re import compile


class Extractor:

    available_url_patterns = {
        'eldorado': [
            compile(r'https://www.eldorado.ru/c/(.*)/'),
            compile(r'https://www.eldorado.ru/cat/detail/(.*)/')
        ],
        'citilink': [
            compile(r'https://www.citilink.ru/catalog/(.*)/'),
            compile(r'https://www.citilink.ru/product/(.*)/')
        ],
        'e-katalog': [
            compile(r'https://www.e-katalog.ru/list/(.*)/'),
            compile(r'https://www.e-katalog.ru/(.*).htm')
        ],
        'onlinetrade': [
            compile(r'https://www.onlinetrade.ru/catalogue/(.*)/')
        ]
    }

    @staticmethod
    def get_relevant(urls):
        result = {
            'eldorado': [],
            'citilink': [],
            'e-katalog': [],
            'onlinetrade': []
        }
        for url in urls:
            for key in Extractor.available_url_patterns:
                if key not in url:
                    continue
                for pattern in Extractor.available_url_patterns[key]:
                    found_url = pattern.match(url)
                    if found_url:
                        result[key].append(url)
                    else:
                        continue
        return result

    @staticmethod
    def get_links(urls):
        result = Extractor.get_relevant(urls)
        links = []
        for key in result:
            links.extend(result[key])
        return links
