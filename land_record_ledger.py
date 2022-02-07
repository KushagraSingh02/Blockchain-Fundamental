import datetime 
import hashlib
import json
from urllib import response

from numpy import block
from flask import Flask,jsonify,request
from werkzeug.wrappers import response 


# individual blocks would be dictionary and the blockchain will be stored in a list
#Genesis initial block made by the owner

class blockchain:
    # chain = []
    def __init__(self) :
        self.chain = []
        self.create_block(owner = 'creator' , Reg_no = '007' ,proof = 1,previous_hash = '0')

    # this is creation of first or genesis block
    def create_block(self,owner,Reg_no,proof,previous_hash):
        block = {
            'owner' : owner , #owners name
            'Reg_no' : Reg_no, #lands registeration number 
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' :proof,
            'previous_hash' : previous_hash

        }
        self.chain.append(block)
        return block 

    #we need a proof to generate an unique hash to be added to the blockchain
    def proof_of_work(self,previous_proof):

        new_proof = 1
        check_proof = False

        while check_proof is False:

            #new_proof**2 - previous_proof**2 this is the logic we are using for new hash
            #encode is to encode in sha256 format
            hash_val = hashlib.sha256(str((new_proof**2) - (previous_proof**2)).encode()).hexdigest()

            #too keep it simple we are just considering the new hash should have 4 leading 0
            if hash_val[0:4]=='0000':
                check_proof = True

            else :
                new_proof+=1

        return new_proof

    #this function is use to take a block and return the hash of the block
    def hash(self,block ):
        encoded_block = json.dumps(block).encode() #json dump is used to stringify the object passed
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_idx = 1

        while block_idx < len(chain):
            block = chain[block_idx]
            
            if block['previous_hash']!=self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']

            hash_val = hashlib.sha256(str( (proof**2) - (previous_proof**2)).encode()).hexdigest()
            if hash[0:4]!='0000':
                return False

            previous_block = block
            block_idx +=1

        return True

    #when we are inserting new block we would need the last block in blockchain
    def get_last_block(self):
            return self.chain[-1]
    


#creating the web app

app = Flask(__name__)

blockchain = blockchain()

#getting full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }

    return jsonify(response),200


@app.route("/is_valid",methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.is_chain_valid)

    if is_valid:
        response = {'message' : 'All good .The ledger is valid '}

    else:
        response = {'message' : 'Sir, we have a problem. The records are not valid '}

    return jsonify(response),200

@app.route('/mine_block',methods=["POST"])
def mine_block():
    values  = request.get_json()

    required = ['owner','Reg_no']

    if not all(k in values for k in required):
        return "missing values" , 400

    owner = values['owner']
    Reg_no = values['Reg_no']

    previous_block = blockchain.get_last_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(owner,Reg_no,proof,previous_hash)

    response = {'message':'recorder will be added to the ledger'}
    return jsonify(response),200

# app.run(port=8080,debug=True)

#if we do host then system connected in same network can access it
app.run(host='0.0.0.0',port=5000,debug=True)