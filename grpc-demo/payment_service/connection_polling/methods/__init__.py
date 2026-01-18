from ..methods.card import CardPayment

METHOD_REGISTRY = {
    "CARD": CardPayment(),
    # "WALLET": WalletPayment(),
}
