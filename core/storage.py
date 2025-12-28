"""
Antigravity AI - Storage Manager
MinIO (S3-compatible) file storage
"""
from minio import Minio
from minio.error import S3Error
from pathlib import Path
import logging
from typing import Optional
import uuid
from datetime import timedelta

from core.config import settings

logger = logging.getLogger(__name__)


class StorageManager:
    """MinIO storage manager for video/audio files"""
    
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_SSL
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
                logger.info(f"✓ Created bucket: {self.bucket}")
        except S3Error as e:
            logger.error(f"Bucket creation failed: {e}")
    
    def upload_file(self, file_path: str, object_name: Optional[str] = None) -> str:
        """
        Upload file to MinIO
        
        Returns:
            object_name (key) in bucket
        """
        if object_name is None:
            # Generate unique object name
            ext = Path(file_path).suffix
            object_name = f"{uuid.uuid4()}{ext}"
        
        try:
            self.client.fput_object(
                self.bucket,
                object_name,
                file_path
            )
            logger.info(f"✓ Uploaded: {object_name}")
            return object_name
        except S3Error as e:
            logger.error(f"Upload failed: {e}")
            raise
    
    def get_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        """
        Get presigned URL for downloading
        
        Args:
            object_name: Object key in bucket
            expires: URL expiration time in seconds (default 1 hour)
        
        Returns:
            Presigned download URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise
    
    def delete_file(self, object_name: str):
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket, object_name)
            logger.info(f"✓ Deleted: {object_name}")
        except S3Error as e:
            logger.error(f"Delete failed: {e}")


# Global instance
storage = StorageManager()
