import time
import re
import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("security_audit")

class AdvancedSecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.request_counts = {}
        self.RATE_LIMIT_WINDOW = 60 
        self.MAX_REQUESTS = 100      
        
        self.threat_patterns = [
            re.compile(r"(\%27)|(\')|(\-\-)|(\%23)|(#)", re.IGNORECASE),
            re.compile(r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))", re.IGNORECASE),
            re.compile(r"<script[^>]*>[\s\S]*?</script>", re.IGNORECASE),
            re.compile(r"UNION\s+SELECT", re.IGNORECASE)
        ]

    def process_request(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        self.request_counts[client_ip] = [t for t in self.request_counts[client_ip] if current_time - t < self.RATE_LIMIT_WINDOW]
        
        if len(self.request_counts[client_ip]) >= self.MAX_REQUESTS:
            logger.warning(f"RATE_LIMIT_EXCEEDED | IP: {client_ip} | Path: {request.path}")
            return HttpResponseForbidden("<h1>403 Forbidden: Rate limit exceeded. Too many requests.</h1>")
            
        self.request_counts[client_ip].append(current_time)

        query_string = request.META.get('QUERY_STRING', '')
        body_data = request.body.decode('utf-8', errors='ignore')
        payload_to_check = query_string + " " + body_data

        for pattern in self.threat_patterns:
            if pattern.search(payload_to_check):
                logger.critical(f"SECURITY_THREAT_DETECTED | IP: {client_ip} | Path: {request.path} | Payload matched")
                return HttpResponseForbidden("<h1>403 Forbidden: Potential security threat detected in request payload.</h1>")

        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip