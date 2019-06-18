
try:
    from io import StringIO

except:
    from StringIO import StringIO


import requests

from .base import API, Model

class ImagesQuery(Model):
    _QUERY_ = ["page"]


class ImagesCreateUpdate(Model):
    _SCHEMA_ = {
        "image": ("str", Model.REQUIRED),
        "product": ("str", Model.REQUIRED)
    }


class Images(API):
    @property
    def list(self):
        return self.resource(
            model=ImagesQuery,
            uri="/v2/product-images/",
            method="get"
        )

    def create_from_url(self, **data):
        data["image"] = self.load_image_from_url(data["url"])

        return self.resource(
            model=ImagesCreateUpdate,
            uri="/v2/product-images/",
            method="attachment",
            **data
        )

    def create_from_raw_io(self, **data):
        return self.resource(
            model=ImagesCreateUpdate,
            uri="/v2/product-images/",
            method="attachment",
            **data
        )

    def delete(self, image_id):
        return self.resource(
            model=ImagesQuery,
            uri="/v2/product-images/{id}/",
            path_param=image_id,
            method="delete"
        )

    def get_by_id(self, image_id):
        return self.resource(
            model=ImagesQuery,
            uri="/v2/product-images/{id}/",
            path_param=image_id,
            method="get"
        )

    def load_image_from_file(self, file_path):
        fp = open(file_path, "rb")
        return fp

    def load_image_from_url(self, url):
        res = requests.get(url)
        return self.load_image_binary_as_stringio(res.content)

    def load_image_binary_as_stringio(self, binary):
        f = StringIO()
        f.write(binary)
        f.seek(0)
        return f

