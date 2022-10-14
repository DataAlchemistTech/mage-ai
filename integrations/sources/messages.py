from singer.messages import SchemaMessage as SchemaMessageOriginal, write_message
from typing import List


class SchemaMessage(SchemaMessageOriginal):
    def __init__(self, replication_method: str = None, **kwargs):
        super().__init__(**kwargs)
        self.replication_method = replication_method

    def asdict(self):
        result = super().asdict()
        if self.replication_method:
            result['replication_method'] = self.replication_method

        return result


def write_schema(
    stream_name: str,
    schema,
    key_properties: List[str],
    bookmark_properties: List[str] = None,
    replication_method: str = None,
    stream_alias: str = None,
) -> None:
    """Write a schema message.

    stream = 'test'
    schema = {'properties': {'id': {'type': 'integer'}, 'email': {'type': 'string'}}}  # nopep8
    key_properties = ['id']
    write_schema(stream, schema, key_properties)
    """
    if isinstance(key_properties, (str, bytes)):
        key_properties = [key_properties]
    if not isinstance(key_properties, list):
        raise Exception("key_properties must be a string or list of strings")

    write_message(
        SchemaMessage(
            bookmark_properties=bookmark_properties,
            key_properties=key_properties,
            replication_method=replication_method,
            schema=schema,
            stream=(stream_alias or stream_name),
        ),
    )
