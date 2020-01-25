# Yao's Millionaire Problem
python implementation of Yao's Millionaire Problem protocol as specified in [Protocols for secure computations](https://research.cs.wisc.edu/areas/sec/yao1982-ocr.pdf)

## requirements
- python3
- and all packages in `requirements.txt`

## usage
First off, start a node server, think of it as your Bob
```bash
# usage
# python node_server.py -h
python node_server.py 8 # 8 is the number of millions Bob owned
```

Then, start a node client, this is your Alice
```bash
# usage
# python node_client.py -h
python node_client.py ws://127.0.0.1:16233
```