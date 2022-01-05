# d-chat

Decentralized text messaging application using python sockets. 

## What is decentralized text messaging?

Decentralized means without any central authority, this means that there is no one who can control the messages being sent or received but the nodes (computers connected to a network) themselves. Unlike current messaging services (like WhatsApp, Snapchat, Telegram, etc.) which use a group of centralized server which stores all your messages, which is then distributed to specific users. In the case of d-chat there is no such server, but your message goes directly to the receiver(s), thus ensuring better security. Decentralization also ensures that there is no single point of failure - if a server goes down then an entire chat system is down (this is the case with current systems), but with a decentralized system there is no single point of failure, even if a node drops from the network the system continues to work flawlessly. Isn't this exciting? If you think so too then download d-chat today :)

# Steps to install 

1. Install d-chat using pip:

```bash
use@programmer~:$ pip install git+https://github.com/pulse-net/d-chat.git
```

2. Run dchat command:

2.1 To create a new dchat network:

```bash
user@programmer~:$ dchat --create
```

2.2 To join an existing dchat network:

```bash
user@programmer~:$ dchat --join
```