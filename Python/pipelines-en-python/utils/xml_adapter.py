from pathlib import Path

import pandas as pd

COLUMN_NAMES = [
    "Customer ID",
    "Age",
    "Gender",
    "Item Purchased",
    "Category",
    "Purchase Amount (USD)",
    "Location",
    "Size",
    "Color",
    "Season",
    "Review Rating",
    "Subscription Status",
    "Shipping Type",
    "Discount Applied",
    "Promo Code Used",
    "Previous Purchases",
    "Payment Method",
    "Frequency of Purchases",
    "year",
]


class XMLAdapter:
    """Normaliza un XML de shopping behavior al mismo esquema de columnas que los CSV."""

    column_names = COLUMN_NAMES

    def __init__(self, xml_data_path):
        self.xml_data_path = Path(xml_data_path)

    def get_data(self):
        if not self.xml_data_path.is_file():
            raise FileNotFoundError(f"No se encontro el archivo XML: {self.xml_data_path}")

        df = pd.read_xml(self.xml_data_path)

        if len(df.columns) != len(self.column_names):
            raise ValueError(
                f"{self.xml_data_path.name} tiene {len(df.columns)} columnas, "
                f"se esperaban {len(self.column_names)}"
            )

        df.columns = self.column_names
        return df


XMLAdpater = XMLAdapter
