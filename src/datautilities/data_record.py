class DataRecord:
    def __init__(
        self,
        organization,
        platform_handle,
        obs_type,
        uom_type,
        s_order,
        value,
        date_time,
    ):
        self.organization = organization
        self.platform_handle = platform_handle
        self.obs_type = obs_type
        self.uom_type = uom_type
        self.s_order = s_order
        self.value = value
        self.date_time = date_time
