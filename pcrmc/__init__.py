"""Top-level package for pcrmc"""
# pcrmc/__init__.py

__app_name__ = "pcrmc"
__version__ = "0.1.0"

(
        SUCCESS,
        DIR_ERROR,
        FILE_ERROR,
        DB_READ_ERROR,
        DB_WRITE_ERROR,
        JSON_ERROR,
        ID_ERROR,
        NOT_FOUND_ERROR,
        DUPLICATE_ERROR
) = range(9)

ERRORS = {
        DIR_ERROR: "config directory error",
        FILE_ERROR: "config file error",
        DB_READ_ERROR: "database read error",
        DB_WRITE_ERROR: "database write error",
        JSON_ERROR: "json parsing error",
        ID_ERROR: "id error",
        NOT_FOUND_ERROR: "not found",
        DUPLICATE_ERROR: "found more than once"
}
