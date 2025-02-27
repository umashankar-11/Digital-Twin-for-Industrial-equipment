import datetime
import pandas as pd

class EquipmentLifecycle:
    def __init__(self, equipment_id, installation_date):
        self.equipment_id = equipment_id
        self.installation_date = installation_date
        self.upgrade_history = []
        self.replacement_history = []
        self.decommission_date = None

    def record_upgrade(self, upgrade_type, upgrade_date):
        self.upgrade_history.append({
            'Upgrade Type': upgrade_type,
            'Upgrade Date': upgrade_date
        })

    def record_replacement(self, part, replacement_date):
        self.replacement_history.append({
            'Part Replaced': part,
            'Replacement Date': replacement_date
        })

    def decommission(self, decommission_date):
        self.decommission_date = decommission_date

    def get_lifecycle_summary(self):
        return {
            'Equipment ID': self.equipment_id,
            'Installation Date': self.installation_date,
            'Upgrade History': self.upgrade_history,
            'Replacement History': self.replacement_history,
            'Decommission Date': self.decommission_date
        }


equipment = EquipmentLifecycle("EQ12345", datetime.date(2018, 5, 12))


equipment.record_upgrade("Software Update", datetime.date(2020, 3, 15))
equipment.record_upgrade("Hardware Upgrade", datetime.date(2021, 8, 10))
equipment.record_replacement("Pump", datetime.date(2022, 2, 5))
equipment.decommission(datetime.date(2025, 1, 15))


lifecycle_summary = equipment.get_lifecycle_summary()
print(pd.DataFrame(lifecycle_summary))

