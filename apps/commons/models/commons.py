import uuid
from copy import deepcopy

from django.db import models

from apps.commons.utils.commons import nested_getattr
from apps.commons.utils.slugify import unique_slugify


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampModel):
    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(max_length=255, editable=False)

    class Meta:
        abstract = True

    def _get_slug_text(self):
        assert any([hasattr(self, 'name'), hasattr(self, 'title')])
        slug_text = ''
        if hasattr(self, 'name'):
            slug_text = self.name.lower()
        elif hasattr(self, 'title'):
            slug_text = self.title.lower()
        return slug_text

    def _get_previous_slug_text(self):
        if self.id:
            _pre_data = self.__class__.objects.get(id=self.id)
            return _pre_data._get_slug_text()
        return None

    def save(self, *args, **kwargs):
        slug_text = self._get_slug_text()
        pre_slug_text = self._get_previous_slug_text()
        if not self.slug or slug_text != pre_slug_text:
            unique_slugify(self, slug_text)
        super().save(*args, **kwargs)


class UUIDModel(models.Model):
    uuid = models.CharField(max_length=6, default='', editable=False, unique=True)

    class Meta:
        abstract = True

    @staticmethod
    def get_uuid():
        return uuid.uuid4().hex[:6]

    def _get_valid_uuid(self):
        while True:
            _uuid = self.get_uuid()
            if not self.__class__.objects.filter(uuid=_uuid).exists():
                return _uuid

    def save(self, *args, **kwargs):
        uuid_text = self._get_valid_uuid()
        setattr(self, 'uuid', uuid_text)
        super().save(*args, **kwargs)


class SerializedModal:

    def __repr__(self):
        return str(self.to_dict())

    def get_model_reference(self):
        assert hasattr(self, 'model_reference'), 'You must specify model_reference to use SerializedModel'
        return self.model_reference

    def to_dict(self):
        model_reference = self.get_model_reference()
        data = deepcopy(model_reference)
        return self.get_data(data)

    def get_data(self, data):
        for key, reference in deepcopy(data).items():
            if not isinstance(reference, dict):
                data[key] = nested_getattr(self, reference)
            elif isinstance(reference, dict):
                data[key] = self.get_data(reference)
        return data
