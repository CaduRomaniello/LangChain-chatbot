from dataclasses import dataclass

@dataclass
class CHATDTO:
    message: str

    @staticmethod
    def from_entity_to_DTO(message):
        print(message)
        return CHATDTO(
            message = message['content'],
        )