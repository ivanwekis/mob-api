from queue import Empty
from pymongo import MongoClient
import argparse


def read_csv(input_file):
    with open(input_file) as csv_file:
        data = csv_file.read()
        data_list = data.split("\n")
        data = None
        header_aux = data_list[0].split(",")
        header=[]
        for word in header_aux:
            header.append(word.replace("\n", "").replace('"', ''))

        data_list_dictionary = []
        for row in range(1, len(data_list)-1):
            dictionary_aux = {}
            row_list = data_list[row].split(",")
            for column in range(len(header)):
                if len(header) == len(row_list):
                    dictionary_aux[header[column]] = row_list[column].replace("\n", "").replace('"', '')
            data_list_dictionary.append(dictionary_aux)
        return data_list_dictionary


def write_csv(input_file, data_list_dictionary):
    MONGO_URI = "mongodb://localhost"
    client = MongoClient(MONGO_URI)
    db = client["weatherdata"]
    collection = db[str(input_file).replace(".csv","")]
    for dict in data_list_dictionary:
        if not dict is Empty:
            collection.insert_one(dict)


def main(input_file):
    data_list_dictionary = read_csv(input_file)
    write_csv(input_file,data_list_dictionary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        type=str,
        help="Name of the input file. By default ='data_files/tests.csv'",
    )
    args = parser.parse_args()
    main(args.input_file)
