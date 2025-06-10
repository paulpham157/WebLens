# Browser Use Cloud API Documentation

## Tổng quan

Tài liệu này tổng hợp thông tin quan trọng từ [tài liệu chính thức của Browser Use Cloud API](https://docs.browser-use.com/cloud/implementation) để hỗ trợ việc chuyển đổi framework WebLens từ Playwright sang Browser Use Cloud API.

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Cấu hình API](#cấu-hình-api)
  - [Thiết lập API Key](#thiết-lập-api-key)
  - [Tùy chỉnh Base URL](#tùy-chỉnh-base-url)
- [Các API endpoints chính](#các-api-endpoints-chính)
- [Triển khai cơ bản](#triển-khai-cơ-bản)
- [Kiểm soát tác vụ](#kiểm-soát-tác-vụ)
- [Structured Output](#structured-output)
- [Webhooks](#webhooks)
- [Các best practices](#các-best-practices)
- [Ví dụ tích hợp với WebLens](#ví-dụ-tích-hợp-với-weblens)
  - [Best Practices khi tùy chỉnh Base URL](#best-practices-khi-tùy-chỉnh-base-url)

## Giới thiệu

Browser Use là một giải pháp cloud API cho phép tự động hóa trình duyệt web qua API. Thay vì sử dụng Playwright để điều khiển trình duyệt cục bộ, WebLens có thể sử dụng Browser Use Cloud API để thực hiện các tác vụ tự động hóa trình duyệt trên cloud.

Ưu điểm chính:
- Không cần cài đặt trình duyệt hoặc drivers
- Giảm tải việc xử lý trên máy local
- Khả năng mở rộng tốt hơn
- Hỗ trợ giải captcha tự động
- Tích hợp sẵn trí tuệ nhân tạo để thực hiện tác vụ phức tạp

## Cài đặt

WebLens đã loại bỏ Playwright và chỉ sử dụng `browser-use` package. Để cài đặt hoặc cập nhật:

```bash
pip install browser-use>=0.2.0
```

## Cấu hình API

### Thiết lập API Key

WebLens yêu cầu API key để kết nối với Browser Use Cloud API. Bạn có thể đặt API key trong tệp cấu hình `.env`:

```bash
# Trong tệp .env
BROWSER_USE_API_KEY=your_api_key_here
```

### Tùy chỉnh Base URL

Mặc định, WebLens sử dụng base URL của Browser Use Cloud API chính thức: `https://api.browser-use.com/api/v1`. 
Tuy nhiên, trong một số trường hợp bạn có thể cần tùy chỉnh base URL này, ví dụ:

- Sử dụng phiên bản API mới
- Kết nối tới instance Browser Use riêng
- Sử dụng proxy để tối ưu hóa kết nối ở các khu vực địa lý khác nhau

Để tùy chỉnh base URL, hãy đặt biến môi trường `BROWSER_USE_BASE_URL` trong tệp `.env`:

```bash
# Trong tệp .env
BROWSER_USE_API_KEY=your_api_key_here
BROWSER_USE_BASE_URL=https://your-custom-api-endpoint.com/api/v1
```

WebLens sẽ tự động sử dụng base URL tùy chỉnh khi khởi tạo các agent.

## Các API endpoints chính

Browser Use Cloud API bao gồm các endpoints sau:

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/api/v1/run-task` | POST | Tạo một tác vụ tự động hóa mới |
| `/api/v1/task/{task_id}` | GET | Lấy thông tin chi tiết về một tác vụ |
| `/api/v1/task/{task_id}/status` | GET | Kiểm tra trạng thái của một tác vụ |
| `/api/v1/pause-task` | PUT | Tạm dừng một tác vụ đang chạy |
| `/api/v1/resume-task` | PUT | Tiếp tục một tác vụ đã tạm dừng |
| `/api/v1/stop-task` | PUT | Dừng hẳn một tác vụ |

## Triển khai cơ bản

Dưới đây là ví dụ triển khai cơ bản sử dụng Python với thư viện `requests`:

```python
import json
import time
import requests

BROWSER_USE_API_KEY = 'your_api_key_here'
BROWSER_USE_BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {'Authorization': f'Bearer {BROWSER_USE_API_KEY}'}


def create_task(instructions: str) -> str:
    """Create a new browser automation task"""
    response = requests.post(f'{BROWSER_USE_BASE_URL}/run-task', headers=HEADERS, json={'task': instructions})
    return response.json()['id']


def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get current task status"""
    response = requests.get(f'{BROWSER_USE_BASE_URL}/task/{task_id}/status', headers=HEADERS)
    return response.json()


def get_task_details(task_id: str) -> Dict[str, Any]:
    """Get full task details including output"""
    response = requests.get(f'{BROWSER_USE_BASE_URL}/task/{task_id}', headers=HEADERS)
    return response.json()


def wait_for_completion(task_id: str, poll_interval: int = 2) -> Dict[str, Any]:
    """Poll task status until completion"""
    count = 0
    unique_steps = []
    while True:
        details = get_task_details(task_id)
        new_steps = details['steps']
        # use only the new steps that are not in unique_steps.
        if new_steps != unique_steps:
            for step in new_steps:
                if step not in unique_steps:
                    print(json.dumps(step, indent=4))
            unique_steps = new_steps
        count += 1
        status = details['status']

        if status in ['finished', 'failed', 'stopped']:
            return details
        time.sleep(poll_interval)


def main() -> None:
    task_id = create_task('Open https://www.google.com and search for openai')
    print(f'Task created with ID: {task_id}')
    task_details = wait_for_completion(task_id)
    print(f"Final output: {task_details['output']}")


if __name__ == '__main__':
    main()
```

## Kiểm soát tác vụ

Ví dụ về cách tạm dừng và tiếp tục một tác vụ:

```python
def control_task():
    # Create a new task
    task_id = create_task("Go to google.com and search for Browser Use")

    # Wait for 5 seconds
    time.sleep(5)

    # Pause the task
    requests.put(f"{BROWSER_USE_BASE_URL}/pause-task?task_id={task_id}", headers=HEADERS)
    print("Task paused! Check the live preview.")

    # Wait for user input
    input("Press Enter to resume...")

    # Resume the task
    requests.put(f"{BROWSER_USE_BASE_URL}/resume-task?task_id={task_id}", headers=HEADERS)

    # Wait for completion
    result = wait_for_completion(task_id)
    print(f"Task completed with output: {result['output']}")
```

## Structured Output

Sử dụng Pydantic để định nghĩa cấu trúc output:

```python
import json  
import os  
import time  
from typing import List  

import requests  
from pydantic import BaseModel 


BROWSER_USE_API_KEY = os.getenv("BROWSER_USE_API_KEY")
BROWSER_USE_BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {
    "Authorization": f"Bearer {BROWSER_USE_API_KEY}",
    "Content-Type": "application/json"
}


# Define output schema using Pydantic
class SocialMediaCompany(BaseModel):
    name: str
    market_cap: float
    headquarters: str
    founded_year: int


class SocialMediaCompanies(BaseModel):
    companies: List[SocialMediaCompany]


def create_structured_task(instructions: str, schema: dict) -> Dict[str, Any]:
    """Create a task that expects structured output"""
    payload = {
        "task": instructions,
        "structured_output_json": json.dumps(schema)
    }
    response = requests.post(f"{BROWSER_USE_BASE_URL}/run-task", headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def wait_for_task_completion(task_id: str, poll_interval: int = 5) -> None:
    """Poll task status until it completes"""
    while True:
        response = requests.get(f"{BROWSER_USE_BASE_URL}/task/{task_id}/status", headers=HEADERS)
        response.raise_for_status()
        status = response.json()
        if status == "finished":
            break
        elif status in ["failed", "stopped"]:
            raise RuntimeError(f"Task {task_id} ended with status: {status}")
        print("Waiting for task to finish...")
        time.sleep(poll_interval)


def fetch_task_output(task_id: str) -> Any:
    """Retrieve the final task result"""
    response = requests.get(f"{BROWSER_USE_BASE_URL}/task/{task_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()["output"]


def main():
    schema = SocialMediaCompanies.model_json_schema()
    task_id = create_structured_task(
        "Get me the top social media companies by market cap",
        schema
    )
    print(f"Task created with ID: {task_id}")

    wait_for_task_completion(task_id)
    print("Task completed!")

    output = fetch_task_output(task_id)
    print("Raw output:", output)

    try:
        parsed = SocialMediaCompanies.model_validate_json(output)
        print("Parsed output:")
        print(parsed)
    except Exception as e:
        print(f"Failed to parse structured output: {e}")
```

## Webhooks

Bạn có thể thiết lập webhooks để nhận thông báo về các sự kiện trong tác vụ của mình. Dưới đây là một ví dụ về cách xử lý webhooks với FastAPI:

```python
import hashlib  
import hmac  
import json  
import os  

import uvicorn  
from fastapi import FastAPI, Request, HTTPException  

app = FastAPI()

SECRET_KEY = os.getenv['SECRET_KEY']
if SECRET_KEY is None:  
    raise ValueError("The SECRET_KEY environment variable has not been set.")  


def verify_signature(payload: Dict[str, Any], timestamp: str, received_signature: str) -> bool:
    message = f'{timestamp}.{json.dumps(payload, separators=(",", ":"), sort_keys=True)}'
    expected_signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_signature, received_signature)

@app.post('/webhook')
async def webhook(request: Request) -> Dict[str, str]:
    body = await request.json()

    timestamp = request.headers.get('X-Browser-Use-Timestamp')
    signature = request.headers.get('X-Browser-Use-Signature')
    if not timestamp or not signature:
        raise HTTPException(status_code=400, detail='Missing timestamp or signature')

    if not verify_signature(body, timestamp, signature):
        raise HTTPException(status_code=403, detail='Invalid signature')

    # Handle different event types
    event_type = body.get('type')
    if event_type == 'agent.task.status_update':
        # Handle task status update
        print('Task status update received:', body['payload'])
    elif event_type == 'test':
        # Handle test webhook
        print('Test webhook received:', body['payload'])
    else:
        print('Unknown event type:', event_type)

    return {'status': 'success', 'message': 'Webhook received'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
```

Các loại sự kiện webhook:

| Loại sự kiện | Mô tả |
|--------------|-------|
| agent.task.status_update | Cập nhật trạng thái của tác vụ đang chạy |

Các trạng thái tác vụ trong webhook:

| Trạng thái | Mô tả |
|------------|-------|
| initializing | Tác vụ đang khởi tạo |
| started | Tác vụ đã bắt đầu (trình duyệt đã khả dụng) |
| paused | Tác vụ đã tạm dừng giữa quá trình thực thi |
| stopped | Tác vụ đã bị dừng giữa quá trình thực thi |
| finished | Tác vụ đã hoàn thành |

## Các tham số API chính

### `/api/v1/run-task`

| Tham số | Loại | Mô tả | Bắt buộc |
|---------|------|-------|----------|
| task | string | Mô tả nhiệm vụ cho agent thực hiện | Có |
| secrets | object | Dictionary chứa thông tin secret mà agent sẽ dùng | Không |
| allowed_domains | array | Danh sách domain được phép truy cập | Không |
| save_browser_data | boolean | Lưu cookies và dữ liệu trình duyệt | Không |
| structured_output_json | string | Schema JSON cho output có cấu trúc | Không |
| llm_model | string | Model LLM sử dụng (mặc định: gpt-4o) | Không |
| use_adblock | boolean | Sử dụng adblock | Không |
| use_proxy | boolean | Sử dụng proxy (cần thiết để giải captcha) | Không |
| proxy_country_code | string | Mã quốc gia cho proxy (mặc định: 'us') | Không |
| highlight_elements | boolean | Highlight các element trên trang | Không |
| included_file_names | array | File names để đính kèm | Không |

## Các best practices

1. **Xử lý API key an toàn**: Sử dụng environment variables hoặc secret management system thay vì hardcoding API keys.
2. **Tùy chỉnh URL cơ sở**: Sử dụng biến môi trường `BROWSER_USE_BASE_URL` để tùy chỉnh endpoint API, ví dụ khi cần sử dụng proxy, server riêng, hoặc môi trường staging.
3. **Xử lý lỗi**: Luôn cài đặt xử lý lỗi đầy đủ cho các API calls.
4. **Sử dụng Structured Output**: Khi cần dữ liệu có cấu trúc rõ ràng, hãy sử dụng Structured Output với schema Pydantic.
5. **Giới hạn domain**: Thiết lập `allowed_domains` để tăng tính bảo mật.
6. **Sử dụng proxy**: Bật tùy chọn `use_proxy` khi cần giải quyết captchas.
7. **Kiểm tra trạng thái**: Kiểm tra trạng thái tác vụ thường xuyên và xử lý từng trường hợp cụ thể.
8. **Xác minh webhook signatures**: Luôn xác minh chữ ký webhooks trước khi xử lý payload.

## Ví dụ tích hợp với WebLens

Dưới đây là một ví dụ về cách tích hợp Browser Use Cloud API với WebLens:

```python
# Ví dụ code browser_manager.py

import json
import time
import logging
from typing import Dict, List, Optional, Any

import requests
from weblens.utils.logger import setup_logger

logger = setup_logger(__name__)

class BrowserManager:
    """
    BrowserManager
    """
    def __init__(self, api_key: str, base_url: str = "https://api.browser-use.com/api/v1") -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def create_task(self, 
                   instructions: str, 
                   secrets: Optional[Dict[str, str]] = None, 
                   allowed_domains: Optional[List[str]] = None,
                   structured_output_json: Optional[str] = None,
                   use_adblock: bool = True) -> str:
        """Create a new browser automation task"""
        payload = {
            "task": instructions,
            "use_adblock": use_adblock
        }
        
        if secrets:
            payload["secrets"] = secrets
            
        if allowed_domains:
            payload["allowed_domains"] = allowed_domains
            
        if structured_output_json:
            payload["structured_output_json"] = structured_output_json
            
        try:
            response = requests.post(f"{self.base_url}/run-task", headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()["id"]
        except requests.RequestException as e:
            logger.error(f"Failed to create task: {str(e)}")
            raise
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the current status of a task"""
        try:
            response = requests.get(f"{self.base_url}/task/{task_id}/status", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get task status: {str(e)}")
            raise
    
    def get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get full details about a task"""
        try:
            response = requests.get(f"{self.base_url}/task/{task_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get task details: {str(e)}")
            raise
    
    def pause_task(self, task_id: str) -> None:
        """Pause a running task"""
        try:
            response = requests.put(f"{self.base_url}/pause-task?task_id={task_id}", headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to pause task: {str(e)}")
            raise
    
    def resume_task(self, task_id: str) -> None:
        """Resume a paused task"""
        try:
            response = requests.put(f"{self.base_url}/resume-task?task_id={task_id}", headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to resume task: {str(e)}")
            raise
    
    def stop_task(self, task_id: str) -> None:
        """Stop a running task"""
        try:
            response = requests.put(f"{self.base_url}/stop-task?task_id={task_id}", headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to stop task: {str(e)}")
            raise
    
    def wait_for_completion(self, task_id: str, poll_interval: int = 2, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Poll task status until completion or timeout
        
        Args:
            task_id: The ID of the task to monitor
            poll_interval: Time in seconds between status checks
            timeout: Maximum time in seconds to wait (None for no timeout)
            
        Returns:
            Dict containing task details
        """
        start_time = time.time()
        unique_steps = []
        
        while True:
            # Check timeout
            if timeout and time.time() - start_time > timeout:
                logger.warning(f"Task {task_id} timed out after {timeout} seconds")
                self.stop_task(task_id)
                return self.get_task_details(task_id)
            
            # Get task details
            details = self.get_task_details(task_id)
            status = details['status']
            
            # Process new steps
            new_steps = details.get('steps', [])
            if new_steps != unique_steps:
                for step in new_steps:
                    if step not in unique_steps:
                        logger.info(f"Task step: {json.dumps(step)}")
                unique_steps = new_steps
            
            # Check if task is complete
            if status in ['finished', 'failed', 'stopped']:
                if status == 'failed':
                    logger.error(f"Task {task_id} failed")
                elif status == 'stopped':
                    logger.warning(f"Task {task_id} was stopped")
                else:
                    logger.info(f"Task {task_id} finished successfully")
                return details
            
            # Wait before checking again
            time.sleep(poll_interval)
```

Sử dụng ví dụ:

```python
# Ví dụ sử dụng BrowserManager trong WebLens

import os
from weblens.core.browser_manager import BrowserManager
from weblens.config import config

# Các biến môi trường đã được đọc tự động từ config.py
# Cấu hình Browser Use API trong file .env
# BROWSER_USE_API_KEY='your_api_key_here'
# BROWSER_USE_BASE_URL='https://api.browser-use.com/api/v1'  # Mặc định hoặc URL tùy chỉnh

# BrowserManager sẽ sử dụng cấu hình từ config instance, bao gồm base_url nếu được đặt
browser_manager = BrowserManager()
await browser_manager.start()

# Tạo agent mới với tác vụ cụ thể
# Agent sẽ được tạo với base_url và api_key từ config
agent = await browser_manager.create_agent(
    task="Go to https://example.com and extract all heading text"
)

# Chạy agent và lấy kết quả
result = await agent.run()
print(f"Output: {result}")

# Dọn dẹp tài nguyên khi hoàn thành
await browser_manager.stop()
```

### Best Practices khi tùy chỉnh Base URL

1. **Kiểm tra kết nối**: Luôn kiểm tra kết nối trước khi triển khai:
   ```python
   import requests
   
   def test_connection(base_url, api_key):
       headers = {'Authorization': f'Bearer {api_key}'}
       try:
           response = requests.get(f"{base_url}/ping", headers=headers)
           return response.status_code == 200
       except Exception as e:
           print(f"Connection error: {e}")
           return False
   ```

2. **Xử lý failover**: Chuẩn bị cơ chế failover trong trường hợp URL tùy chỉnh không hoạt động:
   ```python
   # Trong config.py hoặc module xử lý lỗi
   def get_reliable_base_url():
       custom_url = os.getenv("BROWSER_USE_BASE_URL") 
       if custom_url and test_connection(custom_url, api_key):
           return custom_url
       return "https://api.browser-use.com/api/v1"  # Fallback to default
   ```

3. **Quản lý môi trường**: Sử dụng các base URL khác nhau cho các môi trường phát triển, kiểm thử và sản xuất:
   ```bash
   # .env.dev
   BROWSER_USE_BASE_URL=https://dev-api.browser-use.com/api/v1
   
   # .env.prod
   BROWSER_USE_BASE_URL=https://api.browser-use.com/api/v1
   ```

Đây là một ví dụ tích hợp cơ bản, trong môi trường thực tế, bạn cần thêm xử lý lỗi, retry logic, và khả năng cấu hình nâng cao hơn.
