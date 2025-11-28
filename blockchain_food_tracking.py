"""
🔗 Blockchain-Based Food Supply Chain Tracking
Unique Feature: Track food from farm to plate with transparency
Prevents corruption and ensures quality
"""

import hashlib
import json
from datetime import datetime

class FoodSupplyBlockchain:
    """
    Simple blockchain implementation for food supply chain tracking
    Ensures transparency and prevents tampering
    """
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
        # Create genesis block
        self.create_block(previous_hash='0', proof=1)
    
    def create_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1])
        }
        
        self.pending_transactions = []
        self.chain.append(block)
        return block
    
    def hash_block(self, block):
        """
        Create SHA-256 hash of a block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def add_food_transaction(self, food_item, stage, location, handler, quantity, quality_check=True):
        """
        Add a food supply chain transaction
        
        Stages: Purchase -> Storage -> Preparation -> Distribution -> Consumption
        """
        transaction = {
            'food_item': food_item,
            'stage': stage,
            'location': location,
            'handler': handler,
            'quantity_kg': quantity,
            'quality_check_passed': quality_check,
            'timestamp': str(datetime.now()),
            'transaction_id': hashlib.sha256(
                f"{food_item}{stage}{datetime.now()}".encode()
            ).hexdigest()[:16]
        }
        
        self.pending_transactions.append(transaction)
        return transaction
    
    def get_food_journey(self, food_item):
        """
        Get complete journey of a food item from farm to plate
        """
        journey = []
        
        for block in self.chain:
            for transaction in block.get('transactions', []):
                if transaction.get('food_item') == food_item:
                    journey.append({
                        'block': block['index'],
                        'stage': transaction['stage'],
                        'location': transaction['location'],
                        'handler': transaction['handler'],
                        'timestamp': transaction['timestamp'],
                        'quality_passed': transaction['quality_check_passed']
                    })
        
        return journey
    
    def verify_chain_integrity(self):
        """
        Verify that blockchain hasn't been tampered with
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if previous hash matches
            if current_block['previous_hash'] != self.hash_block(previous_block):
                return False
            
            # Check if block hash is valid
            if not self.hash_block(current_block).startswith('0000'):
                # Simplified proof of work
                pass
        
        return True
    
    def generate_qr_code_for_food(self, food_item):
        """
        Generate QR code linking to food's blockchain record
        """
        import qrcode
        
        # Create URL with food journey
        journey_hash = hashlib.sha256(food_item.encode()).hexdigest()[:12]
        url = f"https://nutrition-advisor.app/track/{journey_hash}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"food_qr_{journey_hash}.png"
        img.save(filename)
        
        return filename, url


class SupplyChainDashboard:
    """
    Dashboard for monitoring food supply chain
    """
    
    def __init__(self, blockchain):
        self.blockchain = blockchain
    
    def get_supply_chain_stats(self):
        """
        Get overall supply chain statistics
        """
        total_transactions = sum(len(block.get('transactions', [])) for block in self.blockchain.chain)
        
        # Calculate quality metrics
        quality_passed = 0
        total_quality_checks = 0
        
        for block in self.blockchain.chain:
            for transaction in block.get('transactions', []):
                if 'quality_check_passed' in transaction:
                    total_quality_checks += 1
                    if transaction['quality_check_passed']:
                        quality_passed += 1
        
        quality_rate = (quality_passed / total_quality_checks * 100) if total_quality_checks > 0 else 0
        
        return {
            'total_transactions': total_transactions,
            'total_blocks': len(self.blockchain.chain),
            'quality_pass_rate': round(quality_rate, 2),
            'chain_verified': self.blockchain.verify_chain_integrity(),
            'last_transaction_time': self.blockchain.chain[-1]['timestamp'] if self.blockchain.chain else None
        }
    
    def detect_anomalies(self):
        """
        Detect suspicious activities in supply chain
        """
        anomalies = []
        
        for block in self.blockchain.chain:
            for transaction in block.get('transactions', []):
                # Check for failed quality checks
                if not transaction.get('quality_check_passed', True):
                    anomalies.append({
                        'type': 'Quality Failure',
                        'food_item': transaction['food_item'],
                        'stage': transaction['stage'],
                        'timestamp': transaction['timestamp']
                    })
                
                # Check for unusual quantity changes
                # (This would need historical comparison)
        
        return anomalies


# ============================================
# EXAMPLE USAGE
# ============================================

def demo_blockchain_tracking():
    """
    Demonstrate blockchain food tracking
    """
    blockchain = FoodSupplyBlockchain()
    
    # Track rice from purchase to consumption
    print("📦 Tracking Rice Supply Chain\n")
    
    # Stage 1: Purchase
    blockchain.add_food_transaction(
        food_item="Basmati Rice",
        stage="Purchase",
        location="Local Market, Bangalore",
        handler="Vendor: Ram Kumar",
        quantity=50,
        quality_check=True
    )
    blockchain.create_block(proof=12345)
    
    # Stage 2: Storage
    blockchain.add_food_transaction(
        food_item="Basmati Rice",
        stage="Storage",
        location="Anganwadi Storage Room",
        handler="Worker: Lakshmi",
        quantity=50,
        quality_check=True
    )
    blockchain.create_block(proof=67890)
    
    # Stage 3: Preparation
    blockchain.add_food_transaction(
        food_item="Basmati Rice",
        stage="Preparation",
        location="Anganwadi Kitchen",
        handler="Cook: Radha",
        quantity=10,  # 10kg used for cooking
        quality_check=True
    )
    blockchain.create_block(proof=11111)
    
    # Stage 4: Distribution
    blockchain.add_food_transaction(
        food_item="Basmati Rice",
        stage="Distribution",
        location="Anganwadi Main Hall",
        handler="Worker: Sita",
        quantity=10,
        quality_check=True
    )
    blockchain.create_block(proof=22222)
    
    # Get journey
    journey = blockchain.get_food_journey("Basmati Rice")
    print("🔗 Rice Journey:")
    for step in journey:
        print(f"  Block {step['block']}: {step['stage']} at {step['location']}")
        print(f"    Handled by: {step['handler']}")
        print(f"    Quality: {'✅ Passed' if step['quality_passed'] else '❌ Failed'}\n")
    
    # Verify integrity
    print(f"🔒 Blockchain Integrity: {'✅ Verified' if blockchain.verify_chain_integrity() else '❌ Compromised'}")
    
    # Dashboard stats
    dashboard = SupplyChainDashboard(blockchain)
    stats = dashboard.get_supply_chain_stats()
    print(f"\n📊 Supply Chain Statistics:")
    print(f"  Total Transactions: {stats['total_transactions']}")
    print(f"  Quality Pass Rate: {stats['quality_pass_rate']}%")
    print(f"  Blocks in Chain: {stats['total_blocks']}")


# ============================================
# FLASK ROUTES TO ADD
# ============================================
"""
Add to flask_app.py:

from blockchain_food_tracking import FoodSupplyBlockchain, SupplyChainDashboard

food_blockchain = FoodSupplyBlockchain()
supply_dashboard = SupplyChainDashboard(food_blockchain)

@app.route('/api/blockchain/add-transaction', methods=['POST'])
def add_blockchain_transaction():
    '''Add food transaction to blockchain'''
    data = request.json
    
    transaction = food_blockchain.add_food_transaction(
        food_item=data['food_item'],
        stage=data['stage'],
        location=data['location'],
        handler=data['handler'],
        quantity=data['quantity'],
        quality_check=data.get('quality_check', True)
    )
    
    # Create new block
    proof = hash(str(datetime.now()))
    food_blockchain.create_block(proof=proof)
    
    return jsonify({
        'success': True,
        'transaction': transaction,
        'block_created': True
    })

@app.route('/api/blockchain/track/<food_item>')
def track_food_item(food_item):
    '''Track food item journey'''
    journey = food_blockchain.get_food_journey(food_item)
    
    return jsonify({
        'success': True,
        'food_item': food_item,
        'journey': journey,
        'total_stages': len(journey)
    })

@app.route('/api/blockchain/stats')
def blockchain_stats():
    '''Get supply chain statistics'''
    stats = supply_dashboard.get_supply_chain_stats()
    anomalies = supply_dashboard.detect_anomalies()
    
    return jsonify({
        'success': True,
        'stats': stats,
        'anomalies': anomalies
    })

@app.route('/blockchain-dashboard')
def blockchain_dashboard():
    '''Blockchain transparency dashboard'''
    return render_template('blockchain_dashboard.html')
"""

if __name__ == "__main__":
    demo_blockchain_tracking()
