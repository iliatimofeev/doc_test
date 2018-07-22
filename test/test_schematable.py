from ..schematable import prepare_table_header, prepare_schema_tabel
from altair import Root, Scale

def test_tabel():

    table, tbody = prepare_table_header(
        ["Property", "Type", "Description"],
        [10, 20, 50]
    )
    print(table.asdom().toprettyxml('  ', '\n'))
    # print(table.pformat())


def test_schema_tabel():
    props = "padding,paddingInner,paddingOuter,rangeStep,round"
    source = "Scale"
    schema = Root._schema['definitions'][source]
    # print(schema)
    table = prepare_schema_tabel(schema, props.split(',') )
    print(table.asdom().toprettyxml('  ', '\n'))
    # print(table.pformat())

