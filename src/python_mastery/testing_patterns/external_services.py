"""
External Services (To be Mocked)
===============================

This module simulates external dependencies (like a Payment API) that you
typically want to mock during testing to avoid:
1. Slow execution
2. Network dependency
3. Charging real credit cards
"""

import random
import time


class PaymentGateway:
    def charge(self, amount: float, currency: str) -> bool:
        """
        Simulates a charge.
        In real life, this would make an HTTP request to Stripe/PayPal.
        """
        print(f"Connecting to bank... charging {amount} {currency}")
        time.sleep(2)  # Slow!

        if random.random() < 0.1:
            raise ConnectionError("Bank API unavailable")

        return True


class UserManager:
    def __init__(self, payment_gateway: PaymentGateway):
        self.gateway = payment_gateway

    def upgrade_user(self, user_id: int) -> str:
        """
        Upgrades a user to premium status.
        DEPENDENCY: Requires PaymentGateway to work.
        """
        try:
            success = self.gateway.charge(99.00, "USD")
            if success:
                return "User upgraded successfully"
            else:
                return "Payment declined"
        except ConnectionError:
            return "Payment failed - try again later"
