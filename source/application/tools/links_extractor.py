from re import compile


class LinksExtractor:

    """Статический класс с описанием методов для проверкм валидности введенных ссылок."""

    # Доступные шаблоны
    available_url_patterns = {
        'citilink': [
            compile(r'https://www.citilink.ru/product/(.*)/'),
            compile(r'https://www.citilink.ru/catalog/(.*)/')
        ],
        'e-katalog': [
            compile(r'https://www.e-katalog.ru/(.*).htm'),
            compile(r'https://www.e-katalog.ru/list/(.*)/'),
            compile(r'https://www.e-katalog.ru/ek-list(.*)')
        ],
        'onlinetrade': [
            compile(r'https://www.onlinetrade.ru/catalogue/(.*).html'),
            compile(r'https://www.onlinetrade.ru/catalogue/(.*)/')
        ]
    }

    @staticmethod
    def get_relevant(urls):
        """Метод, проверяющий валидность ссылок.

        Args:
            urls: список ссылок для проверки.

        Returns:
            result - словарь валидных ссылок, сгруппированных по магазинам и типу.
        """
        result = {
            'eldorado': {
                'product': [],
                'products': []
            },
            'citilink': {
                'product': [],
                'products': []
            },
            'e-katalog': {
                'product': [],
                'products': []
            },
            'onlinetrade': {
                'product': [],
                'products': []
            }
        }
        for url in urls:
            for key in LinksExtractor.available_url_patterns:
                if key not in url:
                    continue
                for pattern in LinksExtractor.available_url_patterns[key]:
                    found_url = pattern.match(url)
                    if found_url:
                        if LinksExtractor.available_url_patterns[key].index(pattern) == 0:
                            result[key]['product'].append(url)
                        else:
                            result[key]['products'].append(url)
                    else:
                        continue
        return result

    @staticmethod
    def get_links(urls):
        """Метод, проверяющий валидность ссылок, возвращающий их в виде списка.

        Args:
            urls: список ссылок для проверки.

        Returns:
            links - список валидных ссылок.
        """
        result = LinksExtractor.get_relevant(urls)
        links = []
        for key in result:
            result[key]['product'].extend(result[key]['products'])
            links.extend(result[key]['product'])
        return links
