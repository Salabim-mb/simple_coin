# Simple Coin - basic blockchain network simulator

<ins>Authors: Michał Balas (Salabim-mb), Maciej Czarkowski (czarkom)</ins>

### Table of contents
1. Introduction
2. How it works
3. How to use the network
4. Methods worth explaining
5. Development perspectives

### Introduction
Simple Coin is a project based on blockchain technology. It allows
its users to securely connect with others, without any centralized
supervisor. Given that, user can be sure that his privacy is put as
the top priority.

### How it works
Our project is using mechanism of digital signature verification, which
is provided by ECDSA algorithm, based on elliptic curves. With that
kind of sophisticated solution it is possible to verify author of the
message among all transactions (very often junky) received. Candidates that are verified with correct
signature and data can be then added to blockchain. Blockchain can also be fetched for lookup by any user (it is an assurance of transparency).

### Tech stack
Project is created in Flask Framework (runnning on Python 3.+) and it's using following libraries:
- gunicorn
- requests
- cryptography
- pycryptodome
- base64
- random
- ecdsa

### Current API Specification
| Method | Version | Path                                 | [Dynamic params]/[Body example]                                                                           | Sample response                                                           | Description                                                        |
|--------|---------|--------------------------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------|
| GET    | v1_1    | /fetch-blockchain                    |                                                                                                           |                                                                           | Fetch all blockchain blocks                                        |
| POST   | v1_0    | /candidate-block                     |                                                                                                           |                                                                           | Verify and add candidate block to blockchain                       |
| POST   | v1_0    | /transfer                            | [Transfer request](#transfer-request)                                                                     |                                                                           | Perform transfer of specified amount                               |
| POST   | v1_0    | /proxy/transfer/<target_port>        | target_port -- port that transfer should be sent to<br/>[Proxy transfer request](#proxy-transfer-request) |                                                                           | Transfer money from node that request is sent to to specified port |
| GET    | v1_0    | /print-node-list                     |                                                                                                           |                                                                           | Print list of all nodes register in blockchain (to server logs)    |
| GET    | v1_0    | /fetch-node-list                     |                                                                                                           | [Node list format](#node-list-format)                                     | Get list of all nodes registered in blockchain                     |
| POST   | v1_0    | /register-node                       | [Single node data](#single-node-data)                                                                     |                                                                           | Add node that the request is sent from to node list                |
| POST   | v1_0    | /message                             | {<br/>"message": "Some message",<br/>"signature": "kjhkjqwhjhkjhk"<br/>}                                  |                                                                           | Send message for signature verification                            |
| GET    | v1_0    | /message                             |                                                                                                           | {<br/>"message": "Message to sign",<br/>"signature": "iuouq,mndajh"<br/>} | Get message with appropriate signature from host                   | 
| GET    | v1_0    | /proxy/forward-message/<target_port> | target_port -- port that message<br/>should be sent to                                                    |                                                                           | Send message to <target_port> through host that is called          |

### Transfer request
```json
{
  "amount": 12,
  "transfer_id": "5126322f2r3f211edtyvd236e3232b7",
  "signature": "389d2n82n98ndnw98289hhduhhduidwhuihwuhiudhwuiwhdui21"
}
```


### Proxy transfer request
```json
{
  "amount": 1
}
```

### Single node data
```json
{
    "address": "http://127.0.0.1:5002",
    "name": 2,
    "pub_key": "yXAZ5fu6whySRAWc8oSgB4NVhZaRd5qUHHDPvK5MWcmXZPqbmQeMIGndF2PKuHjA"
}
```

### Node list format
```json
[
    {
        "address": "http://127.0.0.1:5003",
        "name": 3,
        "pub_key": "hdh3Ltgf2Vyb835ZqJHam0qAPoE3z7BgZT/haK5vjx03DGkSJR+fOs20aPnPJIob"
    },
    {
        "address": "http://127.0.0.1:5002",
        "name": 2,
        "pub_key": "yXAZ5fu6whySRAWc8oSgB4NVhZaRd5qUHHDPvK5MWcmXZPqbmQeMIGndF2PKuHjA"
    }
]
```