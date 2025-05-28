from .doc_loader import CustomizedOcrDocLoader
from .pdf_loader import CustomizedOcrPdfLoader
from .sqldata_loader import CustomizedSQLDataLoader


LOADER_MAPPING = {
    "CustomizedOcrPdfLoader": [".pdf"],
    "CustomizedOcrDocLoader": [".docx", ".doc"],
    "CustomizedSQLDataLoader":[".sqldata"]
}
