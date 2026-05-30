import unicodedata

# Função pra pegar essa disgrama de nome sem ficar com acento nem os carai
def create_player_id(name):

    normalized = unicodedata.normalize("NFD", name)

    no_accents = "".join(

        char for char in normalized

        if unicodedata.category(char) != "Mn"

    )

    return (
        no_accents
        .strip()
        .lower()
        .replace(" ", "_")
    )