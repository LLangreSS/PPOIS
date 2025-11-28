class Supplier:
    """
    Представляет компанию или организацию, поставляющую товары на склад.
    Содержит минимальную контактную информацию.
    """

    def __init__(self, id: str, name: str, contact_email: str, phone: str = ""):
        self.id = id
        self.name = name
        self.contact_email = contact_email
        self.phone = phone
        self.is_active = True

    def validate_contact_info(self) -> bool:
        """Проверяет корректность контактной информации."""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, self.contact_email))

    def get_contact_summary(self) -> str:
        """Возвращает сводку контактной информации."""
        contacts = [self.contact_email]
        if self.phone:
            contacts.append(self.phone)
        return ", ".join(contacts)

