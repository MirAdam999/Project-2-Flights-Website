from business_logic.facade_base import FacadeBase


# 22.01.24
# Mir Shukhman


class AirlineFacade(FacadeBase):
    def __init__(self, token):
        super().__init__()
        self.token= token