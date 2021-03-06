"""交易输出的数据结构"""
from typing import List

from .btc import Btc


__all__ = ["TransOutput", ]


_SPLIT_STR = ":"     # 用于分隔的字符串


class TransOutput:
    """交易输出"""
    def __init__(self, btcs: Btc=Btc("0"), address: str="") -> None:
        """初始化"""
        self.btcs = btcs
        self.address = address
    
    @classmethod
    def load(cls, trans_output: str) -> "TransOutput":
        tap = trans_output.split(_SPLIT_STR)
        return cls(Btc(tap[0]), tap[1])

    def keys(self) -> List[str]:
        return [
            "btcs",
            "address"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __str__(self) -> str:
        """btcs:address"""
        return f"{self.btcs}{_SPLIT_STR}{self.address}"
    
    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __ne__(self, other) -> bool:
        return str(self) != str(other)
