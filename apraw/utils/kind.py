def prepend_kind(org: str, kind: str) -> str:
    return kind + "_" + org.replace(kind + "_", "")
