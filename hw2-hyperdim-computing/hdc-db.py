from hdc import *
import csv


class HDDatabase:

    def __init__(self):
        self.db = HDItemMem("db")
        self.codebook = HDCodebook("codebook")
        self.field_names = []

    def encode_string(self, value):
        if not self.codebook.has(value):
            self.codebook.add(value)
        
        return self.codebook.get(value)

    def decode_string(self, hypervec):
        return self.codebook.wta(hypervec)

    def encode_row(self, fields):
        if not self.field_names:
            self.field_names = list(fields.keys())
        else:
            assert self.field_names == list(fields.keys())

        field_value_hv = []

        for field, value in fields.items():
            field_hv = self.encode_string(field)
            value_hv = self.encode_string(value)
            field_value_hv.append(HDC.bind(field_hv, value_hv))

        return HDC.bundle(field_value_hv)

    def decode_row(self, hypervec):
        row = {}

        for field_name in self.field_names:
            field_name_hv = self.encode_string(field_name)
            bound_hv = HDC.bind(field_name_hv, hypervec)
            value = self.decode_string(bound_hv)
            row[field_name] = value

        return row

    def add_row(self, primary_key, fields):
        self.db.add(primary_key, self.encode_row(fields))

    def get_row(self, key):
        row_hv = self.db.get(key)
        return self.decode_row(row_hv)

    def get_value(self, key, field):
        row = self.get_row(key)
        return row[field]

    def get_matches(self, field_value_dict, threshold=0.4):
        field_value_pairs = []
        
        for field, value in field_value_dict.items():
            field_hv = self.encode_string(field)
            value_hv = self.encode_string(value)
            field_value_pairs.append(HDC.bind(field_hv, value_hv))

        query = HDC.bundle(field_value_pairs)

        return self.db.matches(query, threshold)

    def get_analogy(self, target_key, other_key, target_value):
        raise Exception("analogy query")


def load_json():
    data = {}
    with open("digimon.csv", "r") as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['Digimon']
            data[key] = rows
    return data


def build_database(data):
    HDC.SIZE = 10000
    db = HDDatabase()

    for key, fields in data.items():
        db.add_row(key, fields)

    return db


def summarize_result(data, result, summary_fn):
    print("---- # matches = %d ----" % len(list(result.keys())))
    for digi, distance in result.items():
        print("%f] %s: %s" % (distance, digi, summary_fn(data[digi])))


def digimon_basic_queries(data, db):

    print("===== virus-plant query =====")
    thr = 0.40
    digis = db.get_matches({"Type": "Virus", "Attribute": "Plant"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Type"] == "Virus" and row["Attribute"] == "Plant" else "false positive")

    print("===== champion query =====")
    thr = 0.40
    digis = db.get_matches({"Stage": "Champion"}, threshold=thr)
    summarize_result(data, digis, lambda row: "true match" if row["Stage"] == "Champion" else "false positive")


def digimon_test_encoding(data, db):
    strn = "tester"
    hv_test = db.encode_string(strn)
    rec_strn = db.decode_string(hv_test)
    print("original=%s" % strn)
    print("recovered=%s" % rec_strn)
    print("---")

    row = data["Wormmon"]
    hvect = db.encode_row(row)
    rec_row = db.decode_row(hvect)
    print("original=%s" % str(row))
    print("recovered=%s" % str(rec_row))
    print("---")


def digimon_value_queries(data, db):
    value = db.get_value("Lotosmon", "Stage")
    print("Lotosmon.Stage = %s" % value)

    targ_row = db.get_row("Lotosmon")
    print("Lotosmon" + str(targ_row))


def analogy_query(data, db):
    # Lotosmon is to Data as Imperialdramon PM is to <what field>

    targ_row = db.get_row("Lotosmon")
    other_row = db.get_row("Imperialdramon PM")
    print("Lotosmon has a a field with a Data value, what is the equivalent value in Imperialdramon PM's entry")
    value, dist = db.get_analogy(target_key="Lotosmon", other_key="Imperialdramon PM", target_value="Data")
    print("Lotosmon" + str(targ_row))
    print("Imperialdramon PM" + str(other_row))
    print("------")
    print("value: %s (dist=%f)" % (value, dist))
    print("expected result: Vaccine, the type of Imperialdramon PM")
    print("")


if __name__ == '__main__':
    data = load_json()
    db = build_database(data)
    digimon_test_encoding(data, db)
    # digimon_basic_queries(data, db)
    # digimon_value_queries(data, db)
    # digimon_test_encoding(data, db)
    # analogy_query(data, db)
