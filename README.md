# underpass - a UDP/wirguard TURN service (WIP)
Underpass is a simple python server you can run to connect wireguard peers behind NAT, without having to run wireguard on the underpass server itself.

## advantages
Typical wireguard setups involve at least one web-facing peer playing router for the other peers. This is easy to setup and maintain, however suffers from the flaw that all wireguard traffic is decrypted and re-encrypted on the web-facing "relay". 
Underpass is just a glorified port-forwarder, all wireguard traffic is routed without being decrypted. 
This enables you to use underpass as a substitute for a regular wireguard relay when:
- the Kernel of the relay does not support wireguard yet
- you do not have root access on the relay
- the relay is just a container VM not a full blown (V)PS

## disadavantages
Underpass requires constant NAT traversal and peer endpoint reconfiguration on your clients. This might cause some packet loss and connection instability. 
