import itertools
import operator
import csv
import re


def csv_to_dict(csv_name):
    contacts_dict = []
    with open(csv_name, "r", encoding="utf8") as file:
        rows = csv.reader(file, delimiter=",")
        contacts_list = list(rows)
        header = contacts_list[0]
        lines = contacts_list[1:]
        for i, j in enumerate(lines):
            contacts_dict.append({})
            for k, l in zip(header, j):
                contacts_dict[i].update({k: l})
    return contacts_dict


def dict_to_csv(dictionary, csv_name):
    header = list(dictionary[0].keys())
    with open(csv_name, "w", newline='', encoding="utf8") as file:
        writer = csv.DictWriter(file, delimiter=",", fieldnames=header)
        writer.writeheader()
        writer.writerows(dictionary)


def phone_to_phone(csv_name_in, csv_name_out):
    with open(csv_name_in, "r", encoding="utf8") as file:
        csv_text = file.read()
    patt_phone = r"(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d+)?\)?"
    phone_corr = r"+7(\2)\3-\4-\5\6\7\8"
    text_corr = re.sub(patt_phone, phone_corr, csv_text)
    with open(csv_name_out, "w+", encoding="utf8") as file:
        csv_text_out = file.write(text_corr)


def correct_name(csv_name):
    contact_dict = csv_to_dict(csv_name)
    for line in contact_dict:
        split_line = line['lastname'].split(' ')
        if len(split_line) > 1:
            line['lastname'] = split_line[0]
            line['firstname'] = split_line[1]
            if len(split_line) > 2:
                line['surname'] = split_line[2]
        split_line2 = line['firstname'].split(' ')
        if len(split_line2) > 1:
            line['firstname'] = split_line2[0]
            line['surname'] = split_line2[1]
    return contact_dict


def merge_lines(lines):
    unique = ['firstname', 'lastname']
    unique_group = operator.itemgetter(*unique)
    lines.sort(key=unique_group)
    unique_group_out = itertools.groupby(lines, unique_group)
    merged_lines = []
    for (first_name, last_name), i in unique_group_out:
        merged_lines.append({'lastname': last_name, 'firstname': first_name})
        for j in i:
            m = merged_lines[-1]
            for k, l in j.items():
                if k not in m or m[k] == '':
                    m[k] = l

    return merged_lines


if __name__ == '__main__':
    csv_name_in = "phonebook_raw.csv"
    csv_name_iteration = "phonebook_iteration.csv"
    csv_name_out = "phonebook.csv"
    phone_to_phone(csv_name_in, csv_name_iteration)
    correct_name = correct_name(csv_name_iteration)
    merge_lines = merge_lines(correct_name)
    dict_to_csv(merge_lines, csv_name_out)
