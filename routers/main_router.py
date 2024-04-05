from controllers.upload_controller import upload_file
from controllers.read_controller import read_file
from controllers.update_controller import update_file
from controllers.delete_controller import delete_file

def upload(file_path, file_type):
    return upload_file(file_path, file_type)

def read(file_id, file_type):
    return read_file(file_id, file_type)

def update(file_id, file_type, updated_content):
    return update_file(file_id, file_type, updated_content)

def delete(file_id, file_type):
    return delete_file(file_id, file_type)
