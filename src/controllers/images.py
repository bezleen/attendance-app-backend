import bson
import pydash as py_
import src.models.repo as Repo
import src.schemas.images as SchemaImages


class Images(object):
    
    @classmethod
    def list_images(cls,page,page_size):
        list_item = Repo.mImages.get_list(page=page, page_size=page_size)
        obj= SchemaImages.Item(many=True).dump(list_item)
        return obj
    
