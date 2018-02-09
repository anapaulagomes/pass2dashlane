from pathlib import Path
import os
import csv


PASS_DIRECTORY = Path.home() / '.password-store'


def _read_password(name):
    print(name)
    result = os.popen(f"pass {name}").read().rstrip()
    return result


def _retrieve_pass_files():
    for root, dirs, files in os.walk(PASS_DIRECTORY):
        if '.git' in dirs:
            dirs.remove('.git')
        for file_ in files:
            file_ = Path(root + '/' + file_)
            if '.gpg' in file_.suffixes:
                yield file_


def _pass_label(pass_file):
    return pass_file.relative_to(PASS_DIRECTORY).as_posix().replace('.gpg', '')


def _password_info(pass_file):
    name = _pass_label(pass_file)
    website = ''
    login = ''
    login2 = ''
    password = _read_password(name)
    category = 'Other'
    note = 'Exported using pass2dashlane'
    return [website, name, login, login2, password, category, note]


def read_passwords():
    data = []
    for pass_file in _retrieve_pass_files():
        data.append(_password_info(pass_file))
    return data


def to_csv(data):
    with open('pass2dashlane.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        header = [
            'website', 'name', 'login', 'login2', 'password', 'category', 'note']
        writer.writerow(header)
        writer.writerows(data)


if __name__ == '__main__':
    print("Reading passwords...")
    data = read_passwords()
    print("Converting to csv...")
    to_csv(data)
    print("Done.")
