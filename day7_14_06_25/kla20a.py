class NotFound(Exception):
    def __init__(self, resourse, resource_id):
        msg = f"{resourse} o ID {resoure_id} nie znalezione!!!"
        super().__init__(msg)
        self.resource = resource
        self.resource_id = resource_id

    @classmethod
    def user(cls, user_id):
        return cls("Użytkownik", user_id)

    def
        return NotFound(resource, resource_id)