import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.images as SchemaImages
from src.functions import check_allowed_file
from werkzeug.utils import secure_filename
import src.constants as Consts
import os
class Images(object):
    
    @classmethod
    def list_images(cls,page,page_size):
        list_item = Repo.mImages.get_list(page=page, page_size=page_size)
        obj= SchemaImages.Item(many=True).dump(list_item)
        return obj
    
    @classmethod
    def exec_upload(cls,file,student_oid):
        if file.filename == '':
            raise ValueError("No file selected for uploading")
        if file and check_allowed_file(file.filename):
            name= secure_filename(file.filename)
            prefix=str(student_oid)
            true_filename=prefix+'.'+str(name.split('.')[-1])
            path=os.path.join(Consts.UPLOAD_FOLDER,true_filename)
            file.save(path)
        else:
            raise ValueError("File is not allowed")
        return