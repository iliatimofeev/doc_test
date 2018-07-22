from ..pykramdown import ParserWithTables


def print_nodes(ast):
  indent = 0
  for n in ast.walker():
    if n[1]:
      print ("  "*indent,n[0])
      indent += 1
    else:
      indent -= 1
  

md_alt = """
{: .suppress-error}
```json
// Single View Specification
{
  "data": ... ,
  "mark": "area",
  "encoding": ... ,
  ...
}
```

`area` represent multip....

## Documentation Overview
{:.no_toc}

somse unusual 

{:#ids}
## Heading with id: ids

some text more
"""

md_alt2 = """
```json
// Single View Specification
{
  "data": ... ,
  "mark": "area",
  "encoding": ... ,
  ...
}
```

`area` represent multip....

## Documentation Overview

somse unusual 

## Heading with id: ids

some text more
"""


def test_alt():
    parser = ParserWithTables()
    
    ast = parser.parse(md_alt)
    print_nodes(ast)

    ast = parser.parse(md_alt2)
    print_nodes(ast)


def test_ald():
    md_ald = """
{:#type}
## Scale Types #id type

just text

## It has red class
{:.red}
"""
    parser = ParserWithTables()
    
    ast = parser.parse(md_ald)
    print_nodes(ast)

    
 

def test_empty_header():
    md_table = """
|[P](#p)| B |
|:---|:-------:|
| x | y |

##I want it back

| B  | A |
|:---|---:|
| x | y 
"""
    md_table1 = """ pppp

| xx                   |                                |     |
|---------------------:|:------------------------------:|:---:|
| __X, Y__ | [Band](#band) / [Point](#point)<sup>2</sup>|     |    
"""
    md_list = """ pppp
* 1
    + 2.1
* 2
#H
"""
   
    parser = ParserWithTables()
    
    ast = parser.parse(md_table)
    # print(ast)

    # ast = parser.parse(md_list)
    print(ast)
