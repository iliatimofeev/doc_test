
INDENT = r"^(?:\t| {4})"
OPT_SPACE = r"\ {0,3}"

ALD_ID_CHARS = r"[\w-]"  # /
ALD_ANY_CHARS = r"\\\}|[^\}]"  # /
ALD_ID_NAME = r"\w"+ALD_ID_CHARS+r"*"  # /
ALD_CLASS_NAME = r"[^\s\.#]+"  # /
ALD_TYPE_KEY_VALUE_PAIR = r"("+ALD_ID_NAME+r")=(\"|')((?:\\\}|\\\2|[^\}\2])*?)\2"  # /
ALD_TYPE_CLASS_NAME = r"\.("+ALD_CLASS_NAME+r")"  # /
ALD_TYPE_ID_NAME = r"#([A-Za-z][\w:-]*)"  # /
ALD_TYPE_ID_OR_CLASS = r""+ALD_TYPE_ID_NAME+r"|"+ALD_TYPE_CLASS_NAME   # /
ALD_TYPE_ID_OR_CLASS_MULTI = r"((?:"+ALD_TYPE_ID_NAME+r"|"+ALD_TYPE_CLASS_NAME+r")+)"  # /
ALD_TYPE_REF = r"("+ALD_ID_NAME+r")"  # /
ALD_TYPE_ANY = r"(?:\A|\s)(?:"+ALD_TYPE_KEY_VALUE_PAIR+r"|"+ALD_TYPE_REF+r"|"+ALD_TYPE_ID_OR_CLASS_MULTI+r")(?=\s|\Z)"  # /
ALD_START = r"^"+OPT_SPACE+r"\{:("+ALD_ID_NAME+r"):("+ALD_ANY_CHARS+r"+)\}\s*?\n"  # /

EXT_STOP_STR = r"\{:/(%s)?\}" # "" 
EXT_START_STR = r"\{::(\w+)(?:\s("+ALD_ANY_CHARS+r"*?)|)(\/)?\}"  # "" 
EXT_BLOCK_START = r"^"+OPT_SPACE+r"(?:"+EXT_START_STR+r"|"+EXT_STOP_STR.format(ALD_ID_NAME)+r"\s*?\n"  # /
EXT_BLOCK_STOP_STR = r"^"+OPT_SPACE+EXT_STOP_STR+r"\s*?\n"  # "" 

IAL_BLOCK = r"\{:(?!:|\/)("+ALD_ANY_CHARS+r"+)\}\s*?\n" 
IAL_BLOCK_START = r"^"+OPT_SPACE+IAL_BLOCK   # /

BLOCK_EXTENSIONS_START = r"^"+OPT_SPACE+r"\{:"  # /
