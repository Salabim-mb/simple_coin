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
message among all messages (very often junky) received.

### Tech stack
Project is created in Flask Framework (runnning on Python 3.+) and it's using following libraries:
- gunicorn
- requests
- cryptography
- pycryptodome
- ecdsa

### Current API Specification
| Method | Version | Path                                 | [Dynamic params]/[Body example]                                          | Sample response                                                           | Description                                                     |
|--------|---------|--------------------------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------|
| GET    | v1_0    | /print-node-list                     |                                                                          |                                                                           | Print list of all nodes register in blockchain (to server logs) |
| GET    | v1_0    | /fetch-node-list                     |                                                                          | [Node list format](#node-list-format)                                     | Get list of all nodes registered in blockchain                  |
| POST   | v1_0    | /register-node                       | [Single node data](#single-node-data)                                    |                                                                           | Add node that the request is sent from to node list             |
| POST   | v1_0    | /message                             | {<br/>"message": "Some message",<br/>"signature": "kjhkjqwhjhkjhk"<br/>} |                                                                           | Send message for signature verification                         |
| GET    | v1_0    | /message                             |                                                                          | {<br/>"message": "Message to sign",<br/>"signature": "iuouq,mndajh"<br/>} | Get message with appropriate signature from host                | 
| GET    | v1_0    | /proxy/forward-message/<target_port> | target_port -- port that message<br/>should be sent to                   |                                                                           | Send message to <target_port> through host that is called       |


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