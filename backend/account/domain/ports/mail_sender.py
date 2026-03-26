from typing import Protocol


class MailSender(Protocol):
    def send_code(self, code: int, to_email: str) -> None: ...
