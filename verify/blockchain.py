"""验证区块链的合法性"""
import time
from typing import List

from chain import BlockChain
from config import FIREST_BLOCK_PREHASH
from .base import BaseBlockChainVerify


__all__ = ["BlockChainVerify", ]


class OrderBlockChain(BaseBlockChainVerify):
    """验证区块链的顺序性"""
    def __init__(self) -> None:
        super().__init__()
    
    def is_ok(self) -> bool:
        pre_hash = FIREST_BLOCK_PREHASH
        for i, block in enumerate(BlockChain.get_instance().get_blocks()):
            # 索引值index应合法
            if block.get_index() != i + 1:
                return False
            # pre_hash值应为上一个区块
            if pre_hash != block.get_prehash():
                return False
            pre_hash = block.get_hash()
        return True


class TimestapBlockChain(BaseBlockChainVerify):
    """检查每个区块的时间戳"""
    def __init__(self) -> None:
        super().__init__()
    
    def is_ok(self) -> bool:
        blc = BlockChain.get_instance()
        for block in blc.get_blocks():
            # 区块的时间戳肯定比区块链要后
            if block.get_timestap() < blc.get_start_time():
                return False
            # 区块的时间戳肯定比现在前
            if block.get_timestap() > time.localtime():
                return False
        return True


BlockChainVerify: List[type] = [OrderBlockChain, TimestapBlockChain]
