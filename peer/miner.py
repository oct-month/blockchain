"""矿工"""
from typing import Set, List
from queue import Queue

from config import MAX_USER_TRANSACTION_NUMBER
from chain import Btc, Block, Transaction, BlockChain, TransOutput
from verify import Verify


__all__ = ["Miner", ]


class Miner:
    def __init__(self) -> None:
        self.trans_cache = Queue()  # 交易池
        self.trans_num = MAX_USER_TRANSACTION_NUMBER    # 一个区块打包多少个交易
        self.address = ""           # 获取收益的地址

    def mining(self, block: Block) -> Block:
        """挖矿"""
        trans_list = self.__get_mining_trans()
        blc = BlockChain.get_instance()
        block = Block(blc.get_height() + 1, blc.get_top_block().get_hash())
        # 计算总交易费
        fee = Btc("0")
        for trans in trans_list:
            fee += blc.compute_transaction_fee(trans)
            block.add_transaction(trans)    # 添加交易到block中
        # 加上矿工奖励
        fee += block.get_now_ming_btcs()
        # 构造创块交易
        head_trans = Transaction()
        head_trans.add_output(TransOutput(address=self.address, btcs=fee))
        block.set_head_transaction(head_trans)
        # 正式开始挖矿
        block.find_randnum()
        return block

    def add_trans(self, trans: Transaction) -> None:
        """往交易池中添加交易（先验证）"""
        if Verify.verify_new_transaction(trans):
            self.trans_cache.put(trans)
            # TODO 广播交易
    
    def __get_mining_trans(self) -> List[Transaction]:
        """获取用于打包区块的交易（阻塞）"""
        trans_list = []
        for i in range(self.trans_num):
            tap = self.trans_cache.get()
            trans_list.append(tap)
        return trans_list

    def accept_block(self, block: Block) -> None:
        """胜利者已经产生（新块已加入区块链）"""
        # TODO 广播新块
        # TODO 停止挖矿
