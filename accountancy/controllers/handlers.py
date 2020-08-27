from accountancy.models import File
from accountancy.utility.upload_module import parse_file_bd


def handle_uploaded_file(f, path, filename):
    # print(filename)
    return parse_file_bd(f, path, filename)
