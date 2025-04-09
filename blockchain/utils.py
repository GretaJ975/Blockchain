from datetime import datetime
from .models import Block


class Blockchain:
    difficulty = 4

    @staticmethod
    def create_genesis_block():

        if Block.objects.count() == 0:
            genesis_block = Block(
                timestamp=datetime.utcnow(),
                data="Genesis Block",
                previous_hash="0"
            )
            genesis_block.hash = genesis_block.compute_hash()
            genesis_block.save()
            return genesis_block

    @staticmethod
    def get_last_block():
        return Block.objects.order_by('-id').first()

    @staticmethod
    def add_new_block(data):
        last_block = Blockchain.get_last_block()
        new_block = Block(
            timestamp=datetime.utcnow(),
            data=data,
            previous_hash=last_block.hash if last_block else "0"
        )

        new_block.hash, new_block.nonce = Blockchain.proof_of_work(new_block)
        new_block.save()
        return new_block

    @staticmethod
    def proof_of_work(block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash, block.nonce