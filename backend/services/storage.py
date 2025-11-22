"""
Storage service for file management (S3)
"""

import os
from typing import BinaryIO
from loguru import logger


class StorageService:
    """File storage service (S3)"""
    
    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET", "finagent-storage")
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        folder: str = "receipts"
    ) -> str:
        """Upload file to S3 and return URL"""
        # In production, upload to S3
        url = f"https://storage.finagent.pro/{folder}/{filename}"
        logger.info(f"File uploaded: {url}")
        return url
    
    async def delete_file(self, url: str) -> bool:
        """Delete file from S3"""
        # In production, delete from S3
        logger.info(f"File deleted: {url}")
        return True
