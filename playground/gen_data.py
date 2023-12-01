import os
import random
import warnings
from datetime import datetime, timedelta
from time import time

from faker import Faker
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

load_dotenv('.env')

ES_HOST = os.getenv('ES_HOST')
ES_USER = os.getenv('ES_USER')
ES_PASS = os.getenv('ES_PASS')
ES_CA_CERT_PATH = os.getenv('ES_CA_CERT_PATH')
ES_VERIFY_CERTS = False

ES_CREDENTIALS = {
    "hosts": ES_HOST,
    "ca_certs": ES_CA_CERT_PATH,
    "basic_auth": (ES_USER, ES_PASS),
    "verify_certs": ES_VERIFY_CERTS
}

warnings.filterwarnings("ignore")  # , category=Warning, module="elasticsearch")

es = Elasticsearch(ES_HOST, basic_auth=(ES_USER, ES_PASS), verify_certs=False)  # type: ignore
fake = Faker()


def generate_random_data(index_name, num_docs=-1, max_seconds=60 * 60):
    """ Max time in seconds to generate data, default 1 hour
    If not set - will generate data until num_docs is reached
    If set - will generate as many docs as possible in max_seconds
    If both are not set - will generate as many docs as possible in 1 hour"""

    time_start = time()
    reached_time_limit = False
    genereted_docs = 0
    reached_max_docs_limit = False
    print(f"Starting to renerate {num_docs if num_docs != -1 else 'as many as possible'} docs " +
          f"in {max_seconds} seconds into index {index_name}...")

    while not reached_time_limit and not reached_max_docs_limit:
        reached_time_limit = time() - time_start >= max_seconds if max_seconds > 0 else False
        reached_max_docs_limit = genereted_docs >= num_docs if num_docs > 0 else False

        title = fake.sentence(nb_words=random.randint(10, 20))
        url = fake.url()
        text_length = random.randint(200, 1000) if random.random() < 0.9 else random.randint(1000, 10000)
        text = fake.text(max_nb_chars=text_length)
        domain = url.split("//")[-1].split("/")[0]
        date = fake.date_time_this_decade()
        author = fake.name()
        indexed_at = datetime.now() - timedelta(days=random.randint(1, 30))

        print(f"Generated {genereted_docs} docs in {time() - time_start:.0f}s...", end='\r')

        genereted_docs += 1
        yield {
            '_op_type': 'index',
            '_index': index_name,
            '_source': {
                'title': title,
                'url': url,
                'text': text,
                'domain': domain,
                'date': date,
                'author': author,
                'indexed_at': indexed_at
            }
        }
    print()


def create_index(index_name):
    es.indices.create(index=index_name, ignore=400)


def gen_data(index_name, docs_number=20000, max_seconds=-1):
    create_index(index_name)

    time_start = time()
    actions = generate_random_data(index_name, docs_number, max_seconds)
    success, failed = helpers.bulk(es, actions)
    print(f"Indexed {success} documents in {time() - time_start:.0f} seconds.")
    if failed:
        print(f"Failed to index {failed} documents")


def main(index_name='split-texts-000001', docs_number=20000, max_seconds=60 * 60):
    create_index(index_name)
    gen_data(index_name, docs_number, max_seconds=max_seconds)
    print("Indexing completed.")
    warnings.resetwarnings()


if __name__ == "__main__":
    import fire

    fire.Fire(main)
