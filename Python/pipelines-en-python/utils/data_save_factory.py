import json
from pathlib import Path


class DataSaveFactory:
    _SAVERS = {
        "txt": "_save_txt",
        "json": "_save_json",
    }

    def _save_txt(self, result, id, output_dir):
        output_file = Path(output_dir) / f"result_{id}.txt"
        with output_file.open("w", encoding="utf-8") as f:
            for customer_id, category in result:
                f.write(f"{customer_id}, {category}\n")
        return output_file

    def _save_json(self, result, id, output_dir):
        output_file = Path(output_dir) / f"result_{id}.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(
                [{"customer_id": customer_id, "category": category} for customer_id, category in result],
                f,
                indent=4,
                ensure_ascii=False,
            )
        return output_file

    def save_file(self, save_type, result, id, output_dir="."):
        saver = self._SAVERS.get(save_type)
        if saver is None:
            raise ValueError(
                f"save_type no soportado: {save_type!r}. Opciones: {sorted(self._SAVERS)}"
            )
        return getattr(self, saver)(result=result, id=id, output_dir=output_dir)
