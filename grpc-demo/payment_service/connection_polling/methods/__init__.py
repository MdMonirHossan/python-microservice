from payment_service.methods.card import CardPayment
from payment_service.methods.wallet import WalletPayment

METHOD_REGISTRY = {
    "CARD": CardPayment(),
    "WALLET": WalletPayment(),
}
