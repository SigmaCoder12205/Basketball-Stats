import socket
import uuid
import urllib.request
from typing import Optional, Dict, Any
from datetime import datetime, timezone

class Logging:
    def __init__(self, service_name: str = "", user_id: str = "Unknown"):
        self.service_name = service_name
        self.host = socket.gethostname()
        self.public_ip = self.get_public_ip()
        self.user_id = user_id

    def get_public_ip(self) -> str:
        try:
            return urllib.request.urlopen("https://api.ipify.org").read().decode()
        except Exception as e:
            return socket.gethostbyname(socket.gethostname())
        
    def create_log(
        self,
        level: str,
        message: str,
        where: str,
        error: Optional[Dict[str, Any]] = None,
        service_name: str = "access_data_service",
        host: str = None,
        user_id: str = "N/A",
        source_ip: str = "N/A",
        request_id: str = None
    ) -> Dict[str, Any]:
        if host is None:
            host = socket.gethostname()
        if request_id is None:
            request_id = str(uuid.uuid4())
            
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "log_level": level,
            "service_name": service_name,
            "host": host,
            "message": message,
            "where": where,
            "user_id": user_id,
            "source_ip": source_ip,
            "request_id": request_id,
            **({"error": error} if error else {})
        }