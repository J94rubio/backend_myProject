class Cita:
    def __init__(
        self,
        id: int,
        mascota_id: int,
        fecha: str,
        motivo: str,
        estado: str
    ):
        self.id = id
        self.mascota_id = mascota_id
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado