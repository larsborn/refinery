#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    import javaobj.v2 as java
except ImportError:
    java = None

from .. import Unit
from ...lib.json import BytesAsArrayEncoder


class JavaEncoder(BytesAsArrayEncoder):

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if isinstance(obj, java.beans.JavaString):
                return str(obj)
            if isinstance(obj, java.beans.JavaInstance):
                cd = obj.classdesc
                fd = obj.field_data[cd]
                return dict(
                    isException=cd.is_exception,
                    isInnerClass=cd.is_inner_class,
                    isLocalInnerClass=cd.is_local_inner_class,
                    isStaticMemberClass=cd.is_static_member_class,
                    name=cd.name,
                    fields={t.name: v for t, v in fd.items()}
                )
            if isinstance(obj, java.beans.JavaField):
                return obj.class_name
            if isinstance(obj, java.beans.JavaEnum):
                return obj.value
            if isinstance(obj, java.beans.JavaArray):
                if obj.classdesc.name == '[B':
                    return bytearray(t & 0xFF for t in obj)
            raise


class dsjava(Unit):
    """
    Deserialize Java serialized data and re-serialize as JSON.
    """
    def process(self, data):
        with JavaEncoder as encoder:
            return encoder.dumps(java.loads(data)).encode(self.codec)
