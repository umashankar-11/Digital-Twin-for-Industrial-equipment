import pandas as pd
import random

class SupplyChainIntegration:
    def __init__(self):
        self.parts_inventory = {
            'Pump': 10,
            'Valve': 5,
            'Motor': 8
        }
        self.equipment_health = {
            'EQ12345': {'Status': 'Operational', 'LastMaintenance': '2024-01-15', 'NeedsParts': []},
            'EQ67890': {'Status': 'Operational', 'LastMaintenance': '2023-11-20', 'NeedsParts': ['Pump']}
        }

    def check_parts_availability(self, equipment_id):
        needs_parts = self.equipment_health[equipment_id]['NeedsParts']
        unavailable_parts = []

        for part in needs_parts:
            if self.parts_inventory.get(part, 0) == 0:
                unavailable_parts.append(part)

        return unavailable_parts

    def schedule_downtime(self, equipment_id):
       
        unavailable_parts = self.check_parts_availability(equipment_id)
        if unavailable_parts:
          
            return f"Scheduled downtime for {equipment_id} due to missing parts: {', '.join(unavailable_parts)}."
        else:
            return f"{equipment_id} is ready for maintenance."

    def update_parts_inventory(self, part, quantity)gitgg:
        if part in self.parts_inventory:
            self.parts_inventory[part] += quantity
        else:
            self.parts_inventory[part] = quantity

    def update_equipment_status(self, equipment_id, status):
        self.equipment_health[equipment_id]['Status'] = status


supply_chain = SupplyChainIntegration()


equipment_id = 'EQ67890'
downtime_message = supply_chain.schedule_downtime(equipment_id)
print(downtime_message)


supply_chain.update_parts_inventory('Pump', 5)


downtime_message = supply_chain.schedule_downtime(equipment_id)
print(downtime_message)
