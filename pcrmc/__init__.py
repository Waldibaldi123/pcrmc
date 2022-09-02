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
        DUPLICATE_ERROR,
        BAD_INPUT_ERROR,
        NO_INIT_ERROR,
        NO_NAME_OR_ID_ERROR
) = range(12)

ERRORS = {
        DIR_ERROR: "config directory error",
        FILE_ERROR: "config file error",
        DB_READ_ERROR: "database read error",
        DB_WRITE_ERROR: "database write error",
        JSON_ERROR: "json parsing error",
        ID_ERROR: "id error",
        NOT_FOUND_ERROR: "not found error",
        DUPLICATE_ERROR: "duplicate error",
        BAD_INPUT_ERROR: "bad input error",
        NO_INIT_ERROR: "config files not found, run init",
        NO_NAME_OR_ID_ERROR: "Must give either name or id"
}
