import aiohttp
import asyncio
import base64
import json
import uuid
from typing import Dict, Any, Optional

from config import settings

class YooKassaClient:
    def __init__(self, shop_id: str, secret_key: str) -> None:
        self.shop_id: str = shop_id
        self.secret_key: str = secret_key
        self.auth_header: str = base64.b64encode(f"{shop_id}:{secret_key}".encode()).decode()
        self.base_url: str = "https://api.yookassa.ru/v3/payments"

    async def create_payment(
        self,
        amount: float,
        currency: str = "RUB",
        description: str = "Test payment",
        return_url: str = "https://your-site.com/return"
    ) -> Dict[str, Any]:
        """
        Создает платеж в ЮKassa и возвращает JSON-ответ.
        """
        idempotence_key: str = str(uuid.uuid4())
        headers: Dict[str, str] = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json",
            "Idempotence-Key": idempotence_key
        }

        data: Dict[str, Any] = {
            "amount": {"value": f"{amount:.2f}", "currency": currency},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": description
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, headers=headers, data=json.dumps(data)) as resp:
                result: Dict[str, Any] = await resp.json()
                return result
            

    async def get_payment_status(self, payment_id: str) -> Optional[str]:
        """
        Получает статус платежа по payment_id.
        Возвращает строку статуса или None, если ошибка.
        """
        url: str = f"{self.base_url}/{payment_id}"
        headers: Dict[str, str] = {
            "Authorization": f"Basic {self.auth_header}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return None
                result: Dict[str, Any] = await resp.json()
                return result.get("status")


yookassa = YooKassaClient(settings.payment.shop_id, settings.payment.secret_key)