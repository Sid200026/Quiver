import enum


class ParseError(enum.Enum):
    bad_status = "Could not parse file"
