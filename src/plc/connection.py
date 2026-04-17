from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

try:
    from pylogix import PLC
except Exception:  # pragma: no cover
    PLC = None


@dataclass
class ConnectionConfig:
    ip: str
    slot: int = 0


class PLCConnection:
    def __init__(self) -> None:
        self._ip = ""
        self._slot = 0

    @property
    def connected(self) -> bool:
        return bool(self._ip)

    def configure(self, ip: str, slot: int) -> None:
        self._ip = ip.strip()
        self._slot = int(slot)

    def test_connection(self, ip: str, slot: int) -> Tuple[bool, str]:
        if PLC is None:
            return False, "pylogix no está instalado en el entorno."
        if not ip.strip():
            return False, "IP del PLC vacía."
        try:
            with PLC() as comm:
                comm.IPAddress = ip.strip()
                comm.ProcessorSlot = int(slot)
                resp = comm.GetPLCTime()
                if getattr(resp, "Status", "") == "Success":
                    self.configure(ip, slot)
                    return True, "Conexión exitosa."
                return False, f"Fallo al conectar: {getattr(resp, 'Status', 'Error desconocido')}"
        except Exception as exc:
            return False, f"Error de conexión: {exc}"

    def discover_tags(self) -> Tuple[bool, List[Dict[str, str]], str]:
        if PLC is None:
            return False, [], "pylogix no está instalado en el entorno."
        if not self.connected:
            return False, [], "No hay PLC configurado."
        try:
            with PLC() as comm:
                comm.IPAddress = self._ip
                comm.ProcessorSlot = self._slot
                resp = comm.GetTagList()
                if getattr(resp, "Status", "") != "Success":
                    return False, [], f"No se pudieron listar tags: {getattr(resp, 'Status', 'Error')}"
                tags = []
                for tag in getattr(resp, "Value", []) or []:
                    tags.append(
                        {
                            "name": getattr(tag, "TagName", ""),
                            "type": getattr(tag, "DataType", "Unknown"),
                            "value": "-",
                        }
                    )
                return True, tags, "Tags obtenidos correctamente."
        except Exception as exc:
            return False, [], f"Error listando tags: {exc}"

    def read_tags(self, tag_names: List[str]) -> Tuple[bool, Dict[str, str], str]:
        if PLC is None:
            return False, {}, "pylogix no está instalado en el entorno."
        if not self.connected:
            return False, {}, "No hay PLC configurado."
        if not tag_names:
            return True, {}, "Sin tags seleccionados."
        try:
            with PLC() as comm:
                comm.IPAddress = self._ip
                comm.ProcessorSlot = self._slot
                results = comm.Read(tag_names)
                if not isinstance(results, list):
                    results = [results]
                values: Dict[str, str] = {}
                for item in results:
                    name = getattr(item, "TagName", "")
                    status = getattr(item, "Status", "")
                    values[name] = str(getattr(item, "Value", "ERR")) if status == "Success" else "ERR"
                return True, values, "Lectura correcta."
        except Exception as exc:
            return False, {}, f"Error leyendo tags: {exc}"
