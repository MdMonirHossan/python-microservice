class PaymentMethod:
    async def process(self, request, registry):
        raise NotImplementedError
